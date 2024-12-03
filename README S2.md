
# Video Processing API

Esta es una API desarrollada en Python utilizando FastAPI para procesar y analizar videos mediante la biblioteca FFmpeg. Ofrece múltiples endpoints para redimensionar videos, modificar propiedades, extraer información y generar archivos transformados.

## Funcionalidades

### 1. Redimensionar un Video
**Endpoint**: `/resize_video/`  
Permite redimensionar un video a una resolución específica. Se utiliza FFmpeg para escalar la altura y anchura según lo solicitado.

- **Entrada**:
  ```json
  {
    "input_path": "ruta_del_video_entrada",
    "output_path": "ruta_del_video_salida",
    "width": 1280,
    "height": 720
  }
  ```
- **Salida**: Mensaje de éxito y ruta del archivo redimensionado.

---

### 2. Modificar Chroma Subsampling
**Endpoint**: `/modify_chroma_subsampling/`  
Cambia el formato de muestreo de croma (chroma subsampling) de un video. Útil para modificar la representación de colores.

- **Entrada**:
  ```json
  {
    "input_path": "ruta_del_video_entrada",
    "output_path": "ruta_del_video_salida",
    "subsampling": "pix_fmt_deseado" 
  }
  ```
- **Salida**: Mensaje de éxito y ruta del archivo transformado.

---

### 3. Obtener Información del Video
**Endpoint**: `/get_video_info/`  
Extrae información relevante de un video como formato, resolución, duración, tasa de bits, códec y fotogramas por segundo.

- **Entrada**:
  ```json
  {
    "input_path": "ruta_del_video_entrada"
  }
  ```
- **Salida**:
  ```json
  {
    "video_info": {
      "format_name": "mp4",
      "duration": 120.5,
      "bit_rate": 1000000,
      "resolution": "1920x1080",
      "codec_name": "h264",
      "frame_rate": 30
    }
  }
  ```

---

### 4. Procesamiento Completo de Video
**Endpoint**: `/process_video/`  
Realiza un conjunto de transformaciones sobre un video, incluyendo:
1. Cortar a los primeros 20 segundos.
2. Extraer audio en diferentes formatos: AAC, MP3 y AC3.
3. Empaquetar video y audio en un archivo final MP4.

- **Entrada**:
  ```json
  {
    "input_path": "ruta_del_video_entrada",
    "output_video_path": "ruta_del_video_cortado",
    "output_audio_aac": "ruta_del_audio_aac",
    "output_audio_mp3": "ruta_del_audio_mp3",
    "output_audio_ac3": "ruta_del_audio_ac3",
    "final_output_path": "ruta_del_video_final"
  }
  ```
- **Salida**: Mensaje de éxito y ruta del archivo final.

---

### 5. Contar Tracks de Video, Audio y Subtítulos
**Endpoint**: `/count_tracks/`  
Cuenta el número de pistas de video, audio y subtítulos en un archivo multimedia.

- **Entrada**:
  ```json
  {
    "input_path": "ruta_del_archivo_multimedia"
  }
  ```
- **Salida**:
  ```json
  {
    "total_tracks": 5,
    "video_tracks": 1,
    "audio_tracks": 3,
    "subtitle_tracks": 1
  }
  ```

---

### 6. Generar Macroblocks y Motion Vectors
**Endpoint**: `/generate_motion_vectors/`  
Genera un archivo de video con macroblocks y vectores de movimiento visibles, útil para análisis visual de la compresión del video.

- **Entrada**:
  ```json
  {
    "input_path": "ruta_del_video_entrada",
    "output_path": "ruta_del_video_salida"
  }
  ```
- **Salida**: Mensaje de éxito y ruta del video generado.

---

### 7. Generar Histograma YUV
**Endpoint**: `/generate_yuv_histogram/`  
Genera un histograma YUV sobre un video, que muestra la distribución de luminancia y crominancia.

- **Entrada**:
  ```json
  {
    "input_path": "ruta_del_video_entrada",
    "output_path": "ruta_del_video_con_histograma"
  }
  ```
- **Salida**: Mensaje de éxito y ruta del video generado.

---