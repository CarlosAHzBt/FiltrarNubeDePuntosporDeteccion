import cv2 as cv
import numpy as np

# Cargar la imagen original
imagen_original = cv.imread('ModeloSegmentacion/mascara_segmentacion.png')

# Cargar las coordenadas que incluyen el contorno y el interior del bache
coordenadas = np.loadtxt('roi_bache_7.txt', delimiter=',')

# Crear una imagen en negro con las mismas dimensiones que la imagen original
mask = np.zeros(imagen_original.shape[:2], dtype=np.uint8)

# Dibujar los puntos como un polígono blanco sobre la máscara
cv.polylines(mask, [coordenadas.astype(np.int32)], isClosed=True, color=(255), thickness=1)

# Encontrar los contornos en la máscara
contornos, _ = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

# Dibujar solo el contorno externo más grande (asumiendo que es el del bache)
contorno_externo = max(contornos, key=cv.contourArea)
mask_contorno = np.zeros_like(mask)
cv.drawContours(mask_contorno, [contorno_externo], -1, (255), thickness=1)  # Establece el grosor de la línea

# Opcionalmente, aplicar la máscara a la imagen original para visualizar el contorno del bache
imagen_contorno = cv.bitwise_and(imagen_original, imagen_original, mask=mask_contorno)

# Guardar o mostrar la imagen resultante
cv.imwrite('imagen_contorno_bache.png', imagen_contorno)
