import subprocess
# task 3
from PIL import Image
class ex3:
    def redimensionar_imagen(input_path, output_path, width, height):
        command = [
            'ffmpeg', '-i', input_path,
            '-vf', f'scale={width}:{height}',
            output_path
        ]
        return output_path

#ex3.redimensionar_imagen(imagen,output,320,240)

# task4

class ex4:
    def serpentine_diagonal(matrix):
        rows = len(matrix)
        cols = len(matrix[0])
        result = []
        
        for diag in range(rows + cols - 1):
            if diag % 2 == 0:
                # Diagonal hacia abajo
                row = diag if diag < rows else rows - 1
                col = 0 if diag < rows else diag - (rows - 1)
                while row >= 0 and col < cols:
                    result.append(matrix[row][col])
                    row -= 1
                    col += 1
            else:
                # Diagonal hacia arriba
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

array([[ 1,2,3, 4, 5, 6, 7, 8],
       [ 9, 10, 11, 12, 13, 14,  15, 16],
       [ 17, 18, 19, 20,  21, 22, 23, 24],
       [ 25,  26,  27,  28,  29, 30, 31, 32],
       [33, 34, 35, 36,  37, 38,  39, 40],
       [ 41,42,43, 44, 45, 46, 47, 48],
       [ 49, 50, 51, 52, 53, 54, 55, 56],
       [ 57, 58, 59, 60, 61, 62, 63, 64]]) 



class ex5:
    def convertir_bn_y_comprimir(input_path, output_path):
        command = [
            'ffmpeg', '-i', input_path,  # Especifica el archivo de entrada
            '-vf', 'format=gray',        # Convierte a blanco y negro
            '-q:v', '31',                # Aplica la mayor compresión posible
            output_path                  # Especifica el archivo de salida
        ]
        
        # Ejecuta el comando FFmpeg
        subprocess.run(command, check=True)
        
        print(f"Imagen convertida a blanco y negro y comprimida guardada en {output_path}")
        return output_path


#input_image = 
#output_image = 
#convertir_bn_y_comprimir(input_image, output_image)

class ex6:
    def run_length_encoding(data):
        if not data:
            return []
        
        encoded_data = []
        current_byte = data[0]
        count = 1
        
        # Itera a través de la secuencia de bytes
        for byte in data[1:]:
            if byte == current_byte:
                # Si el byte es igual al actual, incrementa el contador
                count += 1
            else:
                # Si el byte es diferente, guarda el par (count, current_byte) y reinicia el contador
                encoded_data.append((count, current_byte))
                current_byte = byte
                count = 1
        
        # Agrega el último par (count, current_byte) al resultado
        encoded_data.append((count, current_byte))
        
        return encoded_data


            

