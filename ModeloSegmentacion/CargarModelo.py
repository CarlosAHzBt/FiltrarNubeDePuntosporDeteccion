#Clase para cargar el modelo de segmentación
from Segformer_FineTuner import SegformerFinetuner
import torch

class CargarModelo:
    def __init__(self):
        self.args = None
        self.kwargs = None
    def cargar_modelo():
     # Crear una nueva instancia del modelo
     id2label = {
        0: "background",
        1: "Bache",
    }
     modelo = SegformerFinetuner(id2label=id2label)  # Asegúrate de proporcionar los argumentos necesarios aquí

     # Cargar el state_dict guardado en el modelo
     modelo.load_state_dict(torch.load('ModeloSegmentacion/model_state_dict.pth'))

     # Cambiar el modelo a modo de evaluación si se va a hacer inferencia
     modelo.eval()

     return modelo
