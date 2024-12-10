
# Monster API GUI

## Descripción

**Monster API GUI** es una interfaz gráfica creada con Python utilizando `tkinter` para interactuar con una API REST que procesa imágenes y videos. La interfaz permite al usuario ejecutar diversas funciones sobre archivos multimedia como imágenes y videos, incluyendo tareas como redimensionamiento, conversión a otros formatos, y manipulación de audio y video.

La aplicación está dividida en varias pestañas para organizar las funcionalidades:
- **Procesar Imágenes**: Herramientas para convertir y redimensionar imágenes.
- **Procesar Videos**: Funciones para modificar videos y sus características.
- **Otras Funcionalidades**: Opciones adicionales para trabajar con histograma YUV, modificar audio y convertir videos a diferentes códecs.

## Requisitos

Para ejecutar la aplicación, necesitas tener instalado Python y algunas bibliotecas. Puedes instalar las dependencias con `pip`:

```bash
pip install tkinter requests
```

## Instalación y Ejecución

1. Clona este repositorio a tu máquina local:

   ```bash
   git clone https://github.com/tu_usuario/monster_api_gui.git
   ```

2. Navega a la carpeta del proyecto:

   ```bash
   cd monster_api_gui
   ```

3. Ejecuta el archivo `main.py` para iniciar la GUI:

   ```bash
   python main.py
   ```

## Estructura del Proyecto

La estructura de archivos es la siguiente:

```
monster_api_gui/
│
├── README.md            # Este archivo con la documentación
├── main.py              # Código principal de la GUI
└── documents/           # Documentos relacionados, como la especificación de la API, etc.
```

## Uso de la GUI

### Interfaz Gráfica

La GUI está organizada en pestañas utilizando el widget `Notebook` de `tkinter`. Cada pestaña tiene botones que ejecutan las funciones correspondientes. A continuación, se detallan las funcionalidades y la interacción del usuario con la interfaz:

### Pestañas

1. **Procesar Imágenes**:
    - **Convertir RGB a YUV**: Convierte valores RGB a YUV. Se te solicitarán tres valores (R, G, B) entre 0 y 255.
    - **Redimensionar Imagen**: Permite seleccionar una imagen y redimensionarla con un nuevo ancho y alto. La imagen redimensionada se guarda en la ruta seleccionada.
    - **Convertir a Blanco y Negro y Comprimir**: Convierte una imagen a blanco y negro y la comprime. La imagen resultante se guarda en el archivo seleccionado.

2. **Procesar Videos**:
    - **Redimensionar Video**: Redimensiona un video a las dimensiones especificadas por el usuario. Al igual que con las imágenes, se seleccionan los archivos de entrada y salida.
    - **Modificar Chroma Subsampling**: Permite cambiar el subsampling de croma en un video.
    - **Información del Video**: Muestra información sobre el video seleccionado.
    - **Procesar Video Completo**: Este botón requiere que selecciones varios archivos para guardar los resultados del procesamiento:
        - Se te pedirá un archivo de entrada (video).
        - Se te pedirá seleccionar múltiples archivos de salida para el video procesado, así como para los distintos formatos de audio extraídos (AAC, MP3, AC3).
        - El resultado final se guarda en la ruta que determines.
    - **Contar Tracks**: Cuenta los tracks de un video.
    - **Generar Motion Vectors**: Genera vectores de movimiento a partir de un video seleccionado.

3. **Otras Funcionalidades**:
    - **Generar Histograma YUV**: Permite generar un histograma de una imagen o video en el formato YUV.
    - **Convertir Video a Códec**: Convierte un video a un códec especificado (por ejemplo, VP8, H265, AV1).
    - **Modificar Audio**: Modifica el audio de un video, permitiendo cambiar la tasa de bits, el número de canales (mono o estéreo) y el formato de audio (AAC, MP3, WAV).

### Barra de Progreso

En las operaciones que implican procesamiento de archivos, como el redimensionamiento de imágenes o videos, se muestra una barra de progreso para indicar que la operación está en curso. Esta barra aparece cuando se inicia el procesamiento y desaparece una vez que la tarea se ha completado. La barra de progreso es **indeterminada** y está animada, lo que significa que solo muestra que el proceso está en marcha pero no indica el porcentaje exacto de progreso.

### Función de "Procesar Video Completo"

Cuando se selecciona la opción de **Procesar Video Completo**, verás tres ventanas emergentes donde debes seleccionar archivos:
1. **Archivo de Video de Entrada**: El archivo de video original que será procesado.
2. **Archivos de Audio**: Cuatro rutas para guardar el audio extraído del video en diferentes formatos: AAC, MP3 y AC3.
3. **Ruta de Video Final**: El archivo de video procesado que será guardado al final.

Este es un paso necesario para asegurar que todos los archivos resultantes se guarden en las ubicaciones adecuadas. Debes seleccionar los archivos que corresponden para cada uno de los formatos solicitados.

### Personalización de la Interfaz

- **Colores de las Pestañas y Botones**: 
    - La pestaña de **Procesar Imágenes** tiene un fondo azul claro (`#ADD8E6`).
    - La pestaña de **Procesar Videos** tiene un fondo rojo claro (`#FFCCCB`).
    - La pestaña de **Otras Funcionalidades** tiene un fondo amarillo claro (`#FFFF9E`).
    - Los botones dentro de cada pestaña tienen colores personalizados para mejorar la experiencia de usuario.

## Contribuciones

Si deseas contribuir a este proyecto, por favor sigue estos pasos:

1. Fork este repositorio.
2. Crea una nueva rama (`git checkout -b feature-nueva-funcionalidad`).
3. Realiza tus cambios y haz commit (`git commit -am 'Añadir nueva funcionalidad'`).
4. Empuja tus cambios a tu repositorio fork (`git push origin feature-nueva-funcionalidad`).
5. Abre un pull request.

## Licencia

Este proyecto está bajo la licencia MIT. Consulta el archivo [LICENSE](LICENSE) para más detalles.

---

¡Esperamos que disfrutes usando **Monster API GUI** y que te sea útil en tus tareas de procesamiento de imágenes y videos!
