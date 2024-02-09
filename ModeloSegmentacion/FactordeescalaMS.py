from PIL import Image
import numpy as np

#ruta del txt 
# Cargar las coordenadas del contorno desde tu archivo txt
contorno = np.loadtxt('roi_bache_7.txt', delimiter=',')
# Ruta a la imagen original y a la imagen de la máscara de segmentación
ruta_imagen_original = 'ArchivosDeLaExtraccion/RGBcolor_image.png'
ruta_imagen_segmentacion = 'ModeloSegmentacion/mascara_segmentacion.png'

# Abrir la imagen original y obtener sus dimensiones
with Image.open(ruta_imagen_original) as img_original:
    dimensiones_originales = img_original.size  # (ancho, alto)

# Abrir la imagen de la máscara de segmentación y obtener sus dimensiones
with Image.open(ruta_imagen_segmentacion) as img_segmentacion:
    dimensiones_segmentacion = img_segmentacion.size  # (ancho, alto)

# Calcular factores de escala
factor_escala_x = dimensiones_originales[0] / dimensiones_segmentacion[0]
factor_escala_y = dimensiones_originales[1] / dimensiones_segmentacion[1]

# Escalar las coordenadas del contorno
contorno_escalado = np.array([[x * factor_escala_x, y * factor_escala_y] for x, y in contorno])

# Guardar las coordenadas escaladas en un nuevo archivo txt
np.savetxt('contorno_escalado.txt', contorno_escalado, fmt='%d', delimiter=',')
