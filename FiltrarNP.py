import open3d as o3d
import numpy as np
import json

class PointCloudFilter:
    def __init__(self):
        """
        Inicializa el filtro de nube de puntos.

        :param json_path: Ruta al archivo JSON que contiene la región de interés.
        :param ply_path: Ruta al archivo PLY de la nube de puntos.
        """
        self.json_path = "POO/ResultadosDeteccion/Coordenadas/roi.json"
        self.ply_path = "POO/ArchivosDeLaExtraccion/Ply/output.ply"
        self.roi_data = None
        self.pcd = None
        

    def load_roi_data(self):
        """
        Carga la región de interés desde el archivo JSON.
        """
        with open(self.json_path, 'r') as file:
            self.roi_data = json.load(file)

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