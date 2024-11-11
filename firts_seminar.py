import subprocess
import cv2
from scipy.fftpack import dct, idct
import numpy as np
import pywt


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

#ex3.redimensionar_imagen(imagen,output,320,240)

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

array = ([[ 1,2,3, 4, 5, 6, 7, 8],
       [ 9, 10, 11, 12, 13, 14,  15, 16],
       [ 17, 18, 19, 20,  21, 22, 23, 24],
       [ 25,  26,  27,  28,  29, 30, 31, 32],
       [33, 34, 35, 36,  37, 38,  39, 40],
       [ 41,42,43, 44, 45, 46, 47, 48],
       [ 49, 50, 51, 52, 53, 54, 55, 56],
       [ 57, 58, 59, 60, 61, 62, 63, 64]]) 


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


#input_image = "C:\\Users\\Pocoyó\\OneDrive\\Imágenes\\foto cv.jpg"
#output_image = "C:\\Users\\Pocoyó\\OneDrive\\Imágenes\\foto_cv_B&W.jpg"
#ex5.convertir_bn_y_comprimir(input_image, output_image)

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
            
#data = [0, 1, 3, 6, 6, 6, 4, 4, 3, 7, 9]
#encoded = ex5_2.run_length_encoding(data)
#print(encoded)

#TASK 6
class ex6:
     #lo hacemos por filas y por columnas
    def run_dct(data):
        return dct(dct(data, axis=0, norm='ortho'), axis=1, norm='ortho')
    def run_idct(data):
        return idct(idct(data, axis=0, norm='ortho'), axis=1, norm='ortho')

data = np.arange(1, 65).reshape(8, 8)
#result_dct = ex6.run_dct(data)
#result_idct = ex6.run_idct(result_dct)
#print(data)
#print(result_idct/256) #normalizamos

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
    
LL, LH, HL, HH = ex7.apply_dwt(data)
reconstructed_data = ex7.apply_idwt(LL, LH, HL, HH)

print('LL',LL)
print('LH',LH)
print('HL',HL)
print('HH',HH)
print("Matriz reconstruida después de IDWT:",reconstructed_data)

