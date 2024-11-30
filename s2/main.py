from fastapi import FastAPI
from pydantic import BaseModel
import subprocess
import json

# Inicializamos la app
app = FastAPI()

#EJERCICIO 1
# Modelo para recibir parámetros del cliente
class ResizeVideoModel(BaseModel):
    input_path: str
    output_path: str
    width: int
    height: int

# Endpoint para redimensionar videos
@app.post("/resize_video/")
def resize_video(data: ResizeVideoModel):
    try:
        #Mismo comando que resize image del lab anterior
        comando = [
            "ffmpeg", "-i", data.input_path,
            "-vf", f"scale={data.width}:{data.height}",
            data.output_path
        ]
        subprocess.run(comando, check=True)  # Ejecuta FFmpeg
        return {"message": "Video redimensionado correctamente", "output_path": data.output_path}
    except Exception as e:
        return {"error": str(e)}
    

#EJERCICIO 2
# Modelo de entrada
class ChromaSubsamplingModel(BaseModel):
    input_path: str
    output_path: str
    subsampling: str  # Valores que podemos poner como (yuv444p,yuv422p,yuv420)

# Endpoint para modificar el chroma subsampling
@app.post("/modify_chroma_subsampling/")
def modify_chroma_subsampling(data: ChromaSubsamplingModel):
    try:
        comando = [
            "ffmpeg", "-i", data.input_path,
            "-pix_fmt", data.subsampling,
            data.output_path
        ]
        subprocess.run(comando, check=True)
        return {"message": "Chroma subsampling modificado correctamente", "output_path": data.output_path}
    except Exception as e:
        return {"error": str(e)}

#EJERCICIO 3
class VideoInfoModel(BaseModel):
    input_path: str
    
    
# Endpoint para leer la información del video
@app.post("/get_video_info/")
def get_video_info(data: VideoInfoModel):
    try:
        # Ejecuta ffprobe para obtener información del video en formato JSON
        comando = [
            "ffprobe", "-v", "error", "-show_format", "-show_streams",
            "-print_format", "json", data.input_path
        ]
        resultado = subprocess.run(comando, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        if resultado.returncode != 0:
            return {"error": resultado.stderr}

        video_info = json.loads(resultado.stdout)

        # Extraemos datos relevantes
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
# Modelo para recibir parámetros
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

        #extraemos el audio en diferentes formatos
        # AAC Mono
        subprocess.run([
            "ffmpeg", "-i", data.output_video_path, "-ac", "1",
            "-c:a", "aac", data.output_audio_aac
        ], check=True)

        # MP3 Estéreo con menor bitrate
        subprocess.run([
            "ffmpeg", "-i", data.output_video_path, "-b:a", "96k",
            "-c:a", "libmp3lame", data.output_audio_mp3
        ], check=True)

        # AC3 Codec
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
