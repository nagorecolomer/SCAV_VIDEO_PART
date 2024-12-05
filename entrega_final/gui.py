import tkinter as tk
from tkinter import filedialog, messagebox
import requests

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
def rgb_to_yuv():
    try:
        r, g, b = int(r_var.get()), int(g_var.get()), int(b_var.get())
        response = requests.post(f"{API_URL}/rgb_to_yuv/", json={"r": r, "g": g, "b": b})
        result = response.json()
        if "error" in result:
            messagebox.showerror("Error", result["error"])
        else:
            messagebox.showinfo("Resultado", f"Y: {result['Y']}, U: {result['U']}, V: {result['V']}")
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

def modify_chroma_subsampling():
    try:
        data = {
            "input_path": input_path_var.get(),
            "output_path": output_path_var.get(),
            "subsampling": codec_var.get()  # Usamos el mismo campo que para códec
        }
        response = requests.post(f"{API_URL}/modify_chroma_subsampling/", json=data)
        result = response.json()
        if "error" in result:
            messagebox.showerror("Error", result["error"])
        else:
            messagebox.showinfo("Éxito", f"Submuestreo de croma modificado: {result['output_path']}")
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

# Frame para RGB to YUV
frame_rgb = tk.LabelFrame(root, text="RGB to YUV")
frame_rgb.grid(row=0, column=0, padx=10, pady=10, sticky="w")
tk.Label(frame_rgb, text="R:").grid(row=0, column=0)
tk.Entry(frame_rgb, textvariable=r_var).grid(row=0, column=1)
tk.Label(frame_rgb, text="G:").grid(row=1, column=0)
tk.Entry(frame_rgb, textvariable=g_var).grid(row=1, column=1)
tk.Label(frame_rgb, text="B:").grid(row=2, column=0)
tk.Entry(frame_rgb, textvariable=b_var).grid(row=2, column=1)
tk.Button(frame_rgb, text="Convertir", command=rgb_to_yuv).grid(row=3, columnspan=2)

# Frame para Resize Video
frame_resize = tk.LabelFrame(root, text="Redimensionar Video")
frame_resize.grid(row=1, column=0, padx=10, pady=10, sticky="w")
tk.Label(frame_resize, text="Input Path:").grid(row=0, column=0)
tk.Entry(frame_resize, textvariable=input_path_var, width=40).grid(row=0, column=1)
tk.Button(frame_resize, text="Seleccionar", command=lambda: select_file(input_path_var)).grid(row=0, column=2)
tk.Label(frame_resize, text="Output Path:").grid(row=1, column=0)
tk.Entry(frame_resize, textvariable=output_path_var, width=40).grid(row=1, column=1)
tk.Button(frame_resize, text="Seleccionar", command=lambda: select_output(output_path_var)).grid(row=1, column=2)
tk.Label(frame_resize, text="Width:").grid(row=2, column=0)
tk.Entry(frame_resize, textvariable=width_var).grid(row=2, column=1)
tk.Label(frame_resize, text="Height:").grid(row=3, column=0)
tk.Entry(frame_resize, textvariable=height_var).grid(row=3, column=1)
tk.Button(frame_resize, text="Redimensionar", command=resize_video).grid(row=4, columnspan=3)

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

# Frame para Información del Video
frame_info = tk.LabelFrame(root, text="Información del Video")
frame_info.grid(row=3, column=0, padx=10, pady=10, sticky="w")
tk.Label(frame_info, text="Input Path:").grid(row=0, column=0)
tk.Entry(frame_info, textvariable=input_path_var, width=40).grid(row=0, column=1)
tk.Button(frame_info, text="Seleccionar", command=lambda: select_file(input_path_var)).grid(row=0, column=2)
tk.Button(frame_info, text="Obtener Información", command=get_video_info).grid(row=1, columnspan=3)

# Ejecutar ventana principal
root.mainloop()
