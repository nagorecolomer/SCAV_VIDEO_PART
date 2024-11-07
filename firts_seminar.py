#import subprocess
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

array([[ 4, 19,  4, 18, 10, 19, 15, 19],
       [ 3, 10, 20, 16, 10, 17,  4,  5],
       [ 4, 19, 19,  5,  2, 18,  3,  8],
       [ 1,  4,  9,  8,  9,  8,  7,  9],
       [14,  2, 20, 11,  6, 19,  4,  6],
       [ 4,  3,  5,  8,  4,  9, 16, 20],
       [ 8, 16,  8,  4,  6, 16, 17,  3],
       [ 0,  9, 14, 20, 14, 14,  0, 16]]) 

###pruebas de si puedo hacer cambios
