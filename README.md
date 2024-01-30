# FiltrarNubeDePuntosporDeteccion
# Proyecto de Detección y Análisis de Baches

## Descripción General
Este proyecto tiene como objetivo detectar, analizar y cuantificar baches en carreteras o calles urbanas utilizando técnicas de visión por computadora y procesamiento de imágenes 3D. A través de la secuencia de pasos implementados en Python, el proyecto procesa datos de sensores de profundidad para identificar baches, determinar su ubicación y tamaño, y generar una nube de puntos 3D detallada de la región de interés.

## Componentes del Proyecto

### 1. `BagFileProcessor`
- **Descripción**: Esta clase se encarga de procesar archivos `.bag` para extraer imágenes RGB, imágenes de profundidad y nubes de puntos (formato PLY).
- **Funcionalidades**:
  - Configura y ejecuta un pipeline para leer desde archivos `.bag`.
  - Extrae y guarda imágenes RGB y de profundidad.
  - Genera y almacena nubes de puntos PLY.

### 2. `YoloDetector`
- **Descripción**: Implementa un modelo YOLO para detectar baches en las imágenes RGB extraídas.
- **Funcionalidades**:
  - Carga el modelo YOLO preentrenado.
  - Realiza detecciones en imágenes.
  - Guarda imágenes con detecciones y las coordenadas de los baches detectados.

### 3. `ROICoordinateConverter`
- **Descripción**: Convierte las coordenadas de la región de interés (ROI) de píxeles a metros.
- **Funcionalidades**:
  - Calcula la escala de conversión basada en la altura de captura y resolución de la cámara.
  - Convierte coordenadas de la ROI de píxeles a metros.
  - Guarda las coordenadas convertidas en un archivo JSON.

### 4. `PointCloudFilter`
- **Descripción**: Filtra la nube de puntos PLY para conservar solo aquellos puntos dentro de la ROI.
- **Funcionalidades**:
  - Carga la ROI desde un archivo JSON.
  - Filtra la nube de puntos según la ROI.
  - Visualiza y guarda la nube de puntos filtrada.

### 5. `AlturaCaptura`
- **Descripción**: Calcula la altura aproximada de la captura de la nube de puntos.
- **Funcionalidades**:
  - Analiza la nube de puntos para estimar la altura de la superficie capturada.

## Flujo del Proyecto
1. **Extracción de Datos**: Uso de `BagFileProcessor` para obtener imágenes y nubes de puntos de archivos `.bag`.
2. **Detección de Baches**: Aplicación de `YoloDetector` para identificar baches en imágenes RGB.
3. **Asignación de Coordenadas**: Transformación de las coordenadas de los baches a metros utilizando `ROICoordinateConverter`.
4. **Filtrado de Nube de Puntos**: Selección de puntos dentro de la ROI con `PointCloudFilter`, basada en las coordenadas transformadas.
5. **Análisis de Profundidad**: Uso de `AlturaCaptura` para cálculos relacionados con la profundidad y dimensiones de los baches.

## Uso del Proyecto
Para ejecutar el proyecto, siga los siguientes pasos:
1. Coloque su archivo `.bag` en la carpeta `POO/ArchivoBag`.
2. Ejecute el script principal `main.py`.
3. Revise los resultados en las carpetas correspondientes para imágenes procesadas, coordenadas y nubes de puntos filtradas.

## Requisitos
- Python 3.x
- Bibliotecas: OpenCV, Open3D, PyTorch (para YOLO), NumPy, etc.
- Un modelo YOLO preentrenado adecuado para la detección de baches.
