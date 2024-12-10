from fastapi import FastAPI, UploadFile, File,HTTPException
from pydantic import BaseModel
import subprocess
import json
import os
import shutil
from test_first_seminar import ex2, ex5  

# Define rutas base para los archivos
BASE_MEDIA_DIR = "media"
INPUT_DIR = os.path.join(BASE_MEDIA_DIR, "input")
OUTPUT_DIR = os.path.join(BASE_MEDIA_DIR, "output")
os.makedirs(INPUT_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Inicializamos la app
app = FastAPI()


# Función para guardar un archivo subido
def save_uploaded_file(file: UploadFile, folder: str) -> str:
    os.makedirs(folder, exist_ok=True)
    file_path = os.path.join(folder, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return file_path


# 1. Subir archivo
@app.post("/upload_file/")
async def upload_file(file: UploadFile = File(...)):
    try:
        file_path = save_uploaded_file(file, INPUT_DIR)
        return {"message": f"Archivo '{file.filename}' subido correctamente", "path": file_path}
    except Exception as e:
        return {"error": str(e)}

#ENDPOINT ELEGIDOS LAB1
class RGBInput(BaseModel):
    r: int
    g: int
    b: int

class ImageInput(BaseModel):
    image_path: str
    output_path: str
    
@app.post("/convert_rgb_to_yuv/")
async def convert_rgb_to_yuv(data: RGBInput):
    r, g, b = data.r, data.g, data.b
    y, u, v = ex2.RGB_to_YUV(r, g, b)
    return {"Y": y, "U": u, "V": v}

@app.post("/convert_bn_and_compress/")
async def convert_bn_and_compress(data: ImageInput):
    imagen = data.image_path
    output = data.output_path
    ex5.convertir_bn_y_comprimir(imagen, output)
    return {"message": f"Imagen convertida y comprimida correctamente en {output}"}



#EJERCICIO 1 S2
class ResizeVideoModel(BaseModel):
    input_path: str
    output_path: str
    width: int
    height: int
# 2. Redimensionar video
@app.post("/resize_video/")
async def resize_video(file: UploadFile = File(...), width: int = 1280, height: int = 720):
    try:
        input_path = save_uploaded_file(file, INPUT_DIR)
        output_path = os.path.join(OUTPUT_DIR, f"resized_{file.filename}")
        comando = [
            "ffmpeg", "-i", input_path,
            "-vf", f"scale={width}:{height}",
            output_path
        ]
        subprocess.run(comando, check=True)
        return {"message": "Video redimensionado correctamente", "output_path": output_path}
    except Exception as e:
        return {"error": str(e)}


# 3. Modificar Chroma Subsampling
@app.post("/modify_chroma_subsampling/")
async def modify_chroma_subsampling(file: UploadFile = File(...), subsampling: str = "yuv420p"):
    try:
        input_path = save_uploaded_file(file, INPUT_DIR)
        output_path = os.path.join(OUTPUT_DIR, f"subsampling_{file.filename}")
        comando = [
            "ffmpeg", "-i", input_path,
            "-pix_fmt", subsampling,
            output_path
        ]
        subprocess.run(comando, check=True)
        return {"message": "Chroma subsampling modificado correctamente", "output_path": output_path}
    except Exception as e:
        return {"error": str(e)}


# 4. Obtener información del video
@app.post("/get_video_info/")
async def get_video_info(file: UploadFile = File(...)):
    try:
        input_path = save_uploaded_file(file, INPUT_DIR)
        comando = [
            "ffprobe", "-v", "error", "-show_format", "-show_streams",
            "-print_format", "json", input_path
        ]
        resultado = subprocess.run(comando, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if resultado.returncode != 0:
            return {"error": resultado.stderr}
        video_info = json.loads(resultado.stdout)
        return {"video_info": video_info}
    except Exception as e:
        return {"error": str(e)}


# 5. Procesar video
@app.post("/process_video/")
async def process_video(file: UploadFile = File(...)):
    try:
        input_path = save_uploaded_file(file, INPUT_DIR)
        output_video_path = os.path.join(OUTPUT_DIR, f"processed_{file.filename}")
        output_audio_aac = os.path.join(OUTPUT_DIR, f"audio_aac_{file.filename}.aac")
        output_audio_mp3 = os.path.join(OUTPUT_DIR, f"audio_mp3_{file.filename}.mp3")
        output_audio_ac3 = os.path.join(OUTPUT_DIR, f"audio_ac3_{file.filename}.ac3")
        final_output_path = os.path.join(OUTPUT_DIR, f"final_{file.filename}")

        # Cortar el video a 20 segundos
        subprocess.run([
            "ffmpeg", "-i", input_path, "-t", "20",
            "-c:v", "copy", "-c:a", "copy", output_video_path
        ], check=True)

        # Extraer audio en diferentes formatos
        subprocess.run(["ffmpeg", "-i", output_video_path, "-ac", "1", "-c:a", "aac", output_audio_aac], check=True)
        subprocess.run(["ffmpeg", "-i", output_video_path, "-b:a", "96k", "-c:a", "libmp3lame", output_audio_mp3], check=True)
        subprocess.run(["ffmpeg", "-i", output_video_path, "-c:a", "ac3", output_audio_ac3], check=True)

        # Empaquetar en un archivo final
        subprocess.run([
            "ffmpeg", "-i", output_video_path,
            "-i", output_audio_aac, "-i", output_audio_mp3, "-i", output_audio_ac3,
            "-map", "0:v", "-map", "1:a", "-map", "2:a", "-map", "3:a",
            "-c", "copy", final_output_path
        ], check=True)

        return {"message": "Procesamiento completo", "final_output": final_output_path}
    except Exception as e:
        return {"error": str(e)}


# 6. Contar pistas
@app.post("/count_tracks/")
async def count_tracks(file: UploadFile = File(...)):
    try:
        input_path = save_uploaded_file(file, INPUT_DIR)
        comando = [
            "ffprobe", "-i", input_path,
            "-show_streams", "-select_streams", "v", "-print_format", "json"
        ]
        resultado = subprocess.run(comando, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        video_tracks = len(json.loads(resultado.stdout).get("streams", []))
        return {"message": f"El archivo tiene {video_tracks} pistas de video."}
    except Exception as e:
        return {"error": str(e)}


# 7. Generar macroblocks y motion vectors
@app.post("/generate_motion_vectors/")
async def generate_motion_vectors(file: UploadFile = File(...)):
    try:
        input_path = save_uploaded_file(file, INPUT_DIR)
        output_path = os.path.join(OUTPUT_DIR, f"motion_vectors_{file.filename}")
        comando = [
            "ffmpeg", "-flags2", "+export_mvs", "-i", input_path,
            "-vf", "codecview=mv=pf+bf+bb", output_path
        ]
        subprocess.run(comando, check=True)
        return {"message": "Video generado con macroblocks y motion vectors", "output_path": output_path}
    except Exception as e:
        return {"error": str(e)}


# 8. Generar histograma YUV
@app.post("/generate_yuv_histogram/")
async def generate_yuv_histogram(file: UploadFile = File(...)):
    try:
        input_path = save_uploaded_file(file, INPUT_DIR)
        output_path = os.path.join(OUTPUT_DIR, f"histogram_{file.filename}")
        comando = [
            "ffmpeg", "-i", input_path,
            "-vf", "split=2[a][b];[b]histogram,format=yuv420p[hh];[a][hh]overlay",
            output_path
        ]
        subprocess.run(comando, check=True)
        return {"message": "Video generado con el histograma YUV", "output_path": output_path}
    except Exception as e:
        return {"error": str(e)}


#EJERCICIO 1 P2
# Modelo para recibir los datos de entrada
class VideoConversionModel(BaseModel):
    input_path: str
    output_path: str
    codec: str  # Puede ser "vp8", "vp9", "h265" o "av1"

# Endpoint para convertir videos
@app.post("/convert_video/")
def convert_video(data: VideoConversionModel):
    codec_map = {
        "vp8": "libvpx",
        "vp9": "libvpx-vp9",
        "h265": "libx265",
        "av1": "libaom-av1"
    }

    if data.codec not in codec_map:
        raise HTTPException(status_code=400, detail="Códec no soportado. Usa vp8, vp9, h265 o av1.")

    try:
        # Construir el comando FFmpeg
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
