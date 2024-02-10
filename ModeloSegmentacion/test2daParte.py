import cv2 as cv
import numpy as np

# Cargar la imagen original
imagen_original = cv.imread('ModeloSegmentacion/mascara_segmentacion_redimensionada.png')

# Cargar las coordenadas que incluyen el contorno y el interior del bache
coordenadas = np.loadtxt('contorno_escalado.txt', delimiter=',')

# Crear una imagen en negro con las mismas dimensiones que la imagen original
mask = np.zeros(imagen_original.shape[:2], dtype=np.uint8)

# Dibujar los puntos como un polígono blanco sobre la máscara
cv.polylines(mask, [coordenadas.astype(np.int32)], isClosed=True, color=(255), thickness=1)

# Aplicar la operación de cierre morfológico para rellenar huecos
kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (6, 6))
mask = cv.morphologyEx(mask, cv.MORPH_CLOSE, kernel)

# Encontrar los contornos en la máscara
contornos, _ = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)

# Asegurarse de que contorno_externo es una lista de tuplas (x, y)
contorno_externo = max(contornos, key=cv.contourArea)
contorno_externo = contorno_externo.squeeze()
if contorno_externo.ndim == 1:
    contorno_externo = contorno_externo.reshape(-1, 1, 2)

# Buscar el radio máximo y el centro del círculo
radio_maximo = 0
centro_circulo = (0, 0)

# Itera sobre una grilla de puntos dentro del rango de coordenadas del contorno
for punto in np.argwhere(mask):
    dist = cv.pointPolygonTest(contorno_externo, (int(punto[1]), int(punto[0])), True)
    if dist > radio_maximo:
        radio_maximo = dist
        centro_circulo = (int(punto[1]), int(punto[0]))

# Dibujar el círculo máximo inscrito
cv.circle(imagen_original, centro_circulo, int(radio_maximo), (0, 255, 0), 2)
# Imprimir la medida del círculo máximo inscrito
print(f'Centro del círculo: {centro_circulo}')
print(f'Radio máximo: {radio_maximo}')
# Guardar o mostrar la imagen resultante
cv.imwrite('imagen_contorno_bache_con_circulo_maximo_inscrito.png', imagen_original)
cv.imshow('Imagen con círculo máximo inscrito', imagen_original)
cv.waitKey(0)
cv.destroyAllWindows()
