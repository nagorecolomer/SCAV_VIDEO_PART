En el archivo de first_seminar podemos encontrar las funciones que se nos pide en cada ejercicio con su definicion, 
a continuacion explicamos una a una un poco por encima. 

TASK 3: Redimensionar imágenes (ex3.redimensionar_imagen)
Esta función utiliza FFmpeg para redimensionar una imagen a dimensiones específicas de ancho y alto.
Parámetros:
- input_path: Ruta del archivo de imagen de entrada.
- output_path: Ruta donde se guardará la imagen redimensionada.
- width, height: Dimensiones de la nueva imagen.
Retorno: La ruta de salida de la imagen redimensionada

TASK 4: Serpentina (ex4.serpentine_diagonal)
Esta función recorre una matriz en forma de serpentina en diagonal, alternando entre movimiento ascendente y descendente.
Lo que hicimos fue analizar el algortimo y vimos que en realidad lo que hacia era recorrer la matriz con diagonales ascendentes o descendentes 
dependiendo de si eran pares o impares, y asi fue como realizamos este ejercicio. No lo hicimos con imagenes ya que era mas liada. 
Parámetros:
- matrix: Matriz de entrada a recorrer.
Retorno: Una lista de elementos ordenados en el recorrido en serpentina.

TASK 5: Conversión a Blanco y Negro y Compresión (ex5.convertir_bn_y_comprimir)
Convierte una imagen a escala de grises y aplica compresión usando FFmpeg.Encontramos por internet que la comprension maxima que hacia era de 31,
lo comprobamos antes de acabar el metodo para asi fijar el numero 31 como comprension maxima, si este numero se cambia a numero mas bajo te da una calidad
mucho mejor. 
Parámetros:
. input_path: Ruta de la imagen de entrada.
- output_path: Ruta donde se guardará la imagen procesada.
Retorno: La ruta de salida de la imagen comprimida.

TASK 5_2: RLE(ex5_2.run_length_encoding)
Aplica la técnica de compresión RLE (Run-Length Encoding), que agrupa valores repetidos en pares de (numero_contador, valor).
Parámetros:
- data: Lista de datos a codificar.
Retorno: Lista de tuplas donde cada tupla contiene un par (conteo, valor).

TASK 6: Transformada Coseno Discreta (DCT) y su Inversa (IDCT) (ex6.run_dct, ex6.run_idct)
Estas funciones realizan la Transformada Coseno Discreta (DCT) y su inversa (IDCT) en una matriz, aplicando primero la DCT en las filas y luego en las columnas.
Simplemente importamos scipy.fftpack para poder usar .dct i .idct para realizar el ejercicio. 
Parámetros:
- data: Matriz de entrada para la DCT o IDCT.
Retorno: Matriz transformada mediante DCT o la reconstruida mediante IDCT.

TASK 7: Transformada Wavelet Discreta (DWT) y su Inversa (IDWT) (ex7.apply_dwt, ex7.apply_idwt)
Realiza la Transformada Wavelet Discreta (DWT) usando el wavelet 'haar' y su inversa (IDWT) en una matriz de datos.
Parámetros:
- array: Matriz de entrada para la DWT.
Retorno: Componentes de la transformada (LL, LH, HL, HH) para la DWT o la matriz reconstruida para la IDWT.

El archivo test.py contiene pruebas unitarias que validan la funcionalidad de cada función. Las pruebas incluyen:
TestEx3: Verifica el redimensionamiento de imágenes (función ex3.redimensionar_imagen).
TestEx4: Prueba el recorrido en serpentina diagonal de la matriz (función ex4.serpentine_diagonal).
TestEx5: Comprueba la conversión a blanco y negro y compresión de imágenes (función ex5.convertir_bn_y_comprimir).
TestEx5_2: Evalúa la codificación RLE (función ex5_2.run_length_encoding).
TestEx6: Testea la DCT y la IDCT (funciones ex6.run_dct y ex6.run_idct).
TestEx7: Verifica la DWT y la IDWT (funciones ex7.apply_dwt y ex7.apply_idwt).
Cada prueba utiliza el módulo unittest de Python para validar las salidas generadas contra valores esperados o verificar la existencia de archivos generados.



