#Este codigo es el que manda a ejecutar toda la secuencia de pasos de este proyecto para obtener 
#finalmente la nube de puntas ya recortada con la ROI que interesa osea del bache 
#Para ello es necesario tener un archivo .bag capturado a una resolucion de 848x480 tanto en depth como
#en color. Por ahora este codigo solo extrae el primer frame del archivo. 
#La metodologia del coodigo es la siguiente:
# 1.- Se extrae el framde de profundidad, la imagen rgb y la nube de puntos del archivo .bag
# 2.- Se aplica un modelo de deteccion sobre la imagen rgb para obtener la region de interes (bache)
# 3.- Se asignan las coordenadas de la region de interes a la imagen de profundidad
# 4.- Se filtran los puntos de la nube de puntos que esten dentro de la region de interes
# 5.- Se guarda la nube de puntos filtrada en un archivo .ply

import os
import json
import open3d as o3d
from Extractora import BagFileProcessor
from DetectorBaches import YoloDetector
from ObtenerAlturaDeCaptura import AlturaCaptura
from TransformacionROI import ROICoordinateConverter
from FiltrarNP import PointCloudFilter


def main():
    carpeta_con_bags ="POO/ArchivoBag" #Busca por archivos bag en la carpeta, donde deberian subirse los archivos bag
    procesar_bag(carpeta_con_bags) #Extrae el PLY, imagen rgb e imagen de profundidad del archivo .bag
    procesar_imagenes() #Aplica un modelo de deteccion sobre la imagen rgb para obtener la region de interes (bache)
    superficie_de_captura_estimada = estimar_superficie_de_captura() #Estima la altura de la captura
    asignar_coordenadas_a_imagen(superficie_de_captura_estimada) #Asigna las coordenadas de la region de interes a la imagen de profundidad
    filtrar_nube_de_puntos()


#Funcion para buscar por archivos bag en la carpeta
def buscar_archivo_bag(carpeta_bag):
    for root, dirs, files in os.walk(carpeta_bag):
        for file in files:
            if file.endswith(".bag"):
                bag_file = os.path.join(root, file)
                return bag_file
    return None

def procesar_bag(carpeta_bag):
    bag_file = buscar_archivo_bag(carpeta_bag)
    if not bag_file:
        print("No se encontró ningún archivo .bag")
        return
    print("Archivo .bag encontrado: ", bag_file)
    processor = BagFileProcessor(bag_file)
    try:
        processor.process_frames()
    except Exception as e:
        print(e)
        return
    print("Extracción de PLY, imagen RGB e imagen de profundidad completada.")
    print("Se procederá a asignar la región de interés a la imagen de profundidad.")

def procesar_imagenes():
    detector = YoloDetector()
    detector.process_images()
    print("Se procederá a filtrar la nube de puntos.")

def estimar_superficie_de_captura():
    ruta_archivo_ply = "ArchivosDeLaExtraccion/Ply/output.ply"
    altura_captura = AlturaCaptura(ruta_archivo_ply)
    altura = altura_captura.calcular_altura()
    print("Altura de la captura (moda en el eje Z):", altura)
    return altura

def asignar_coordenadas_a_imagen(altura_captura):
    roi_converter = ROICoordinateConverter()
    roi_converter.definir_roi_y_guardar(altura_captura,"ArchivosDeLaExtraccion/RGB/RGBcolor_image.png" ,"POO/ResultadosDeteccion/Coordenadas/roi.json", "POO/ResultadosDeteccion/Coordenadas/color_image.txt")
    print("Se procederá a filtrar la nube de puntos.")


def filtrar_nube_de_puntos():
    filter = PointCloudFilter()
    filter.load_roi_data()
    filter.load_point_cloud()
    #filter.visualize_point_cloud(pcd)
    filtered_pcd = filter.filter_points_in_roi()
    filter.visualize_point_cloud(filtered_pcd)
    filter.save_point_cloud("NubeDePuntosFiltrada/Np.ply", filtered_pcd)
    
if __name__ == '__main__':
    main()