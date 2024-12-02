from fastapi import FastAPI
from pydantic import BaseModel
import subprocess
import json

# Inicializamos la app
app = FastAPI()

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

#endpoint para modificar el chroma subsampling
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

@app.post("/count_tracks/")
def count_tracks(data: TrackInfoModel):
    try:
        #optenemos los tracks por separado
        video_tracks = obtener_pistas(data.input_path, "v")  #video
        audio_tracks = obtener_pistas(data.input_path, "a")  #audio
        subtitle_tracks = obtener_pistas(data.input_path, "s")  #subtítulos

        #contamos cada track
        num_video_tracks = len(video_tracks)
        num_audio_tracks = len(audio_tracks)
        num_subtitle_tracks = len(subtitle_tracks)

        #sumamos el total 
        total_tracks = num_video_tracks + num_audio_tracks + num_subtitle_tracks

        return {
            "total_tracks": total_tracks,
            "video_tracks": num_video_tracks,
            "audio_tracks": num_audio_tracks,
            "subtitle_tracks": num_subtitle_tracks
        }

    except Exception as e:
        return {"error": str(e)}
    
#EJERCICIO 6
class MotionVectorModel(BaseModel):
    input_path: str
    output_path: str

@app.post("/generate_motion_vectors/")
def generate_motion_vectors(data: MotionVectorModel):
    try:
        #comando sacado de la pagina de ffmepg
        comando = [
            "ffmpeg", "-flags2", "+export_mvs", "-i", data.input_path,
            "-vf", "codecview=mv=pf+bf+bb",
            data.output_path
        ]
        
        subprocess.run(comando, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        return {
            "message": "Video generado con macroblocks y motion vectors",
            "output_path": data.output_path
        }
    except subprocess.CalledProcessError as e:
        return {"error": f"FFmpeg failed: {e.stderr}"}
    except Exception as e:
        return {"error": str(e)}
    
    
#EJERCICIO 7
class YUVHistogramModel(BaseModel):
    input_path: str
    output_path: str

# Endpoint para generar el histograma YUV
@app.post("/generate_yuv_histogram/")
def generate_yuv_histogram(data: YUVHistogramModel):
    try:
        #comando sacado de la pagina de ffmepg
        comando = [
            "ffmpeg", "-i", data.input_path,
            "-vf", "split=2[a][b];[b]histogram,format=yuv420p[hh];levels=full[hh];[a][hh]overlay",
            data.output_path
        ]
        
        subprocess.run(comando, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        return {
            "message": "Video generado con el histograma YUV",
            "output_path": data.output_path
        }
    except subprocess.CalledProcessError as e:
        return {"error": f"FFmpeg failed: {e.stderr}"}
    except Exception as e:
        return {"error": str(e)}
