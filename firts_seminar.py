import subprocess
import cv2
from scipy.fftpack import dct, idct
import numpy as np
import pywt


#TASK2 
class ex2:
    #creamos el metodo que pasa de RGB a YUV simplemente aplicamo sla formula de teoria
    def RGB_to_YUV(r, g, b):
        Y= 0.257*r+0.504*g+0.098*b+16
        U=-0.148*r-0.291*g+0.439 * b+128
        V=0.439*r-0.368*g-0.071 *b +128
        return Y,U,V
    #creamos el metodo para pasar de YUV a RGB siguiendo la formula de teoria
    def YUV_to_RGB(y,u,v):
        B=1.164*(y-16)+2.018*(u-128)
        G=1.164 * (y-16) - 0.813 * (v-128) - 0.391*(u-128)
        R=1.164*(y-16)+1.596*(v-128)
        return R,G,B
    
#TASK 3
from PIL import Image
class ex3:
    def redimensionar_imagen(input_path, output_path, width, height):
        command = [
            'ffmpeg', '-i', input_path,
            '-vf', f'scale={width}:{height}',
            output_path
        ]
        #comando para ejecutar ffmpeg
        subprocess.run(command, check=True)

        return output_path


#TASK 4

class ex4:
    def serpentine_diagonal(matrix):
        rows = len(matrix)
        cols = len(matrix[0])
        result = []
        
        for diag in range(rows + cols - 1):
            if diag % 2 == 0:
                #diagonal hacia abajo
                row = diag if diag < rows else rows - 1
                col = 0 if diag < rows else diag - (rows - 1)
                while row >= 0 and col < cols:
                    result.append(matrix[row][col])
                    row -= 1
                    col += 1
            else:
                #diagonal hacia arriba
                col = diag if diag < cols else cols - 1
                row = 0 if diag < cols else diag - (cols - 1)
                while col >= 0 and row < rows:
                    result.append(matrix[row][col])
                    row += 1
                    col -= 1             
        return result

def print_matrix(matrix, width=8):
    for i in range(0, len(matrix), width):
        print(matrix[i:i + width])

#TASK 5
class ex5:
    def convertir_bn_y_comprimir(input_path, output_path):
        command = [
            'ffmpeg', '-i', input_path,  #especifica el archivo de entrada
            '-vf', 'format=gray',        #convierte a blanco y negro
            '-q:v', '31',                #aplica la compresión que quieras, numero de compression = [2, 31], a mayor numero mas compresion y viceversa
            output_path                  #especifica el archivo de salida
        ]
        
        #ejecuta el comando FFmpeg
        subprocess.run(command, check=True)
        return output_path

#TASK 5_2
class ex5_2:
    def run_length_encoding(data):
        if not data:
            return []
        
        encoded_data = []
        current_byte = data[0]
        count = 1
        
        #itera a través de la secuencia de bytes
        for byte in data[1:]:
            if byte == current_byte:
                #si el byte es igual al actual, incrementa el contador
                count += 1
            else:
                #si el byte es diferente, guarda el par (count, current_byte) y reinicia el contador
                encoded_data.append((count, current_byte))
                current_byte = byte
                count = 1
        
        #agrega el último par (count, current_byte) al resultado
        encoded_data.append((count, current_byte))
        
        return encoded_data
            
#TASK 6
class ex6:
     #lo hacemos por filas y por columnas, normalizamos para que salga bien la inversa luego. 
    def run_dct(data):
        return dct(dct(data, axis=0, norm='ortho'), axis=1, norm='ortho')
    def run_idct(data):
        return idct(idct(data, axis=0, norm='ortho'), axis=1, norm='ortho')

#TASK 7
class ex7:
    #aplicamos la dwt a la array, con wavelet de tipo haar
    def apply_dwt(array):
        coeffs = pywt.dwt2(array, "haar")
        LL, (LH, HL, HH) = coeffs
        return LL, LH, HL, HH
    
    def apply_idwt(LL, LH, HL, HH):
        coeffs = LL, (LH, HL, HH)
        return pywt.idwt2(coeffs,"haar")
    