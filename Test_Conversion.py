# Parámetros de la escala de conversión calculados previamente
escala_horizontal = 0.00154  # metros/píxel
escala_vertical = 0.00152    # metros/píxel

# Coordenadas de píxeles de dos esquinas opuestas de la escala de ajedrez (Ejemplo)
# Estas deben ser reemplazadas por tus valores reales
x1_pix, y1_pix = 402, 234  # Esquina superior izquierda
x2_pix, y2_pix = 415, 248  # Esquina inferior derecha

# Dimensiones reales de la escala de ajedrez en metros
ancho_real_m = 22 / 1000  # 220mm convertidos a metros
alto_real_m = 22 / 1000   # 155mm convertidos a metros

# Convertir coordenadas de píxeles a metros
ancho_m = abs(x2_pix - x1_pix) * escala_horizontal
alto_m = abs(y2_pix - y1_pix) * escala_vertical

# Comparar las medidas convertidas con las dimensiones reales
print(f"Medidas convertidas: {ancho_m:.3f}m x {alto_m:.3f}m")
print(f"Dimensiones reales: {ancho_real_m:.3f}m x {alto_real_m:.3f}m")
print(f"Diferencia en ancho: {abs(ancho_m - ancho_real_m):.3f}m")
print(f"Diferencia en alto: {abs(alto_m - alto_real_m):.3f}m")
