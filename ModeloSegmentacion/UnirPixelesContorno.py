import cv2 as cv
import numpy as np

# Cargar las coordenadas que incluyen el contorno y el interior del bache desde tu archivo txt
coordenadas = np.loadtxt('contorno_escalado.txt', delimiter=',')

# Asumiendo que 'imagen_original' es una imagen con el mismo tamaño desde el que se escalaron las coordenadas
imagen_original = cv.imread('imagen_contorno_bache.png')

# Crear una imagen en negro con las mismas dimensiones que la imagen original
mask = np.zeros(imagen_original.shape[:2], dtype=np.uint8)

# Unir las coordenadas con líneas para formar el contorno
# El argumento isClosed=True asegura que el contorno sea cerrado
cv.polylines(mask, [coordenadas.astype(np.int32)], isClosed=True, color=(255), thickness=1)

# Ahora 'mask' contiene una representación del contorno del bache que puedes usar para lo que necesites
# Por ejemplo, puedes guardar esta máscara o mostrarla
cv.imwrite('contorno.png', mask)
cv.imshow('Contorno', mask)
cv.waitKey(0)
cv.destroyAllWindows()