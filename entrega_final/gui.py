import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
from tkinter.ttk import Progressbar
import requests
import threading


class MonsterAPIGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Monster API NAGO & URI")
        self.root.geometry("800x600")

        # Estilo para mejorar la apariencia
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TButton", font=("Pacifico", 10, "bold"))
        self.style.configure("TLabel", font=("Pacifico", 10))
        
        # Estilo para botones de la pestaña de imágenes
        style = ttk.Style()
        style.configure("Image.TButton", font=("Pacifico", 10, "bold"), foreground="white", background="#004d98")  # Azul oscuro
        style.map("Image.TButton", background=[("active", "#5A9BD5")])  # Azul más claro al hacer clic

        # Estilo para botones de la pestaña de videos
        style.configure("Video.TButton", font=("Pacifico", 10, "bold"), foreground="white", background="#a50044")  # Rojo
        style.map("Video.TButton", background=[("active", "#D46A6A")])  # Rojo más claro al hacer clic

        # Estilo para botones de la pestaña de otras funcionalidades
        style.configure("Misc.TButton", font=("Pacifico", 10, "bold"), foreground="black", background="#edbb00")  # Amarillo
        style.map("Misc.TButton", background=[("active", "#FFEC8B")])  # Amarillo más claro al hacer clic

        
        # Notebook para organizar pestañas
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill="both")

        # Pestañas
        self.create_image_tab()
        self.create_video_tab()
        self.create_other_tab()

    def send_request_with_progress(self, endpoint, data):
        """Envía una solicitud y muestra una barra de progreso mientras se procesa."""
        progress = Progressbar(self.root, orient="horizontal", mode="indeterminate", length=300)
        progress.pack(pady=10)
        progress.start()  # Inicia la animación de la barra de progreso

        # Enviar la solicitud en un hilo separado para no bloquear la interfaz
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
    
    def create_image_tab(self):
        """Crea la pestaña de procesamiento de imágenes."""
        self.image_tab = tk.Frame(self.notebook, bg="#ADD8E6") 
        self.notebook.add(self.image_tab, text="Procesar Imágenes")

        ttk.Button(self.image_tab, text="Convertir RGB a YUV",style="Image.TButton", command=self.convert_rgb_to_yuv).pack(pady=5)
        ttk.Button(self.image_tab, text="Redimensionar Imagen", style="Image.TButton",command=self.resize_image).pack(pady=5)
        ttk.Button(self.image_tab, text="Convertir a Blanco y Negro y Comprimir",style="Image.TButton", command=self.convert_bw_compress).pack(pady=5)

    def create_video_tab(self):
        """Crea la pestaña de procesamiento de videos."""
        self.video_tab = tk.Frame(self.notebook, bg="#FFCCCB")  
        self.notebook.add(self.video_tab, text="Procesar Videos")

        ttk.Button(self.video_tab, text="Redimensionar Video",style="Video.TButton", command=self.resize_video).pack(pady=5)
        ttk.Button(self.video_tab, text="Modificar Chroma Subsampling",style="Video.TButton", command=self.modify_chroma_subsampling).pack(pady=5)
        ttk.Button(self.video_tab, text="Información del Video",style="Video.TButton", command=self.get_video_info).pack(pady=5)
        ttk.Button(self.video_tab, text="Procesar Video Completo",style="Video.TButton", command=self.process_video).pack(pady=5)
        ttk.Button(self.video_tab, text="Contar Tracks",style="Video.TButton", command=self.count_tracks).pack(pady=5)
        ttk.Button(self.video_tab, text="Generar Motion Vectors",style="Video.TButton", command=self.generate_motion_vectors).pack(pady=5)

    def create_other_tab(self):
        """Crea la pestaña de otras funcionalidades."""
        self.misc_tab = tk.Frame(self.notebook, bg="#FFFF9E")
        self.notebook.add(self.misc_tab, text="Otras Funcionalidades")

        ttk.Button(self.misc_tab, text="Generar Histograma YUV", style="Misc.TButton",command=self.generate_yuv_histogram).pack(pady=5)
        ttk.Button(self.misc_tab, text="Convertir Video a Códec",style="Misc.TButton", command=self.convert_video).pack(pady=5)
        ttk.Button(self.misc_tab, text="Modificar Audio",style="Misc.TButton", command=self.modify_audio).pack(pady=5)

    # Funciones auxiliares para seleccionar archivos
    def select_file(self):
        return filedialog.askopenfilename()

    def save_file(self):
        return filedialog.asksaveasfilename()

    # Funcionalidades (endpoints de la API)
    def convert_rgb_to_yuv(self):
        r = simpledialog.askinteger("Input", "Valor R (0-255):")
        g = simpledialog.askinteger("Input", "Valor G (0-255):")
        b = simpledialog.askinteger("Input", "Valor B (0-255):")
        data = {"r": r, "g": g, "b": b}
        self.send_request_with_progress("convertir_rgb_a_yuv/", data)

    def resize_image(self):
        input_path = self.select_file()
        output_path = self.save_file()
        width = simpledialog.askinteger("Input", "Ancho:")
        height = simpledialog.askinteger("Input", "Alto:")
        data = {"input_path": input_path, "output_path": output_path, "width": width, "height": height}
        self.send_request_with_progress("resize_image/", data)

    def convert_bw_compress(self):
        input_path = self.select_file()
        output_path = self.save_file()
        width = simpledialog.askinteger("Input", "Ancho:")
        height = simpledialog.askinteger("Input", "Alto:")
        data = {"input_path": input_path, "output_path": output_path, "width": width, "height": height}
        self.send_request_with_progress("convertir_bn_y_comprimir/", data)

    def resize_video(self):
        input_path = self.select_file()
        output_path = self.save_file()
        width = simpledialog.askinteger("Input", "Ancho:")
        height = simpledialog.askinteger("Input", "Alto:")
        data = {"input_path": input_path, "output_path": output_path, "width": width, "height": height}
        self.send_request_with_progress("resize_video/", data)

    def modify_chroma_subsampling(self):
        input_path = self.select_file()
        output_path = self.save_file()
        subsampling = simpledialog.askstring("Input", "Chroma Subsampling (e.g., yuv420p):")
        data = {"input_path": input_path, "output_path": output_path, "subsampling": subsampling}
        self.send_request_with_progress("modify_chroma_subsampling/", data)

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

    def count_tracks(self):
        input_path = self.select_file()
        data = {"input_path": input_path}
        self.send_request_with_progress("count_tracks/", data)

    def generate_motion_vectors(self):
        input_path = self.select_file()
        output_path = self.save_file()
        data = {"input_path": input_path, "output_path": output_path}
        self.send_request_with_progress("generate_motion_vectors/", data)

    def generate_yuv_histogram(self):
        input_path = self.select_file()
        output_path = self.save_file()
        data = {"input_path": input_path, "output_path": output_path}
        self.send_request_with_progress("generate_yuv_histogram/", data)

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
