# Proyecto de Detección y Análisis de Baches

## Descripción General
Este proyecto se enfoca en la detección y análisis de baches utilizando técnicas de visión por computadora y procesamiento de imágenes 3D. Procesa datos de sensores de profundidad para identificar baches, determinar su ubicación y tamaño, y generar una nube de puntos 3D detallada de la región de interés.

## Secuencia de Ejecución y Componentes del Proyecto

### 1. `Extractora.py` (Clase `BagFileProcessor`)
- **Descripción**: Maneja la extracción de datos de archivos `.bag`, incluyendo imágenes RGB, imágenes de profundidad y nubes de puntos.
- **Funcionalidades Principales**:
  - Configura y ejecuta un pipeline para leer datos de archivos `.bag`.
  - Extrae y guarda el primer frame de profundidad y RGB.
  - Genera y almacena una nube de puntos en formato PLY.

### 2. `DetectorBaches.py` (Clase `YoloDetector`)
- **Descripción**: Utiliza un modelo YOLO para detectar baches en imágenes RGB.
- **Funcionalidades Principales**:
  - Carga y aplica el modelo YOLO preentrenado.
  - Procesa imágenes RGB para identificar baches.
  - Guarda las coordenadas de baches detectados y las imágenes resultantes.

### 3. `ObtenerAlturaDeCaptura.py` (Clase `AlturaCaptura`)
- **Descripción**: Estima la altura de la superficie a partir de la nube de puntos.
- **Funcionalidades Principales**:
  - Analiza la nube de puntos para estimar la altura de la superficie de captura.

### 4. `TransformacionROI.py` (Clase `ROICoordinateConverter`)
- **Descripción**: Transforma coordenadas de la ROI de píxeles a metros.
- **Funcionalidades Principales**:
  - Calcula la escala de conversión de píxeles a metros.
  - Convierte y guarda las coordenadas de la ROI en metros.

### 5. `FiltrarNP.py` (Clase `PointCloudFilter`)
- **Descripción**: Filtra la nube de puntos para conservar solo los puntos dentro de la ROI.
- **Funcionalidades Principales**:
  - Carga la nube de puntos y datos de la ROI.
    
  - Filtra la nube de puntos utilizando los límites de la ROI.
    
  - Visualiza y guarda la nube de puntos filtrada.

## Uso del Proyecto
Para ejecutar el proyecto, siga los siguientes pasos:

  -Coloque su archivo .bag en la carpeta POO/ArchivoBag.
  -Ejecute el script principal main.py.
  -Revise los resultados en las carpetas correspondientes para imágenes procesadas, coordenadas y nubes de puntos filtradas.

## Requisitos
- Python 3.x
- Bibliotecas: OpenCV, Open3D, PyTorch (para YOLO), NumPy, etc.
- Un modelo YOLO preentrenado adecuado para la detección de baches.
