import tkinter as tk
from tkinter import filedialog, messagebox
import requests
import json
import os

# URL base de la API
API_URL = "http://127.0.0.1:8000"

# Funciones generales para selección de archivos y rutas
def select_file(entry_var):
    file_path = filedialog.askopenfilename()
    if file_path:
        entry_var.set(file_path)

def select_output(entry_var):
    output_path = filedialog.asksaveasfilename()
    if output_path:
        entry_var.set(output_path)

# Funciones para cada operación
import requests
from tkinter import messagebox

# Funciones para cada operación
def rgb_to_yuv(r_var, g_var, b_var):
    try:
        # Obtener los valores RGB del formulario
        r = int(r_var.get())
        g = int(g_var.get())
        b = int(b_var.get())
        
        # Crear el diccionario de datos para la solicitud
        data = {
            "r": r,
            "g": g,
            "b": b
        }
        
        # Hacer la solicitud al servidor
        response = requests.post(f"{API_URL}/convertir_rgb_a_yuv/", json=data)

        result = response.json()

        # Si hay un error, mostrarlo
        if "error" in result:
            messagebox.showerror("Error", result["error"])
        else:
            # Mostrar los valores YUV en lugar de 'output_path'
            y = result.get("y")
            u = result.get("u")
            v = result.get("v")
            messagebox.showinfo("Éxito", f"Conversión a YUV exitosa.\nY: {y}\nU: {u}\nV: {v}")

    except Exception as e:
        messagebox.showerror("Error", str(e))


def resize_image():
    try:
        data = {
            "input_path": input_path_var.get(),
            "output_path": output_path_var.get(),
            "width": int(width_var.get()),
            "height": int(height_var.get())
        }
        response = requests.post(f"{API_URL}/resize_image/", json=data)
        result = response.json()
        if "error" in result:
            messagebox.showerror("Error", result["error"])
        else:
            messagebox.showinfo("Éxito", f"Imagen redimensionada: {result['output_path']}")
    except Exception as e:
        messagebox.showerror("Error", str(e))
        
def convertir_bn_y_comprimir():
    try:
        if not input_path_var.get() or not output_path_var.get():
            messagebox.showerror("Error", "Debe especificar las rutas de entrada y salida.")
            return
        data = {"input_path": input_path_var.get(),  
                "output_path": output_path_var.get()  
            }
        response = requests.post(f"{API_URL}/convertir_bn_y_comprimir/", json=data)
        result = response.json()
        
        if "error" in result:
            messagebox.showerror("Error", result["error"])
        else:
            messagebox.showinfo("Éxito", f"Convertido a Blanco y Negro y Comprimido:{result['output_path']}")
    except Exception as e:
        messagebox.showerror("Error", str(e))



def resize_video():
    try:
        data = {
            "input_path": input_path_var.get(),
            "output_path": output_path_var.get(),
            "width": int(width_var.get()),
            "height": int(height_var.get())
        }
        response = requests.post(f"{API_URL}/resize_video/", json=data)
        result = response.json()
        if "error" in result:
            messagebox.showerror("Error", result["error"])
        else:
            messagebox.showinfo("Éxito", f"Video redimensionado: {result['output_path']}")
    except Exception as e:
        messagebox.showerror("Error", str(e))
        

def modify_chroma_subsampling():
    try:
        data = {
            "input_path": input_path_var.get(),
            "output_path": output_path_var.get(),
            "subsampling": subsampling_var.get()  # Usamos el mismo campo que para códec
        }
        response = requests.post(f"{API_URL}/modify_chroma_subsampling/", json=data)
        result = response.json()
        if "error" in result:
            messagebox.showerror("Error", result["error"])
        else:
            messagebox.showinfo("Éxito", f"Submuestreo de croma modificado: {result['output_path']}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def get_video_info():
    try:
        input_path = input_path_var.get()
        response = requests.post(f"{API_URL}/get_video_info/", json={"input_path": input_path})
        result = response.json()
        if "error" in result:
            messagebox.showerror("Error", result["error"])
        else:
            messagebox.showinfo("Información del Video", f"Info: {result['video_info']}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def procesar_video(input_path_var, output_path_var):
    try:
        # Obtenemos las rutas de los archivos desde los campos de texto
        data = {
            "input_path": input_path_var.get(),
            "output_path": output_path_var.get()
        }

        # Hacemos la solicitud al endpoint de la API
        response = requests.post(f"{API_URL}/procesar_video/", json=data)

        # Procesamos la respuesta de la API
        result = response.json()

        # Si hay un error en la respuesta, lo mostramos
        if "error" in result:
            messagebox.showerror("Error", result["error"])
        else:
            messagebox.showinfo("Éxito", f"Video procesado exitosamente: {result['output_path']}")
    
    except Exception as e:
        messagebox.showerror("Error", str(e))

def count_tracks():
    try:
        input_path = input_path_var.get()
        response = requests.post(f"{API_URL}/count_tracks/", json={"input_path": input_path})
        result = response.json()
        if "error" in result:
            messagebox.showerror("Error", result["error"])
        else:
            messagebox.showinfo(
                "Conteo de Pistas",
                f"Total: {result['total_tracks']}, Video: {result['video_tracks']}, Audio: {result['audio_tracks']}, Subtítulos: {result['subtitle_tracks']}"
            )
    except Exception as e:
        messagebox.showerror("Error", str(e))
        

def generate_motion_vectors():
    try:
        data = {
            "input_path": input_path_var.get(),
            "output_path": output_path_var.get()
        }
        response = requests.post(f"{API_URL}/generate_motion_vectors/", json=data)
        result = response.json()
        if "error" in result:
            messagebox.showerror("Error", result["error"])
        else:
            messagebox.showinfo("Éxito", f"Motion vectors generados: {result['output_path']}")
    except Exception as e:
        messagebox.showerror("Error", str(e))
        

def generate_yuv_histogram():
    try:
        data = {
            "input_path": input_path_var.get(),
            "output_path": output_path_var.get()
        }
        response = requests.post(f"{API_URL}/generate_yuv_histogram/", json=data)
        result = response.json()
        if "error" in result:
            messagebox.showerror("Error", result["error"])
        else:
            messagebox.showinfo("Éxito", f"Histograma YUV generado: {result['output_path']}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def convert_video():
    try:
        data = {
            "input_path": input_path_var.get(),
            "output_path": output_path_var.get(),
            "codec": codec_var.get()
        }
        response = requests.post(f"{API_URL}/convert_video/", json=data)
        result = response.json()
        if "error" in result:
            messagebox.showerror("Error", result["error"])
        else:
            messagebox.showinfo("Éxito", f"Video convertido: {result['output_path']}")
    except Exception as e:
        messagebox.showerror("Error", str(e))



# Crear ventana principal
root = tk.Tk()
root.title("Monster API - GUI")


# Variables globales
r_var = tk.StringVar()
g_var = tk.StringVar()
b_var = tk.StringVar()
input_path_var = tk.StringVar()
output_path_var = tk.StringVar()
width_var = tk.StringVar()
height_var = tk.StringVar()
codec_var = tk.StringVar()

# Frame para RGB a YUV
frame_rgb_to_yuv = tk.LabelFrame(root, text="RGB a YUV")
frame_rgb_to_yuv.grid(row=8, column=0, padx=10, pady=10, sticky="w")
tk.Label(frame_rgb_to_yuv, text="R:").grid(row=0, column=0)
tk.Entry(frame_rgb_to_yuv, textvariable=r_var).grid(row=0, column=1)
tk.Label(frame_rgb_to_yuv, text="G:").grid(row=1, column=0)
tk.Entry(frame_rgb_to_yuv, textvariable=g_var).grid(row=1, column=1)
tk.Label(frame_rgb_to_yuv, text="B:").grid(row=2, column=0)
tk.Entry(frame_rgb_to_yuv, textvariable=b_var).grid(row=2, column=1)
tk.Button(frame_rgb_to_yuv, text="Convertir RGB a YUV", command=lambda: rgb_to_yuv(r_var, g_var, b_var)).grid(row=3, columnspan=2)



# Frame para Redimensionar Imagen
frame_resize_image = tk.LabelFrame(root, text="Redimensionar Imagen")  
frame_resize_image.grid(row=1, column=0, padx=10, pady=10, sticky="w")  
tk.Label(frame_resize_image, text="Input Path:").grid(row=0, column=0)
tk.Entry(frame_resize_image, textvariable=input_path_var, width=40).grid(row=0, column=1)
tk.Button(frame_resize_image, text="Seleccionar", command=lambda: select_file(input_path_var)).grid(row=0, column=2)
tk.Label(frame_resize_image, text="Output Path:").grid(row=1, column=0)
tk.Entry(frame_resize_image, textvariable=output_path_var, width=40).grid(row=1, column=1)
tk.Button(frame_resize_image, text="Seleccionar", command=lambda: select_output(output_path_var)).grid(row=1, column=2)
tk.Label(frame_resize_image, text="Width:").grid(row=2, column=0)
tk.Entry(frame_resize_image, textvariable=width_var).grid(row=2, column=1)
tk.Label(frame_resize_image, text="Height:").grid(row=3, column=0)
tk.Entry(frame_resize_image, textvariable=height_var).grid(row=3, column=1)
tk.Button(frame_resize_image, text="Redimensionar", command=resize_image).grid(row=4, columnspan=3)

# # Frame para Convertir en Blanco y Negro y Comprimir
# frame_bn_compress = tk.LabelFrame(root, text="Convertir en Blanco y Negro y Comprimir")
# frame_bn_compress.grid(row=9, column=0, padx=10, pady=10, sticky="w")

# # input_path_bn_compress = tk.StringVar()
# # output_path_bn_compress = tk.StringVar()

# tk.Label(frame_bn_compress, text="Input Path:").grid(row=0, column=0)
# tk.Entry(frame_bn_compress, textvariable=input_path_var, width=40).grid(row=0, column=1)
# tk.Button(frame_bn_compress, text="Seleccionar", command=lambda: select_file(input_path_var)).grid(row=0, column=2)

# tk.Label(frame_bn_compress, text="Output Path:").grid(row=1, column=0)
# tk.Entry(frame_bn_compress, textvariable=output_path_var, width=40).grid(row=1, column=1)
# tk.Button(frame_bn_compress, text="Seleccionar", command=lambda: select_output(output_path_var)).grid(row=1, column=2)

# tk.Button(frame_bn_compress, text="Convertir y Comprimir", command=convertir_bn_y_comprimir).grid(row=2, columnspan=3)


# Frame para Redimensionar Video
frame_resize_video = tk.LabelFrame(root, text="Redimensionar Video") 
frame_resize_video.grid(row=2, column=0, padx=10, pady=10, sticky="w")  
tk.Label(frame_resize_video, text="Input Path:").grid(row=0, column=0)
tk.Entry(frame_resize_video, textvariable=input_path_var, width=40).grid(row=0, column=1)
tk.Button(frame_resize_video, text="Seleccionar", command=lambda: select_file(input_path_var)).grid(row=0, column=2)
tk.Label(frame_resize_video, text="Output Path:").grid(row=1, column=0)
tk.Entry(frame_resize_video, textvariable=output_path_var, width=40).grid(row=1, column=1)
tk.Button(frame_resize_video, text="Seleccionar", command=lambda: select_output(output_path_var)).grid(row=1, column=2)
tk.Label(frame_resize_video, text="Width:").grid(row=2, column=0)
tk.Entry(frame_resize_video, textvariable=width_var).grid(row=2, column=1)
tk.Label(frame_resize_video, text="Height:").grid(row=3, column=0)
tk.Entry(frame_resize_video, textvariable=height_var).grid(row=3, column=1)
tk.Button(frame_resize_video, text="Redimensionar", command=resize_video).grid(row=4, columnspan=3)

# Frame para Modificar Submuestreo de Croma
# frame_chroma = tk.LabelFrame(root, text="Modificar Submuestreo de Croma")
# frame_chroma.grid(row=4, column=0, padx=10, pady=10, sticky="w")

# input_path_chroma = tk.StringVar()
# output_path_chroma = tk.StringVar()
# subsampling_var = tk.StringVar()

# tk.Label(frame_chroma, text="Input Path:").grid(row=0, column=0)
# tk.Entry(frame_chroma, textvariable=input_path_chroma, width=40).grid(row=0, column=1)
# tk.Button(frame_chroma, text="Seleccionar", command=lambda: select_file(input_path_chroma)).grid(row=0, column=2)
# tk.Label(frame_chroma, text="Output Path:").grid(row=1, column=0)
# tk.Entry(frame_chroma, textvariable=output_path_chroma, width=40).grid(row=1, column=1)
# tk.Button(frame_chroma, text="Seleccionar", command=lambda: select_output(output_path_chroma)).grid(row=1, column=2)
# tk.Label(frame_chroma, text="Submuestreo:").grid(row=2, column=0)
# tk.Entry(frame_chroma, textvariable=subsampling_var).grid(row=2, column=1)
# tk.Button(frame_chroma, text="Modificar", command=modify_chroma_subsampling).grid(row=3, columnspan=3)


# Frame para Información del Video
frame_info = tk.LabelFrame(root, text="Información del Video")
frame_info.grid(row=3, column=0, padx=10, pady=10, sticky="w")
tk.Label(frame_info, text="Input Path:").grid(row=0, column=0)
tk.Entry(frame_info, textvariable=input_path_var, width=40).grid(row=0, column=1)
tk.Button(frame_info, text="Seleccionar", command=lambda: select_file(input_path_var)).grid(row=0, column=2)
tk.Button(frame_info, text="Obtener Información", command=get_video_info).grid(row=1, columnspan=3)

# # Frame para Procesar Video
# frame_procesar_video = tk.LabelFrame(root, text="Procesar Video")
# frame_procesar_video.grid(row=11, column=0, padx=10, pady=10, sticky="w")

# input_path_procesar_video = tk.StringVar()
# output_path_procesar_video = tk.StringVar()

# tk.Label(frame_procesar_video, text="Input Path:").grid(row=0, column=0)
# tk.Entry(frame_procesar_video, textvariable=input_path_procesar_video, width=40).grid(row=0, column=1)
# tk.Button(frame_procesar_video, text="Seleccionar", command=lambda: select_file(input_path_procesar_video)).grid(row=0, column=2)

# tk.Label(frame_procesar_video, text="Output Path:").grid(row=1, column=0)
# tk.Entry(frame_procesar_video, textvariable=output_path_procesar_video, width=40).grid(row=1, column=1)
# tk.Button(frame_procesar_video, text="Seleccionar", command=lambda: select_output(output_path_procesar_video)).grid(row=1, column=2)

# tk.Button(frame_procesar_video, text="Procesar Video", command=lambda: procesar_video(input_path_procesar_video, output_path_procesar_video)).grid(row=2, columnspan=3)

# Frame para Contar Pistas DA 0 NS PQ 
frame_count_tracks = tk.LabelFrame(root, text="Contar Pistas")
frame_count_tracks.grid(row=6, column=0, padx=10, pady=10, sticky="w")

input_path_count_tracks = tk.StringVar()

tk.Label(frame_count_tracks, text="Input Path:").grid(row=0, column=0)
tk.Entry(frame_count_tracks, textvariable=input_path_count_tracks, width=40).grid(row=0, column=1)
tk.Button(frame_count_tracks, text="Seleccionar", command=lambda: select_file(input_path_count_tracks)).grid(row=0, column=2)
tk.Button(frame_count_tracks, text="Contar Pistas", command=count_tracks).grid(row=1, columnspan=3)


# # Frame para Generar Vectores de Movimiento
# frame_vectors = tk.LabelFrame(root, text="Generar Vectores de Movimiento")
# frame_vectors.grid(row=5, column=0, padx=10, pady=10, sticky="w")

# input_path_vectors = tk.StringVar()
# output_path_vectors = tk.StringVar()

# tk.Label(frame_vectors, text="Input Path:").grid(row=0, column=0)
# tk.Entry(frame_vectors, textvariable=input_path_vectors, width=40).grid(row=0, column=1)
# tk.Button(frame_vectors, text="Seleccionar", command=lambda: select_file(input_path_vectors)).grid(row=0, column=2)
# tk.Label(frame_vectors, text="Output Path:").grid(row=1, column=0)
# tk.Entry(frame_vectors, textvariable=output_path_vectors, width=40).grid(row=1, column=1)
# tk.Button(frame_vectors, text="Seleccionar", command=lambda: select_output(output_path_vectors)).grid(row=1, column=2)
# tk.Button(frame_vectors, text="Generar", command= generate_motion_vectors).grid(row=2, columnspan=3)

# # Frame para Generar Histograma YUV
# frame_yuv_histogram = tk.LabelFrame(root, text="Generar Histograma YUV")
# frame_yuv_histogram.grid(row=7, column=0, padx=10, pady=10, sticky="w")

# input_path_yuv_histogram = tk.StringVar()
# output_path_yuv_histogram = tk.StringVar()

# tk.Label(frame_yuv_histogram, text="Input Path:").grid(row=0, column=0)
# tk.Entry(frame_yuv_histogram, textvariable=input_path_yuv_histogram, width=40).grid(row=0, column=1)
# tk.Button(frame_yuv_histogram, text="Seleccionar", command=lambda: select_file(input_path_yuv_histogram)).grid(row=0, column=2)

# tk.Label(frame_yuv_histogram, text="Output Path:").grid(row=1, column=0)
# tk.Entry(frame_yuv_histogram, textvariable=output_path_yuv_histogram, width=40).grid(row=1, column=1)
# tk.Button(frame_yuv_histogram, text="Seleccionar", command=lambda: select_output(output_path_yuv_histogram)).grid(row=1, column=2)

# tk.Button(frame_yuv_histogram, text="Generar Histograma YUV", command=generate_yuv_histogram).grid(row=2, columnspan=3)


# Frame para Convert Video
frame_convert = tk.LabelFrame(root, text="Convertir Video")
frame_convert.grid(row=2, column=0, padx=10, pady=10, sticky="w")
tk.Label(frame_convert, text="Input Path:").grid(row=0, column=0)
tk.Entry(frame_convert, textvariable=input_path_var, width=40).grid(row=0, column=1)
tk.Button(frame_convert, text="Seleccionar", command=lambda: select_file(input_path_var)).grid(row=0, column=2)
tk.Label(frame_convert, text="Output Path:").grid(row=1, column=0)
tk.Entry(frame_convert, textvariable=output_path_var, width=40).grid(row=1, column=1)
tk.Button(frame_convert, text="Seleccionar", command=lambda: select_output(output_path_var)).grid(row=1, column=2)
tk.Label(frame_convert, text="Códec:").grid(row=2, column=0)
tk.Entry(frame_convert, textvariable=codec_var).grid(row=2, column=1)
tk.Button(frame_convert, text="Convertir", command=convert_video).grid(row=3, columnspan=3)

# Frame para Modificar Audio
frame_modify_audio = tk.LabelFrame(root, text="Modificar Audio")
frame_modify_audio.grid(row=10, column=0, padx=10, pady=10, sticky="w")

input_path_audio = tk.StringVar()
output_path_audio = tk.StringVar()
audio_option_var = tk.StringVar()  # Esta variable puede ser para la opción de audio, como cambiar volumen, codec, etc.

tk.Label(frame_modify_audio, text="Input Path:").grid(row=0, column=0)
tk.Entry(frame_modify_audio, textvariable=input_path_audio, width=40).grid(row=0, column=1)
tk.Button(frame_modify_audio, text="Seleccionar", command=lambda: select_file(input_path_audio)).grid(row=0, column=2)

tk.Label(frame_modify_audio, text="Output Path:").grid(row=1, column=0)
tk.Entry(frame_modify_audio, textvariable=output_path_audio, width=40).grid(row=1, column=1)
tk.Button(frame_modify_audio, text="Seleccionar", command=lambda: select_output(output_path_audio)).grid(row=1, column=2)

tk.Label(frame_modify_audio, text="Opción de Audio:").grid(row=2, column=0)
tk.Entry(frame_modify_audio, textvariable=audio_option_var).grid(row=2, column=1)

tk.Button(frame_modify_audio, text="Modificar Audio", command=modify_audio).grid(row=3, columnspan=3)


# Ejecutar ventana principal
root.mainloop()
