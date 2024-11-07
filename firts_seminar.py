import ffmpeg 

class ex2:
    #Creamos el metodo que pasa de RGB a YUV simplemente aplicamo sla formula de teoria
    def RGB_to_YUV(r, g, b):
        Y= 0.257*r+0.504*g+0.098*b+16
        U=-0.148*r-0.291*g+0.439 * b+128
        V=0.439*r-0.368*g-0.071 *b +128
        return Y,U,V
    #Creamos el metodo para pasar de YUV a RGB siguiendo la formula de teoria
    def YUV_to_RGB(y,u,v):
        B=1.164*(y-16)+2.018*(u-128)
        G=1.164 * (y-16) - 0.813 * (v-128) - 0.391*(u-128)
        R=1.164*(y-16)+1.596*(v-128)
        return R,G,B
    

#ex3: resize
import subprocess
import os

def redimensionar_imagen(input_image, output_image, width, height, quality):
       # Construir el comando de FFmpeg
    command = [
        'ffmpeg',  # Llamamos a FFmpeg
        '-i', input_image,  # Imagen original
        '-vf', f"scale={width}:{height}",  # Redimensionar
        '-q:v', str(quality),  # Reducir calidad
        output_image  # Nombre de la imagen de salida
    ]
    
    # Ejecutar el comando
    subprocess.run(command)

# Lista de imágenes a procesar
imagenes = ["C:\\Users\\34622\\OneDrive\\Escritorio\\Barcelona-logo-escudo.png", 'imagen2.jpg', 'imagen3.jpg']
# Parámetros de redimensionamiento
ancho = 800
alto = 600
calidad = 10  # Calidad de la imagen (1-31)

for imagen in imagenes:
    output_image = f"resized_{os.path.basename(imagen)}"
    redimensionar_imagen(imagen, output_image, ancho, alto, calidad)


