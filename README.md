
# **FastAPI Image Processing API**

## **Descripción**

Este proyecto proporciona una API construida con **FastAPI** que permite realizar varias operaciones de procesamiento de imágenes y conversiones de color. Está diseñado para ser ejecutado en un contenedor **Docker**, lo que facilita su implementación y despliegue en cualquier entorno. 

Los principales servicios de la API incluyen:

- Conversión de colores RGB a YUV.
- Redimensionamiento de imágenes.
- Conversión de imágenes a blanco y negro y compresión.
- Subida de imágenes para su procesamiento.

## **Estructura del Proyecto**

```
/app
    /images                    # Carpeta para almacenar las imágenes subidas y procesadas
    main.py                    # Archivo principal de la API FastAPI
    Dockerfile                 # Archivo Docker para crear la imagen del contenedor
    requirements.txt           # Dependencias necesarias para ejecutar la API
```

- **main.py**: Define los endpoints de la API utilizando FastAPI.
- **Dockerfile**: Contiene las instrucciones necesarias para construir la imagen Docker.
- **requirements.txt**: Lista las dependencias necesarias para la API, como FastAPI y Uvicorn.

## **Requisitos previos**

Asegúrate de tener los siguientes requisitos previos instalados en tu máquina:

- **Docker**: Para contenerizar la aplicación y facilitar su despliegue.
- **Python 3.9 o superior**: Si prefieres ejecutar la API localmente sin Docker.
- **FastAPI**: Framework para crear APIs rápidas y fáciles de usar.
- **Uvicorn**: Servidor ASGI para ejecutar aplicaciones FastAPI.

## **Cómo ejecutar el proyecto**

### **1. Clonar el repositorio**

Primero, clona este repositorio en tu máquina local:

```bash
git clone https://github.com/tu-usuario/tu-repositorio.git
```

### **2. Construir la imagen Docker**

En el directorio raíz del proyecto, construye la imagen Docker ejecutando el siguiente comando:

```bash
docker build -t fastapi-image-processing .
```

Este comando construirá la imagen de Docker con el nombre `fastapi-image-processing`.

### **3. Ejecutar el contenedor Docker**

Una vez que la imagen esté construida, puedes ejecutar el contenedor con el siguiente comando:

```bash
docker run -d -p 8000:8000 --name fastapi-container fastapi-image-processing
```

Esto ejecutará el contenedor y expondrá la API en el puerto 8000 de tu localhost. Podrás acceder a la API en **`http://localhost:8000`**.

### **4. Usar la API**

La API estará disponible en **`http://localhost:8000`**. Puedes acceder a la documentación interactiva de la API proporcionada por FastAPI en **`http://localhost:8000/docs`**.

## **Endpoints de la API**

### 1. **Conversión RGB a YUV**

- **Método**: `POST`
- **Endpoint**: `/rgb_to_yuv/`
- **Descripción**: Convierte valores RGB (Rojo, Verde, Azul) a sus correspondientes valores YUV.
- **Entrada**:
    ```json
    {
      "r": 255,
      "g": 0,
      "b": 0
    }
    ```
- **Salida**:
    ```json
    {
      "Y": 76,
      "U": 85,
      "V": 255
    }
    ```

### 2. **Redimensionar Imagen**

- **Método**: `POST`
- **Endpoint**: `/resize_image/`
- **Descripción**: Redimensiona una imagen a las dimensiones proporcionadas.
- **Entrada**:
    ```json
    {
      "input_path": "/app/images/input.jpg",
      "output_path": "/app/images/output.jpg",
      "width": 300,
      "height": 200
    }
    ```
- **Salida**:
    ```json
    {
      "output_path": "/app/images/output.jpg"
    }
    ```

### 3. **Convertir a Blanco y Negro y Comprimir**

- **Método**: `POST`
- **Endpoint**: `/convertir_bn_y_comprimir/`
- **Descripción**: Convierte una imagen a blanco y negro y la comprime.
- **Entrada**:
    ```json
    {
      "input_path": "/app/images/input.jpg",
      "output_path": "/app/images/output_compressed.jpg"
    }
    ```
- **Salida**:
    ```json
    {
      "output_path": "/app/images/output_compressed.jpg"
    }
    ```

### 4. **Subir una Imagen**

- **Método**: `POST`
- **Endpoint**: `/upload-photo/`
- **Descripción**: Permite cargar una imagen desde tu máquina local al servidor para su procesamiento.
- **Entrada**: La imagen se sube como archivo, no como JSON.
- **Salida**:
    ```json
    {
      "message": "Photo uploaded successfully",
      "file_path": "/app/images/uploaded_image.jpg"
    }
    ```

## **Cómo interactuar con la API**

- Puedes interactuar con la API utilizando herramientas como **Postman** o **Insomnia** para hacer solicitudes `POST`.
- Para los endpoints de carga de imágenes y redimensionado, asegúrate de enviar las solicitudes con los datos correctos, como la ruta de la imagen y las nuevas dimensiones (en el caso de redimensionamiento).

## **Configuración y Personalización**

- **Imágenes de Entrada**: Las imágenes cargadas o procesadas se guardarán en la carpeta `/app/images/` dentro del contenedor Docker.
- **Configuración de Docker**: Asegúrate de que Docker esté correctamente configurado para acceder a las imágenes locales y que el contenedor tenga permisos de escritura en las carpetas necesarias.

## **Dependencias**

Este proyecto depende de las siguientes bibliotecas y herramientas:

- **fastapi**: Framework web para crear APIs.
- **uvicorn**: Servidor ASGI para ejecutar aplicaciones FastAPI.
- **shutil**: Biblioteca estándar de Python para operaciones con archivos y directorios.
  
Las dependencias están listadas en el archivo `requirements.txt`.

## **Conclusión**

Este proyecto te permite realizar varias operaciones de procesamiento de imágenes y conversiones de color a través de una API construida con **FastAPI**. Utilizando Docker, puedes ejecutar y desplegar la API de manera eficiente en cualquier entorno. Además, la API permite subir imágenes, redimensionarlas y aplicar diversas transformaciones.
