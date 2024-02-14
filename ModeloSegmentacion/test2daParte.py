import cv2 as cv
import numpy as np

# Cargar la imagen original
imagen_original = cv.imread('ModeloSegmentacion/mascara_segmentacion_redimensionada.png')

# Cargar las coordenadas que incluyen el contorno y el interior del bache
coordenadas = np.loadtxt('roi_bache_7.txt', delimiter=',')

# Crear una imagen en negro con las mismas dimensiones que la imagen original
imagen_contorno = np.zeros((480, 848, 3), dtype=np.uint8)

# Colorear los puntos especificados en el archivo txt
for x, y in coordenadas.astype(np.int32):
    imagen_contorno[y, x] = [255, 255, 255]

# Encontrar los contornos en la imagen de puntos
contornos, _ = cv.findContours(cv.cvtColor(imagen_contorno, cv.COLOR_BGR2GRAY), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

# Dibujar el contorno más grande
contorno_externo = max(contornos, key=cv.contourArea)
cv.drawContours(imagen_contorno, [contorno_externo], -1, (0, 255, 0), 2)

# Buscar el radio máximo y el centro del círculo
radio_maximo = 0
centro_circulo = (0, 0)

# Itera sobre los puntos del contorno
for punto in np.argwhere(cv.cvtColor(imagen_contorno, cv.COLOR_BGR2GRAY)):
    dist = cv.pointPolygonTest(contorno_externo, (int(punto[1]), int(punto[0])), True)
    if dist > radio_maximo:
        radio_maximo = dist
        centro_circulo = (int(punto[1]), int(punto[0]))

# Dibujar el círculo máximo inscrito en la imagen original
cv.circle(imagen_original, centro_circulo, int(radio_maximo), (0, 255, 0), 2)

# Imprimir la medida del círculo máximo inscrito
print(f'Centro del círculo: {centro_circulo}')
print(f'Radio máximo: {radio_maximo}')

# Mostrar la imagen con el contorno y el círculo máximo inscrito
cv.imshow('Imagen con círculo máximo inscrito', imagen_original)
cv.waitKey(0)
cv.destroyAllWindows()

# Guardar la imagen con el contorno y el círculo máximo inscrito
cv.imwrite('imagen_contorno_bache_con_circulo_maximo_inscrito.png', imagen_original)
