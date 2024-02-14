import cv2 as cv
import numpy as np

# Cargar las coordenadas que incluyen el contorno y el interior del bache
coordenadas = np.loadtxt('roi_bache_7.txt', delimiter=',')

# Crear una imagen en negro con las dimensiones deseadas
imagen_contorno = np.zeros((480, 848, 3), dtype=np.uint8)

# Colorear los puntos especificados en el archivo txt
for x, y in coordenadas.astype(np.int32):
    imagen_contorno[y, x] = [255, 255, 255]  # Cambia el color si es necesario

# Dibujar el contorno de los puntos coloreados
# Encontrar los contornos en la imagen de puntos
contornos, _ = cv.findContours(cv.cvtColor(imagen_contorno, cv.COLOR_BGR2GRAY), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

# Dibujar el contorno más grande
contorno_externo = max(contornos, key=cv.contourArea)
cv.drawContours(imagen_contorno, [contorno_externo], -1, (0, 255, 0), 2)

# Mostrar la imagen con el contorno dibujado
cv.imshow("Imagen con Contorno Dibujado", imagen_contorno)
cv.waitKey(0)
cv.destroyAllWindows()

# Guardar la imagen con el contorno dibujado
cv.imwrite('imagen_contorno_dibujado.png', imagen_contorno)
