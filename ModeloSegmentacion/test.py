import torch
from PIL import Image
import matplotlib.pyplot as plt
from torchvision.transforms import Compose, ToTensor, Normalize
from CargarModelo import CargarModelo  # Asegúrate de tener esta clase correctamente definida
import numpy as np
from skimage.measure import label, regionprops  # Importar la funcion label

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
    
        # Etiquetar cada bache en la máscara de segmentación
    labeled_baches = label(predicted_mask, connectivity=2)
    regions = regionprops(labeled_baches)

    # Filtrar regiones por área mínima (ajusta este valor según sea necesario)
    min_area = 100  # Este es un ejemplo, deberás ajustar este valor
    filtered_regions = [region for region in regions if region.area >= min_area]

    #guardar la imagen de la mascara de segmentacion
    plt.imsave('ModeloSegmentacion\mascara_segmentacion.png', predicted_mask, cmap='viridis')

    # Visualización (mantenemos tu código original aquí)
    imagen = Image.open(ruta_imagen).convert("RGB")
    predicted_mask_image = Image.fromarray(predicted_mask.astype(np.uint8))
    original_size = imagen.size
    resized_mask_image = predicted_mask_image.resize(original_size, Image.NEAREST)
    resized_mask = np.array(resized_mask_image)

    # Guardar las coordenadas de las regiones filtradas
    for region in filtered_regions:
        # Obtener coordenadas de la región
        coords = region.coords
        with open(f"roi_bache_{region.label}.txt", "w") as file:
            for y, x in coords:
                file.write(f"{x},{y}\n")
        


    plt.figure(figsize=(12, 12))
    plt.subplot(1, 2, 1)
    plt.imshow(imagen)
    plt.title('Imagen Original')
    plt.subplot(1, 2, 2)
    plt.imshow(resized_mask, cmap='viridis')
    plt.title('Máscara de Segmentación Redimensionada')
    plt.colorbar()
    plt.show()

    #Guardar imagen de la mascara de segmentacion redimensionada con cmap viridis
    plt.imsave('ModeloSegmentacion\mascara_segmentacion_redimensionada.png', resized_mask_image)
    

    
# Ruta a la imagen de entrada
ruta_imagen = 'ArchivosDeLaExtraccion\RGBcolor_image.png'  # Actualiza esto con la ruta a tu imagen

# Aplicar el modelo a la imagen y visualizar la detección
aplicar_modelo_y_visualizar(ruta_imagen)
