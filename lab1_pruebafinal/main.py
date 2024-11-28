from fastapi import FastAPI,File, UploadFile
from pydantic import BaseModel
import shutil
import os
import subprocess
from first_seminar import ex2, ex3, ex4, ex5, ex5_2, ex6, ex7
import test_first_seminar 

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "hola Uri,estoy probando"}

""" @app.post("/upload-photo/")
async def upload_photo(file: UploadFile = File(...)):
    try:
        # Ruta donde guardar la imagen subida dentro del contenedor
        file_location = f"/app/uploaded_files/{file.filename}"
        
        # Guardar el archivo en el contenedor
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        return {"message": "Photo uploaded successfully", "file_path": file_location}
    except Exception as e:
        return {"error": str(e)} """
# Modelos para validar las solicitudes de entrada
class RGBModel(BaseModel):
    r: int
    g: int
    b: int

class ResizeImageModel(BaseModel):
    input_path: str
    output_path: str
    width: int
    height: int

class RunLengthEncodingModel(BaseModel):
    data: list[int]

    
# 1. Endpoint para la conversión RGB a YUV
@app.post("/rgb_to_yuv/")
def test_RGB_to_YUV(data: RGBModel):
    try:
        y, u, v = ex2.RGB_to_YUV(data.r, data.g, data.b)
        return {"Y": y, "U": u, "V": v}
    except Exception as e:
        return {"error": str(e)}

# # 2. Endpoint para la conversión YUV a RGB
# @app.post("/yuv_to_rgb/")
# def yuv_to_rgb(data: RGBModel):
#     try:
#         r, g, b = ex2.YUV_to_RGB(data.r, data.g, data.b)
#         return {"R": r, "G": g, "B": b}
#     except Exception as e:
#         return {"error": str(e)}

# 3. Endpoint para redimensionar imágenes
@app.post("/resize_image/")
def resize_image(data: ResizeImageModel):
    try:
        result_path = ex3.redimensionar_imagen(data.input_path, data.output_path, data.width, data.height)
        return {"output_path": result_path}
    except Exception as e:
        return {"error": str(e)}

# 4. Endpoint para la serpentine diagonal
# @app.post("/serpentine_diagonal/")
# def serpentine_diagonal(matrix: list[list[int]]):
#     try:
#         result = ex4.serpentine_diagonal(matrix)
#         return {"result": result}
#     except Exception as e:
#         return {"error": str(e)}

# 5. Endpoint para convertir a blanco y negro y comprimir
@app.post("/convertir_bn_y_comprimir/")
def convertir_bn_y_comprimir(data: ResizeImageModel):
    try:
        output_path = ex5.convertir_bn_y_comprimir(data.input_path, data.output_path)
        return {"output_path": output_path}
    except Exception as e:
        return {"error": str(e)}

# 6. Endpoint para codificación Run Length Encoding
# @app.post("/run_length_encoding/")
# def run_length_encoding(data: RunLengthEncodingModel):
#     try:
#         result = ex5_2.run_length_encoding(data.data)
#         return {"result": result}
#     except Exception as e:
#         return {"error": str(e)}

# 7. Endpoint para aplicar DCT y obtener la inversa (IDCT)
""" @app.post("/dct_idct/")
def dct_idct(data: list[list[float]]):
    try:
        result_dct = ex6.run_dct(data)
        result_idct = ex6.run_idct(result_dct)
        return {"result_dct": result_dct, "result_idct": result_idct}
    except Exception as e:
        return {"error": str(e)}
 """
# 8. Endpoint para aplicar DWT e IDWT
""" @app.post("/dwt_idwt/")
def dwt_idwt(data: list[list[float]]):
    try:
        LL, LH, HL, HH = ex7.apply_dwt(data)
        reconstructed_data = ex7.apply_idwt(LL, LH, HL, HH)
        return {"LL": LL, "LH": LH, "HL": HL, "HH": HH, "reconstructed_data": reconstructed_data}
    except Exception as e:
        return {"error": str(e)} """
