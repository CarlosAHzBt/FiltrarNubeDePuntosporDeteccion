#Vizualizar una nube de puntos

import open3d as o3d
import numpy as np
import os

def visualizar_nube_de_puntos(archivo_ply):
    pcd = o3d.io.read_point_cloud(archivo_ply)
    o3d.visualization.draw_geometries([pcd])

visualizar_nube_de_puntos(r"NubeDePuntosFiltrada\output_0_filtrado.ply")
    
