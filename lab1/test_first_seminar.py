import unittest
import numpy as np
from firts_seminar import ex3, ex4, ex5, ex5_2, ex6, ex7
import os

imagen="C:\\Users\\Pocoyó\\OneDrive\\Imágenes\\MESSI.jpeg"
output='C:\\Users\\Pocoyó\\OneDrive\\Imágenes\\images_test.jpg'

class TestEx2(unittest.TestCase):
    def test_RGB_to_YUV(self):
        # Prueba de conversión de RGB a YUV
        r, g, b = 255, 128, 64
        y, u, v = ex2.RGB_to_YUV(r, g, b)
        
        # Verificamos valores aproximados
        self.assertAlmostEqual(y, 125.504, places=3)
        self.assertAlmostEqual(u, 143.226, places=3)
        self.assertAlmostEqual(v, 92.418, places=3)

    def test_YUV_to_RGB(self):
        # Prueba de conversión de YUV a RGB
        y, u, v = 125.5, 143.2, 92.4
        r, g, b = ex2.YUV_to_RGB(y, u, v)
        
        # Verificamos valores aproximados
        self.assertAlmostEqual(r, 255, delta=1)
        self.assertAlmostEqual(g, 128, delta=1)
        self.assertAlmostEqual(b, 64, delta=1)
    

class TestEx3(unittest.TestCase):
    def test_redimensionar_imagen(self):
        
        #Prueba de redimensionado de imagen
        ex3.redimensionar_imagen(imagen, output, 100, 100)
        self.assertTrue(os.path.exists(output))

        #Limpiar archivos, si quieres ver los resultados comentar esta linea
        os.remove(output)
        
class TestEx4(unittest.TestCase):
    def test_serpentine_diagonal(self):
        matrix = np.arange(1, 65).reshape(8, 8)
        result = ex4.serpentine_diagonal(matrix)
        
        #Comprobar la longitud de salida y verificar algunos valores
        self.assertEqual(len(result), 64)
        self.assertEqual(result[0], 1)
        self.assertEqual(result[-1], 64)

class TestEx5(unittest.TestCase):
    def test_convertir_bn_y_comprimir(self):
        output_path_ex5 = 'C:\\Users\\Pocoyó\\OneDrive\\Imágenes\\images_test5_BW.jpg'
        ex5.convertir_bn_y_comprimir(imagen, output_path_ex5)
        self.assertTrue(os.path.exists(output_path_ex5))
        
        #Limpiar archivos,si quieres ver los resultados comentar esta linea
        os.remove(output_path_ex5)
       
class TestEx5_2(unittest.TestCase):
    def test_run_length_encoding(self):
        data = [0, 1, 3, 6, 6, 6, 4, 4, 3, 7, 9]
        expected_result = [(1, 0), (1, 1), (1, 3), (3, 6), (2, 4), (1, 3), (1, 7), (1, 9)]
        result = ex5_2.run_length_encoding(data)
        self.assertEqual(result, expected_result)

class TestEx6(unittest.TestCase):
    def test_dct_idct(self):
        data = np.arange(1, 65).reshape(8, 8)
        
        #Aplicar DCT e IDCT
        result_dct = ex6.run_dct(data)
        result_idct = ex6.run_idct(result_dct)
        
        #Verificar que la IDCT devuelve la matriz original
        np.testing.assert_array_almost_equal(result_idct, data, decimal=6)

class TestEx7(unittest.TestCase):
    def test_dwt_idwt(self):
        data = np.arange(1, 65).reshape(8, 8)
        
        #Aplicar DWT e IDWT
        LL, LH, HL, HH = ex7.apply_dwt(data)
        reconstructed_data = ex7.apply_idwt(LL, LH, HL, HH)
        
        #Verificar que la IDWT devuelve la matriz original
        np.testing.assert_array_almost_equal(reconstructed_data, data, decimal=6)

if __name__ == '__main__':
    unittest.main()
