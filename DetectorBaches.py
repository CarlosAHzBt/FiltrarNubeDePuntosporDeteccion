from ultralytics import YOLO
from PIL import Image
import os
import json

class YoloDetector:
    def __init__(self):
        self.model = YOLO("POO/ResultadosDeteccion/ModeloDeteccion/best.pt")
        self.source_folder = "Paso1-ExtraerPLYyDepthFrame/ColorImage"
        #self.target_folder = target_folder
        self.coords_folder = "POO/ResultadosDeteccion/Coordenadas"

        # Crear carpetas si no existen
        #os.makedirs(self.target_folder, exist_ok=True)
        os.makedirs(self.coords_folder, exist_ok=True)

    def process_images(self):
        for filename in os.listdir(self.source_folder):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                self.process_image(filename)

        print("Processing complete, bounding boxes saved to:", self.coords_folder)

    def process_image(self, filename):
        image_path = os.path.join(self.source_folder, filename)
        image = Image.open(image_path)

        results = self.model.predict(source=image, conf=0.5)

        try:
            names = self.model.names
            car_id = list(names)[list(names.values()).index('Bache')]
            number = results[0].boxes.cls.tolist().count(car_id)

            detections = results[0].boxes.xyxy[0]  # Get detection bounding boxes

            if number == 1:
                for r in results:
                    for c in r.boxes.cls:
                        print(self.model.names[int(c)])

                with open(os.path.join(self.coords_folder, filename.replace('.png', '.txt')), 'w') as f:
                    f.write(str(detections.tolist()))

                #image.save(os.path.join(self.target_folder, filename))
        except:
            print("No se detecto nada")
            image.save(os.path.join('ImagenesResultados/NoIdentificadas', filename))


 

detector = YoloDetector()
detector.process_images()
