from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import subprocess

app = FastAPI()

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
