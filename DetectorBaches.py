from ultralytics import YOLO
from PIL import Image
import cv2
from ultralytics.utils.plotting import Annotator
import os

class YoloDetector:
    def __init__(self):
        self.model = YOLO("ModeloDeteccion/best.pt")
        self.source_folder = "ArchivosDeLaExtraccion/RGB"
        self.target_folder = "ResultadosDeteccion/ImagenesConDetecciones"
        self.coords_folder = "ResultadosDeteccion/Coordenadas"
        self.no_identificadas_folder = "ResultadosDeteccion/NoIdentificadas"

        # Asegurarse de que existan las carpetas de destino
        os.makedirs(self.target_folder, exist_ok=True)
        os.makedirs(self.coords_folder, exist_ok=True)
        os.makedirs(self.no_identificadas_folder, exist_ok=True)

    def process_images(self):
        for filename in os.listdir(self.source_folder):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                self.process_image(filename)

        print("Processing complete, images and bounding boxes saved to:", self.coords_folder)

    def process_image(self, filename):
        image_path = os.path.join(self.source_folder, filename)
        frame = cv2.imread(image_path)
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Realiza la detección
        results = self.model.predict(img)
        try:
         # Abre el archivo en modo 'w' para sobrescribir cualquier archivo existente
         with open(os.path.join(self.coords_folder, filename.replace('.png', '.txt').replace('.jpg', '.txt').replace('.jpeg', '.txt')), 'w') as f:
             if results[0].boxes is not None and len(results[0].boxes) > 0:  # Verifica si hay detecciones
                 annotator = Annotator(frame, line_width=2, font_size=10)
                 for det in results[0].boxes:  # Itera sobre cada detección
                     b = det.xyxy[0]  # Coordenadas de la caja
                     c = int(det.cls)  # Clase de la detección
                     annotator.box_label(b, self.model.names[c])

                     # Guarda las coordenadas de los baches detectados en un archivo txt
                     f.write(f"{b[0]}, {b[1]}, {b[2]}, {b[3]}\n")

                 # Guarda la imagen con detecciones
                 result_frame = annotator.result()
                 cv2.imwrite(os.path.join(self.target_folder, filename), result_frame)
             else:
                 # Guarda imágenes sin detecciones identificadas en una carpeta específica
                 cv2.imwrite(os.path.join(self.no_identificadas_folder, filename), frame)
        except Exception as e:
            print(f"Error processing {filename}: {e}")

## Instancia y ejecuta el detector
#detector = YoloDetector()
#detector.process_images()
