import open3d as o3d
import numpy as np
import json
import glob
import os

class PointCloudFilter:
    def __init__(self,coor_path,ply_path):
        """
        Inicializa el filtro de nube de puntos.

        :param json_path: Ruta al archivo JSON que contiene la región de interés.
        :param ply_path: Ruta al archivo PLY de la nube de puntos.
        """
        self.txt_path = coor_path
        self.ply_path = ply_path
        self.roi_data = None
        self.pcd = None
        

    def load_roi_data(self):
        """
        Carga y procesa datos de ROI desde múltiples archivos basados en un patrón de nombre de archivo.

        Args:
        - base_path: La ruta de la carpeta donde se encuentran los archivos.
        - base_filename: El nombre base del archivo sin el índice y la extensión.
        """
        base_filename="RGBcolor_image_*.txt_*.txt"
        # Construye el patrón para buscar archivos que coincidan con el nombre base y cualquier índice extra
        search_pattern = os.path.join(self.txt_path, f"{base_filename}_*.txt")

        # Encuentra todos los archivos que coincidan con el patrón
        matching_files = glob.glob(search_pattern)

        # Procesa cada archivo encontrado
        for file_path in matching_files:
            try:
                with open(file_path, 'r') as file:
                    # Asume que cada archivo contiene un objeto JSON
                    roi_data = json.load(file)
                    # Aquí puedes procesar los datos de ROI como necesites
                    print(f"Datos cargados de {file_path}: {roi_data}")

                    # Opcional: Si deseas eliminar el archivo después de procesarlo
                    os.remove(file_path)
                    print(f"Archivo eliminado: {file_path}")

            except json.JSONDecodeError as e:
                print(f"Error al decodificar JSON en {file_path}: {e}")
            except FileNotFoundError as e:
                print(f"Archivo no encontrado: {file_path}: {e}")

    def load_point_cloud(self):
        """
        Carga la nube de puntos desde el archivo PLY.
        """
        self.pcd = o3d.io.read_point_cloud(self.ply_path)

    def filter_points_in_roi(self):
        """
        Filtra puntos dentro de la región de interés.
        """
        if self.pcd is None or self.roi_data is None:
            raise ValueError("Nube de puntos o datos de ROI no cargados")

        points = np.asarray(self.pcd.points)
        filtered_points = points[
            (points[:, 0] >= self.roi_data['x1']) & (points[:, 0] <= self.roi_data['x2']) &
            (points[:, 1] >= self.roi_data['y1']) & (points[:, 1] <= self.roi_data['y2'])
        ]

        filtered_pcd = o3d.geometry.PointCloud()
        filtered_pcd.points = o3d.utility.Vector3dVector(filtered_points)
        return filtered_pcd

    def visualize_point_cloud(self, pcd):
        """
        Visualiza la nube de puntos.
        """
        o3d.visualization.draw_geometries([pcd])
        

    def save_point_cloud(self, output_path, pcd):
        """
        Guarda la nube de puntos en un archivo PLY.
        """
        o3d.io.write_point_cloud(output_path, pcd)