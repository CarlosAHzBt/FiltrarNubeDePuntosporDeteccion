import cv2 as cv
import numpy as np

# Cargar la imagen original
imagen_original = cv.imread('ModeloSegmentacion/mascara_segmentacion_redimensionada.png')

# Cargar las coordenadas que incluyen el contorno y el interior del bache
coordenadas = np.loadtxt('roi_bache_7.txt', delimiter=',')

# Crear una imagen en negro con las mismas dimensiones que la imagen original
mask = np.zeros(imagen_original.shape[:2], dtype=np.uint8)

# Dibujar los puntos como un polígono blanco sobre la máscara
cv.polylines(mask, [coordenadas.astype(np.int32)], isClosed=True, color=255, thickness=1)

# Encontrar los contornos en la máscara
contornos, _ = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

# Dibujar solo el contorno más grande
contorno_externo = max(contornos, key=cv.contourArea)
cv.drawContours(imagen_original, [contorno_externo], -1, (255, 0, 0), 1)

# Mostrar la imagen del contorno externo
cv.imshow("Contorno Externo", imagen_original)

# Guardar la imagen del contorno externo
cv.imwrite('imagen_contorno_externo.png', imagen_original)

cv.waitKey(0)
cv.destroyAllWindows()
