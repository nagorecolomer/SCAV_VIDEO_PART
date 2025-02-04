from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
import shutil
import os
import subprocess
import json

from firts_seminar import ex2, ex3, ex4, ex5, ex5_2, ex6, ex7

app = FastAPI()

@app.get("/")
async def mensaje_inicial():
    return {"mensaje": "Buenas!! Bienvenidos a nuestra super API, quereis ver como funciona?"}





#EJERCICIO 3 
@app.post("/resize_image/")
def resize_image(data: ResizeImageModel):
    try:
        # Construir el comando FFmpeg para redimensionar la imagen
        comando = [
            "ffmpeg", "-i", data.input_path,
            "-vf", f"scale={data.width}:{data.height}",
            data.output_path
        ]

        # Ejecutar el comando FFmpeg
        subprocess.run(comando, check=True)

        return {"message": "Imagen redimensionada correctamente", "output_path": data.output_path}
    except subprocess.CalledProcessError as e:
        return {"error": f"Error al ejecutar FFmpeg: {e.stderr}"}
    except Exception as e:
        return {"error": str(e)}






#EJERCICIO 1 
class ResizeVideoModel(BaseModel):
    input_path: str
    output_path: str
    width: int
    height: int

#endpoint para redimensionar videos, reutilizamos el endpoint del anterior lab 
@app.post("/resize_video/")
def resize_video(data: ResizeVideoModel):
    try:
        comando = [
            "ffmpeg", "-i", data.input_path,
            "-vf", f"scale={data.width}:{data.height}",
            data.output_path
        ]
        subprocess.run(comando, check=True)  #ejecuta FFmpeg
        return {"message": "Video redimensionado correctamente", "output_path": data.output_path}
    except Exception as e:
        return {"error": str(e)}
    

#EJERCICIO 2 
class ChromaSubsamplingModel(BaseModel):
    input_path: str
    output_path: str
    subsampling: str  #Buscar valores en la lista de ffmepg


class VideoInfoModel(BaseModel):
    input_path: str
    
#endpoint para leer la información del video
@app.post("/get_video_info/")
def get_video_info(data: VideoInfoModel):
    try:
        #Comando sacado de la pagina de ffmepg
        comando = [
            "ffprobe", "-v", "error", "-show_format", "-show_streams",
            "-print_format", "json", data.input_path
        ]
        resultado = subprocess.run(comando, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        if resultado.returncode != 0:
            return {"error": resultado.stderr}

        video_info = json.loads(resultado.stdout)

        #Extraemos datos relevantes
        formato = video_info.get("format", {})
        streams = video_info.get("streams", [{}])

        #datos básicos que podemos obtener 
        data_relevante = {
            "format_name": formato.get("format_name"),
            "duration": float(formato.get("duration", 0)),  #duración en segundos
            "bit_rate": int(formato.get("bit_rate", 0)),  #bit rate
            "resolution": f"{streams[0].get('width')}x{streams[0].get('height')}",  #resolución
            "codec_name": streams[0].get("codec_name"),  #codec
            "frame_rate": eval(streams[0].get("avg_frame_rate", "0")),  #FPS, cuadros por segundo
        }

        return {"video_info": data_relevante}

    except Exception as e:
        return {"error": str(e)}
    
    
#EJERCICIO 4 
class VideoProcessingModel(BaseModel):
    input_path: str
    output_video_path: str
    output_audio_aac: str
    output_audio_mp3: str
    output_audio_ac3: str
    final_output_path: str

# Endpoint para realizar todas las operaciones
@app.post("/process_video/")
def process_video(data: VideoProcessingModel):
    try:
        #cortamos el video a 20 segundos
        subprocess.run([
            "ffmpeg", "-i", data.input_path, "-t", "20",
            "-c:v", "copy", "-c:a", "copy", data.output_video_path
        ], check=True)

        #extraemos el audio en diferentes formatos, los comando son sacados de la pagina oficial de ffmpeg
        #AAC Mono
        subprocess.run([
            "ffmpeg", "-i", data.output_video_path, "-ac", "1",
            "-c:a", "aac", data.output_audio_aac
        ], check=True)

        #MP3 Estéreo con menor bitrate
        subprocess.run([
            "ffmpeg", "-i", data.output_video_path, "-b:a", "96k",
            "-c:a", "libmp3lame", data.output_audio_mp3
        ], check=True)

        #AC3 Codec
        subprocess.run([
            "ffmpeg", "-i", data.output_video_path,
            "-c:a", "ac3", data.output_audio_ac3
        ], check=True)

        #Empaquetamos todo en un archivo MP4
        subprocess.run([
            "ffmpeg", "-i", data.output_video_path,
            "-i", data.output_audio_aac, "-i", data.output_audio_mp3, "-i", data.output_audio_ac3,
            "-map", "0:v", "-map", "1:a", "-map", "2:a", "-map", "3:a",
            "-c", "copy", data.final_output_path
        ], check=True)

        return {"message": "Procesamiento completo", "final_output": data.final_output_path}

    except Exception as e:
        return {"error": str(e)}
    
#EJERCICIO 5 
class TrackInfoModel(BaseModel):
    input_path: str

def obtener_pistas(file_path: str, stream_type: str) -> list:
    #comando sacado de la pagina de ffmepg
    comando = [
        "ffprobe", "-i", file_path,
        "-show_streams", "-select_streams", stream_type,
        "-print_format", "json"
    ]
    resultado = subprocess.run(comando, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)


    if resultado.returncode != 0:
        print(f"Error al analizar {stream_type}: {resultado.stderr}")
        return []

    #para poder escribir en la api 
    info = json.loads(resultado.stdout)
    return info.get("streams", [])




#EJERCICIO 1 
#Modelo para recibir los datos de entrada
class VideoConversionModel(BaseModel):
    input_path: str
    output_path: str
    codec: str  #Puede ser "vp8", "vp9", "h265" o "av1"

#Endpoint para convertir videos
@app.post("/convert_video/")
def convert_video(data: VideoConversionModel):
    codec_map = {
        "vp8": "libvpx",
        "vp9": "libvpx-vp9",
        "h265": "libx265",
        "h264": "libx264",
        "av1": "libaom-av1"
    }

    if data.codec not in codec_map:
        raise HTTPException(status_code=400, detail="Códec no soportado. Usa vp8, vp9, h265 o av1.")

    try:
        #Construir el comando FFmpeg
        comando = [
            "ffmpeg", "-i", data.input_path,  # Archivo de entrada
            "-c:v", codec_map[data.codec],   # Selección del códec
            "-b:v", "1M",                    # Bitrate de salida
            data.output_path                 # Archivo de salida
        ]
        # Ejecutar FFmpeg
        subprocess.run(comando, check=True)

        return {"message": f"Video convertido exitosamente a {data.codec}", "output_path": data.output_path}
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"Error al convertir el video: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

#EJERCICIO 2 
class AudioModificationModel(BaseModel):
    input_path: str         # Ruta del archivo de entrada (video)
    output_audio_path: str  # Ruta del archivo de salida (audio modificado)
    audio_bitrate: str      # Bitrate deseado para el audio (por ejemplo, "128k", "256k")
    audio_channels: int     # Número de canales, por ejemplo, 1 (mono), 2 (estéreo)
    audio_format: str       # Formato deseado, como "aac", "mp3", "wav"


#Reutilizando la función 'process_video' pero modificándola para que solo modifique el audio
def process_video(input_path: str, output_audio_path: str, audio_bitrate: str, audio_channels: int, audio_format: str, is_audio_only=False):
    try:
        if is_audio_only:
            comando = [
                "ffmpeg", "-i", input_path,  # Ruta de entrada (video)
                "-b:a", audio_bitrate,      # Bitrate del audio
                "-ac", str(audio_channels), # Número de canales de audio
                "-c:a", audio_format,       # Formato de audio
                output_audio_path           # Ruta de salida (audio extraído)
            ]
        else:
            #Si se necesita hacer más procesamiento (esto se reutiliza de la función original)
            comando = [
                "ffmpeg", "-i", input_path,  # Ruta de entrada
                "-vf", "scale=1280:720",     # Ejemplo de un filtro (puedes agregar otros filtros o procesos)
                "-c:a", audio_format,        # Audio formateado
                output_audio_path            # Ruta de salida
            ]

        #Ejecutar el comando FFmpeg
        subprocess.run(comando, check=True)

        return {"message": "Audio modificado correctamente", "output_audio_path": output_audio_path}
    except subprocess.CalledProcessError as e:
        return {"error": f"Error al ejecutar FFmpeg: {e.stderr}"}
    except Exception as e:
        return {"error": str(e)}

#Endpoint para modificar el audio
@app.post("/modify_audio/")
def modify_audio(data: AudioModificationModel):
    #Llamamos a la función `process_video` para solo modificar el audio
    return process_video(
        input_path=data.input_path,
        output_audio_path=data.output_audio_path,
        audio_bitrate=data.audio_bitrate,
        audio_channels=data.audio_channels,
        audio_format=data.audio_format,
        is_audio_only=True  #Indicamos que solo modificamos el audio
    )


