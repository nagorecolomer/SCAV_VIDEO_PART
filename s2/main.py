from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
import subprocess
import json
import os
import shutil

# Define la ruta base de la carpeta de medios
BASE_MEDIA_DIR = "s2\\media"

# Asegúrate de que las carpetas `input` y `output` existen
os.makedirs(os.path.join(BASE_MEDIA_DIR, "input"), exist_ok=True)
os.makedirs(os.path.join(BASE_MEDIA_DIR, "output"), exist_ok=True)

# Inicializa la app
app = FastAPI()

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    try:
        # Ruta donde guardar el archivo
        input_dir = os.path.join(BASE_MEDIA_DIR, "input")
        file_path = os.path.join(input_dir, file.filename)
        
        # Guardar el archivo subido
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        return {"message": "Archivo subido correctamente", "file_path": file_path}
    except Exception as e:
        return {"error": str(e)}


# EJERCICIO 1
class ResizeVideoModel(BaseModel):
    input_path: str  # Relativo a `input`
    output_path: str  # Relativo a `output`
    width: int
    height: int

@app.post("/resize_video/")
def resize_video(data: ResizeVideoModel):
    try:
        input_dir = os.path.join(BASE_MEDIA_DIR, "input")
        output_dir = os.path.join(BASE_MEDIA_DIR, "output")
        
        input_path = os.path.join(input_dir, data.input_path)
        output_path = os.path.join(output_dir, data.output_path)
        
        comando = [
            "ffmpeg", "-i", input_path,
            "-vf", f"scale={data.width}:{data.height}",
            output_path
        ]
        subprocess.run(comando, check=True)
        return {"message": "Video redimensionado correctamente", "output_path": output_path}
    except Exception as e:
        return {"error": str(e)}


# EJERCICIO 2
class ChromaSubsamplingModel(BaseModel):
    input_path: str  # Relativo a `input`
    output_path: str  # Relativo a `output`
    subsampling: str

@app.post("/modify_chroma_subsampling/")
def modify_chroma_subsampling(data: ChromaSubsamplingModel):
    try:
        input_dir = os.path.join(BASE_MEDIA_DIR, "input")
        output_dir = os.path.join(BASE_MEDIA_DIR, "output")
        
        input_path = os.path.join(input_dir, data.input_path)
        output_path = os.path.join(output_dir, data.output_path)
        
        comando = [
            "ffmpeg", "-i", input_path,
            "-pix_fmt", data.subsampling,
            output_path
        ]
        subprocess.run(comando, check=True)
        return {"message": "Chroma subsampling modificado correctamente", "output_path": output_path}
    except Exception as e:
        return {"error": str(e)}


# EJERCICIO 3
class VideoInfoModel(BaseModel):
    input_path: str  # Relativo a `input`

@app.post("/get_video_info/")
def get_video_info(data: VideoInfoModel):
    try:
        input_dir = os.path.join(BASE_MEDIA_DIR, "input")
        input_path = os.path.join(input_dir, data.input_path)
        
        comando = [
            "ffprobe", "-v", "error", "-show_format", "-show_streams",
            "-print_format", "json", input_path
        ]
        resultado = subprocess.run(comando, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        if resultado.returncode != 0:
            return {"error": resultado.stderr}

        video_info = json.loads(resultado.stdout)
        formato = video_info.get("format", {})
        streams = video_info.get("streams", [{}])
        
        data_relevante = {
            "format_name": formato.get("format_name"),
            "duration": float(formato.get("duration", 0)),
            "bit_rate": int(formato.get("bit_rate", 0)),
            "resolution": f"{streams[0].get('width')}x{streams[0].get('height')}",
            "codec_name": streams[0].get("codec_name"),
            "frame_rate": eval(streams[0].get("avg_frame_rate", "0")),
        }

        return {"video_info": data_relevante}
    except Exception as e:
        return {"error": str(e)}


# EJERCICIO 4
class VideoProcessingModel(BaseModel):
    input_path: str  # Relativo a `input`
    output_video_path: str  # Relativo a `output`
    output_audio_aac: str  # Relativo a `output`
    output_audio_mp3: str  # Relativo a `output`
    output_audio_ac3: str  # Relativo a `output`
    final_output_path: str  # Relativo a `output`

@app.post("/process_video/")
def process_video(data: VideoProcessingModel):
    try:
        input_dir = os.path.join(BASE_MEDIA_DIR, "input")
        output_dir = os.path.join(BASE_MEDIA_DIR, "output")
        
        input_path = os.path.join(input_dir, data.input_path)
        output_video_path = os.path.join(output_dir, data.output_video_path)
        output_audio_aac = os.path.join(output_dir, data.output_audio_aac)
        output_audio_mp3 = os.path.join(output_dir, data.output_audio_mp3)
        output_audio_ac3 = os.path.join(output_dir, data.output_audio_ac3)
        final_output_path = os.path.join(output_dir, data.final_output_path)

        # Cortamos el video
        subprocess.run(["ffmpeg", "-i", input_path, "-t", "20", "-c:v", "copy", "-c:a", "copy", output_video_path], check=True)
        subprocess.run(["ffmpeg", "-i", output_video_path, "-ac", "1", "-c:a", "aac", output_audio_aac], check=True)
        subprocess.run(["ffmpeg", "-i", output_video_path, "-b:a", "96k", "-c:a", "libmp3lame", output_audio_mp3], check=True)
        subprocess.run(["ffmpeg", "-i", output_video_path, "-c:a", "ac3", output_audio_ac3], check=True)
        subprocess.run([
            "ffmpeg", "-i", output_video_path,
            "-i", output_audio_aac, "-i", output_audio_mp3, "-i", output_audio_ac3,
            "-map", "0:v", "-map", "1:a", "-map", "2:a", "-map", "3:a",
            "-c", "copy", final_output_path
        ], check=True)

        return {"message": "Procesamiento completo", "final_output": final_output_path}
    except Exception as e:
        return {"error": str(e)}


# EJERCICIO 5
class TrackInfoModel(BaseModel):
    input_path: str  # Relativo a `input`

@app.post("/count_tracks/")
def count_tracks(data: TrackInfoModel):
    try:
        input_dir = os.path.join(BASE_MEDIA_DIR, "input")
        input_path = os.path.join(input_dir, data.input_path)

        def obtener_pistas(file_path: str, stream_type: str) -> list:
            comando = [
                "ffprobe", "-i", file_path,
                "-show_streams", "-select_streams", stream_type,
                "-print_format", "json"
            ]
            resultado = subprocess.run(comando, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

            if resultado.returncode != 0:
                return []

            info = json.loads(resultado.stdout)
            return info.get("streams", [])

        video_tracks = obtener_pistas(input_path, "v")
        audio_tracks = obtener_pistas(input_path, "a")
        subtitle_tracks = obtener_pistas(input_path, "s")

        return {
            "total_tracks": len(video_tracks) + len(audio_tracks) + len(subtitle_tracks),
            "video_tracks": len(video_tracks),
            "audio_tracks": len(audio_tracks),
            "subtitle_tracks": len(subtitle_tracks),
        }
    except Exception as e:
        return {"error": str(e)}


# EJERCICIO 6
class MotionVectorModel(BaseModel):
    input_path: str  # Relativo a `input`
    output_path: str  # Relativo a `output`

@app.post("/generate_motion_vectors/")
def generate_motion_vectors(data: MotionVectorModel):
    try:
        input_dir = os.path.join(BASE_MEDIA_DIR, "input")
        output_dir = os.path.join(BASE_MEDIA_DIR, "output")
        
        input_path = os.path.join(input_dir, data.input_path)
        output_path = os.path.join(output_dir, data.output_path)

        comando = [
            "ffmpeg", "-flags2", "+export_mvs", "-i", input_path,
            "-vf", "codecview=mv=pf+bf+bb",
            output_path
        ]
        subprocess.run(comando, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        return {"message": "Video generado con motion vectors", "output_path": output_path}
    except Exception as e:
        return {"error": str(e)}


# EJERCICIO 7
class YUVHistogramModel(BaseModel):
    input_path: str  # Relativo a `input`
    output_path: str  # Relativo a `output`

@app.post("/generate_yuv_histogram/")
def generate_yuv_histogram(data: YUVHistogramModel):
    try:
        input_dir = os.path.join(BASE_MEDIA_DIR, "input")
        output_dir = os.path.join(BASE_MEDIA_DIR, "output")
        
        input_path = os.path.join(input_dir, data.input_path)
        output_path = os.path.join(output_dir, data.output_path)

        comando = [
            "ffmpeg", "-i", input_path,
            "-vf", "split=2[a][b];[b]histogram,format=yuv420p[hh];[a][hh]overlay",
            output_path
        ]
        subprocess.run(comando, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        return {"message": "Histograma YUV generado", "output_path": output_path}
    except Exception as e:
        return {"error": str(e)}
