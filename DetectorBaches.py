from ultralytics import YOLO
from PIL import Image
import os
import json

class YoloDetector:
    def __init__(self):
        self.model = YOLO("ResultadosDeteccion/ModeloDeteccion/best.pt")
        self.source_folder = "ArchivosDeLaExtraccion/RGB"
        self.coords_folder = "ResultadosDeteccion/Coordenadas"

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
            detections = results[0].boxes.xyxy  # Get detection bounding boxes
            # Check if there are detections
            if len(detections) > 0:
                detections_list = []
                for detection in detections:
                    detections_list.append(detection.tolist())
                
                # Write detections to a file
                with open(os.path.join(self.coords_folder, filename.replace('.png', '.txt').replace('.jpg', '.txt').replace('.jpeg', '.txt')), 'w') as f:
                    for det in detections_list:
                        f.write(f'{det}\n')
            else:
                print(f"No detections in {filename}")
        except Exception as e:
            print(f"Error processing {filename}: {e}")
 

detector = YoloDetector()
detector.process_images()
