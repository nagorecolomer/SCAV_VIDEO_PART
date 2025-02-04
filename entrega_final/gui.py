import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
from tkinter.ttk import Progressbar
import requests
import threading


class MonsterAPIGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Monster API Nago & URI")
        self.root.geometry("800x600")

        #Estilo para mejorar la apariencia
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TButton", font=("Pacifico", 10, "bold"))
        self.style.configure("TLabel", font=("Pacifico", 10))
        
        #Mensaje inicial de la GUI (get del main)
        self.show_initial_message()
        
        #Estilo para botones de la pestaña de imágenes
        style = ttk.Style()

        #Estilo para botones de la pestaña de videos
        style.configure("Video.TButton", font=("Pacifico", 10, "bold"), foreground="white", background="#a50044")  # Rojo
        style.map("Video.TButton", background=[("active", "#D46A6A")])  # Rojo más claro al hacer clic      

        
        #Notebook para organizar pestañas
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill="both")

        #Pestañas
        self.create_video_tab()

    def send_request_with_progress(self, endpoint, data):
        """Envía una solicitud y muestra una barra de progreso mientras se procesa."""
        progress = Progressbar(self.root, orient="horizontal", mode="indeterminate", length=300)
        progress.pack(pady=10)
        progress.start()  #Inicia la animación de la barra de progreso

        #Enviar la solicitud en un hilo separado para no bloquear la interfaz
        threading.Thread(target=self.send_request, args=(endpoint, data, progress)).start()

    def send_request(self, endpoint, data, progress):
        """Envía la solicitud HTTP y maneja la respuesta."""
        try:
            url = f"http://127.0.0.1:8000/{endpoint}"
            response = requests.post(url, json=data)
            response.raise_for_status()
            messagebox.showinfo("Éxito", response.json())
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", str(e))
        finally:
            progress.stop()  # Detener la barra de progreso
            progress.destroy()  # Eliminar la barra de progreso de la interfaz
    
    def show_initial_message(self):
        try:
            url = "http://127.0.0.1:8000/"  
            response = requests.get(url)
            response.raise_for_status()
            mensaje = response.json().get("mensaje", "¡Bienvenido a Monster API GUI!")
            messagebox.showinfo("Mensaje Inicial", mensaje)
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"No se pudo obtener el mensaje inicial: {str(e)}")

    

    def create_video_tab(self):
        """Crea la pestaña de procesamiento de videos."""
        self.video_tab = tk.Frame(self.notebook, bg="#FFCCCB")  
        self.notebook.add(self.video_tab, text="Procesar Videos")

        ttk.Button(self.video_tab, text="Redimensionar Video",style="Video.TButton", command=self.resize_video).pack(pady=5)
        ttk.Button(self.video_tab, text="Información del Video",style="Video.TButton", command=self.get_video_info).pack(pady=5)
        ttk.Button(self.video_tab, text="Procesar Video Completo",style="Video.TButton", command=self.process_video).pack(pady=5)
        ttk.Button(self.video_tab, text="Convertir Video a Códec",style="Video.TButton", command=self.convert_video).pack(pady=5)
        ttk.Button(self.video_tab, text="Modificar Audio",style="Video.TButton", command=self.modify_audio).pack(pady=5)
   
        

    # Funciones auxiliares para seleccionar archivos
    def select_file(self):
        return filedialog.askopenfilename()

    def save_file(self):
        return filedialog.asksaveasfilename()

    # Funcionalidades (endpoints de la API)
    def resize_video(self):
        input_path = self.select_file()
        output_path = self.save_file()
        width = simpledialog.askinteger("Input", "Ancho:")
        height = simpledialog.askinteger("Input", "Alto:")
        data = {"input_path": input_path, "output_path": output_path, "width": width, "height": height}
        self.send_request_with_progress("resize_video/", data)


    def get_video_info(self):
        input_path = self.select_file()
        data = {"input_path": input_path}
        self.send_request_with_progress("get_video_info/", data)

    def process_video(self):
        input_path = self.select_file()
        output_video_path = self.save_file()
        output_audio_aac = self.save_file()
        output_audio_mp3 = self.save_file()
        output_audio_ac3 = self.save_file()
        final_output_path = self.save_file()
        data = {
            "input_path": input_path,
            "output_video_path": output_video_path,
            "output_audio_aac": output_audio_aac,
            "output_audio_mp3": output_audio_mp3,
            "output_audio_ac3": output_audio_ac3,
            "final_output_path": final_output_path
        }
        self.send_request_with_progress("process_video/", data)


    def convert_video(self):
        input_path = self.select_file()
        output_path = self.save_file()
        codec = simpledialog.askstring("Input", "Codec (vp8, vp9, h265, av1):")
        data = {"input_path": input_path, "output_path": output_path, "codec": codec}
        self.send_request_with_progress("convert_video/", data)

    def modify_audio(self):
        input_path = self.select_file()
        output_audio_path = self.save_file()
        audio_bitrate = simpledialog.askstring("Input", "Audio Bitrate (e.g., 128k):")
        audio_channels = simpledialog.askinteger("Input", "Número de Canales (1 para mono, 2 para estéreo):")
        audio_format = simpledialog.askstring("Input", "Formato de Audio (e.g., aac, mp3, wav):")
        data = {
            "input_path": input_path,
            "output_audio_path": output_audio_path,
            "audio_bitrate": audio_bitrate,
            "audio_channels": audio_channels,
            "audio_format": audio_format
        }
        self.send_request_with_progress("modify_audio/", data)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    gui = MonsterAPIGUI()
    gui.run()
