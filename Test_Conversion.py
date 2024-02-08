import math

# Parámetros de la cámara
fov_horizontal = 69  # FoV horizontal en grados
fov_vertical = 42   # FoV vertical en grados
altura_captura = 0.96  # Altura de captura en metros
resolucion_ancho = 848  # Resolución en píxeles (ancho)
resolucion_alto = 480  # Resolución en píxeles (alto)

# Cálculo de ancho y alto reales en metros utilizando la altura de captura
ancho_real = 2 * altura_captura * math.tan(math.radians(fov_horizontal / 2))
alto_real = 2 * altura_captura * math.tan(math.radians(fov_vertical / 2))

# Cálculo de la escala de conversión de píxeles a metros
escala_horizontal = ancho_real / resolucion_ancho
escala_vertical = alto_real / resolucion_alto

# Coordenadas de píxeles de dos esquinas opuestas de la escala de ajedrez
x1_pix, y1_pix = 99, 241  # Esquina superior izquierda
x2_pix, y2_pix = 112, 254  # Esquina inferior derecha

# Dimensiones reales de la escala de ajedrez en metros
ancho_real_m = 22 / 1000  # 22 mm convertidos a metros
alto_real_m = 22 / 1000   # 22 mm convertidos a metros

# Convertir coordenadas de píxeles a metros
ancho_m = abs(x2_pix - x1_pix) * escala_horizontal
alto_m = abs(y2_pix - y1_pix) * escala_vertical

# Comparar las medidas convertidas con las dimensiones reales
print(f"Medidas convertidas: {ancho_m:.3f}m x {alto_m:.3f}m")
print(f"Dimensiones reales: {ancho_real_m:.3f}m x {alto_real_m:.3f}m")
print(f"Diferencia en ancho: {abs(ancho_m - ancho_real_m):.3f}m")
print(f"Diferencia en alto: {abs(alto_m - alto_real_m):.3f}m")
