import tkinter as tk
from tkinter import filedialog, messagebox
import requests

#hemos utilizado tkinter porque nos ha parecido el mas facil y practico para este trabajoq de
def select_file():
    file_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4;*.mkv")])
    if file_path:
        input_path_var.set(file_path)

def process_video():
    input_path = input_path_var.get()
    codec = codec_var.get()
    output_path = output_path_var.get()
    
    if not input_path or not codec or not output_path:
        messagebox.showerror("Error", "Por favor, completa todos los campos.")
        return

    data = {
        "input_path": input_path,
        "output_path": output_path,
        "codec": codec
    }

    try:
        response = requests.post("http://127.0.0.1:8000/convert_video/", json=data)
        if response.status_code == 200:
            messagebox.showinfo("Éxito", f"Video procesado: {response.json()['output_path']}")
        else:
            messagebox.showerror("Error", response.json().get("detail", "Error desconocido"))
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Crear ventana principal
root = tk.Tk()
root.title("Monster API - Video Processing")

# Variables de entrada
input_path_var = tk.StringVar()
output_path_var = tk.StringVar()
codec_var = tk.StringVar()

# Campos de entrada
tk.Label(root, text="Ruta del Video:").grid(row=0, column=0, sticky="e")
tk.Entry(root, textvariable=input_path_var, width=40).grid(row=0, column=1)
tk.Button(root, text="Seleccionar Archivo", command=select_file).grid(row=0, column=2)

tk.Label(root, text="Códec:").grid(row=1, column=0, sticky="e")
tk.Entry(root, textvariable=codec_var, width=40).grid(row=1, column=1)

tk.Label(root, text="Ruta de Salida:").grid(row=2, column=0, sticky="e")
tk.Entry(root, textvariable=output_path_var, width=40).grid(row=2, column=1)

# Botón para procesar
tk.Button(root, text="Procesar Video", command=process_video).grid(row=3, column=1, pady=10)

# Ejecutar ventana
root.mainloop()
