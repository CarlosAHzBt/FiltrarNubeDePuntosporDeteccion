import torch
from PIL import Image
import matplotlib.pyplot as plt
from torchvision.transforms import Compose, ToTensor, Normalize
from CargarModelo import CargarModelo  # Asegúrate de tener esta clase correctamente definida
import numpy as np
from skimage.measure import label, regionprops  # Importar la funcion label
from skimage.transform import resize

# Configuración del dispositivo
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Cargar el modelo
modelo = CargarModelo()  # Asegúrate de inicializar correctamente tu modelo aquí
modelo = modelo.cargar_modelo()

# Función para preparar la imagen
def preparar_imagen(ruta_imagen):
    imagen = Image.open(ruta_imagen).convert("RGB")
    transformaciones = Compose([
        ToTensor(),
        Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])
    return transformaciones(imagen).unsqueeze(0).to(device)

# Función para aplicar el modelo, visualizar la detección y guardar las coordenadas de las ROIs
def aplicar_modelo_y_visualizar(ruta_imagen):
    pixel_values = preparar_imagen(ruta_imagen)
    with torch.no_grad():
        predicciones = modelo(pixel_values=pixel_values)
        predicted_mask = predicciones[0].argmax(dim=1).squeeze().cpu().numpy()

    # Redimensionar la máscara de segmentación a la resolución deseada
    predicted_mask_resized = resize(predicted_mask, (480, 848), order=0, preserve_range=True, anti_aliasing=False).astype(int)

    # Etiquetar cada región en la máscara de segmentación redimensionada
    labeled_baches_resized = label(predicted_mask_resized, connectivity=2)
    regions_resized = regionprops(labeled_baches_resized)

    # Filtrar regiones por área mínima (ajusta este valor según sea necesario)
    min_area = 10000  # Este es un ejemplo, deberás ajustar este valor
    filtered_regions_resized = [region for region in regions_resized if region.area >= min_area]

    # Guardar las coordenadas de las regiones filtradas de la imagen redimensionada
    for region in filtered_regions_resized:
        # Obtener coordenadas de la región
        coords = region.coords
        with open(f"roi_bache_{region.label}.txt", "w") as file:
            for y, x in coords:
                file.write(f"{x},{y}\n")

    # Visualización (opcional)
    imagen = Image.open(ruta_imagen).convert("RGB")
    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)
    plt.imshow(imagen)
    plt.title('Imagen Original')
    plt.subplot(1, 2, 2)
    plt.imshow(predicted_mask_resized, cmap='viridis')
    plt.title('Máscara de Segmentación Redimensionada')
    plt.colorbar()
    plt.show()

    # Guardar la imagen de la máscara de segmentación redimensionada
    plt.imsave('mascara_segmentacion_redimensionada.png', predicted_mask_resized, cmap='viridis')

# Ruta a la imagen de entrada
ruta_imagen = 'ArchivosDeLaExtraccion/RGBcolor_image.png'  # Actualiza esto con la ruta a tu imagen

# Aplicar el modelo a la imagen y visualizar la detección
aplicar_modelo_y_visualizar(ruta_imagen)
