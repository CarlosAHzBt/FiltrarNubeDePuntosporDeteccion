import torch
from PIL import Image
import matplotlib.pyplot as plt
from torchvision.transforms import Compose, ToTensor, Normalize
from CargarModelo import CargarModelo
import numpy as np
# Configuración del dispositivo
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Cargar el modelo (Asegúrate de reemplazar 'SegformerFinetuner' con la inicialización correcta de tu modelo)
modelo = CargarModelo
modelo = modelo.cargar_modelo()


# Función para preparar la imagen
def preparar_imagen(ruta_imagen):
    imagen = Image.open(ruta_imagen).convert("RGB")
    transformaciones = Compose([
        ToTensor(),
        Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])
    return transformaciones(imagen).unsqueeze(0).to(device)

# Función para aplicar el modelo y visualizar la detección
def aplicar_modelo_y_visualizar(ruta_imagen):
    pixel_values = preparar_imagen(ruta_imagen)
    with torch.no_grad():
        predicciones = modelo(pixel_values=pixel_values)
        predicted_mask = predicciones[0].argmax(dim=1).squeeze().cpu().numpy()
    
    imagen = Image.open(ruta_imagen).convert("RGB")
    logits = predicciones[0]  # Extracción de logits, suponiendo que 'predicciones' es una tupla
    predicted_mask = logits.argmax(dim=1).squeeze().cpu().numpy()  # Conversión de logits a máscara de segmentación

    # Convertir la máscara de segmentación a una imagen PIL para redimensionar
    predicted_mask_image = Image.fromarray(predicted_mask.astype(np.uint8))

    # Redimensionar la máscara de segmentación al tamaño original de la imagen
    original_size = imagen.size  # Tamaño de la imagen original (ancho, alto)
    resized_mask_image = predicted_mask_image.resize(original_size, Image.NEAREST)

    # Convertir la imagen redimensionada de nuevo a un array de NumPy para visualización
    resized_mask = np.array(resized_mask_image)

    # Visualización de la imagen original y la máscara de segmentación redimensionada
    plt.figure(figsize=(12, 12))

    # Visualizar la imagen original
    plt.subplot(1, 2, 1)
    plt.imshow(imagen)
    plt.title('Imagen Original')

    # Visualizar la máscara de segmentación redimensionada
    plt.subplot(1, 2, 2)
    plt.imshow(resized_mask, cmap='viridis')  # 'viridis' es un ejemplo de colormap, puedes elegir otro si es necesario
    plt.title('Máscara de Segmentación Redimensionada')
    plt.colorbar()  # Muestra la barra de colores que corresponde a las clases

    plt.show()
# Ruta a la imagen de entrada
#AQUI CARGA TU IMAGEN PARA PROBAR
ruta_imagen = r'D:\6FebLey\imagenes\20240206_073644\RGB\frame_00149.png'

# Aplicar el modelo a la imagen y visualizar la detección
aplicar_modelo_y_visualizar(ruta_imagen)


