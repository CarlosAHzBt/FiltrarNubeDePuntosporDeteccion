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
    carpeta_con_bags ="ArchivoBag" #Busca por archivos bag en la carpeta, donde deberian subirse los archivos bag
    procesar_bag(carpeta_con_bags) #Extrae el PLY, imagen rgb e imagen de profundidad del archivo .bag
    procesar_imagenes() #Aplica un modelo de deteccion sobre la imagen rgb para obtener la region de interes (bache)
    
    #ciclo para apartir del las coordenadas roi obtenida y del ply correspondiente de cada archivo en la carpeta
    archivos_ply = obtener_archivos_ordenados("ArchivosDeLaExtraccion/Ply", ".ply")
    archivos_rgb = obtener_archivos_ordenados("ArchivosDeLaExtraccion/RGB", ".png")
    archivo_coord= obtener_archivos_ordenados("ResultadosDeteccion/Coordenadas", ".txt")
    #archivo_coord_output= obtener_archivos_ordenados("ResultadosDeteccion/Coordenadas", ".txt")

    for archivo_ply, archivo_rgb, archivo_coord in zip(archivos_ply, archivos_rgb, archivo_coord):
        print(f"Procesando {archivo_ply} y {archivo_rgb} y {archivo_coord}")
        #crear una carpetadonde iran las coordenadas transformadas a metrros 
        os.makedirs("ResultadoDeteccion/CoordenadasTranformadas", exist_ok=True)
        archivo_coord_output = os.path.join("ResultadoDeteccion/CoordenadasTranformadas", os.path.basename(archivo_coord))
        # Aquí aplicas tus procesos a cada par de archivos
        superficie_de_captura_estimada = estimar_superficie_de_captura(archivo_ply)
        asignar_coordenadas_a_imagen(superficie_de_captura_estimada,archivo_rgb,archivo_coord_output,archivo_coord)
        filtrar_nube_de_puntos(archivo_coord_output,archivo_ply)


def obtener_archivos_ordenados(directorio, extension):
    archivos = []
    for root, dirs, files in os.walk(directorio):
        for file in sorted(files):
            if file.endswith(extension):
                archivos.append(os.path.join(root, file))
    return archivos
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

def estimar_superficie_de_captura(ruta_archivo_ply):
    #ruta_archivo_ply = " ArchivosDeLaExtraccion/Ply/output.ply"
    altura_captura = AlturaCaptura(ruta_archivo_ply)
    altura = altura_captura.calcular_altura()
    print("Altura de la captura (moda en el eje Z):", altura)
    return altura

def asignar_coordenadas_a_imagen(altura_captura,archivo_rgb,archivo_coord_output,archivo_coord):
    roi_converter = ROICoordinateConverter()
    roi_converter.definir_roi_y_guardar(altura_captura,archivo_rgb ,archivo_coord_output, archivo_coord)
    print("Se procederá a filtrar la nube de puntos.")


def filtrar_nube_de_puntos(coor_path, ply_path):
    filter = PointCloudFilter(coor_path, ply_path)
    filter.load_roi_data()
    filter.load_point_cloud()
    #filter.visualize_point_cloud(pcd)
    filtered_pcd = filter.filter_points_in_roi()
    filter.visualize_point_cloud(filtered_pcd)

    # Extraer el nombre base del archivo .ply
    nombre_base = os.path.basename(ply_path)
    # Eliminar la extensión del archivo (por ejemplo, '.ply')
    nombre_sin_extension = os.path.splitext(nombre_base)[0]

    # Crear el nuevo nombre del archivo y la ruta de guardado
    nuevo_nombre_archivo = f"{nombre_sin_extension}_filtrado.ply"
    ruta_guardado_NP_filtrada = os.path.join("NubeDePuntosFiltrada", nuevo_nombre_archivo)

    # Guardar la nube de puntos filtrada con el nuevo nombre
    filter.save_point_cloud(ruta_guardado_NP_filtrada, filtered_pcd)
    
if __name__ == '__main__':
    main()