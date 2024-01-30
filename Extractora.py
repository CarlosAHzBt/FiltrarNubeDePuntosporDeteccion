#Clase que contiene las funcionalidades para extraer el PLY, imagen rgb e imagen de profundidad de un archivo .bag
import pyrealsense2 as rs
import numpy as np
import cv2
import os

class BagFileProcessor:
    def __init__(self, file_path):
        self.file_path = file_path
        self.config = rs.config()
        rs.config.enable_device_from_file(self.config, self.file_path)
        self.pipeline = rs.pipeline()
        self.align = rs.align(rs.stream.color)

    def process_frames(self):
        profile = self.pipeline.start(self.config)
        try:
            self.pipeline.wait_for_frames()
            while True:
                frames = self.pipeline.wait_for_frames()
                aligned_frames = self.align.process(frames)

                depth_frame = aligned_frames.get_depth_frame()
                if not depth_frame:
                    continue

                self.save_depth_image(depth_frame)
                self.save_color_image(aligned_frames)
                self.save_pointcloud(depth_frame, aligned_frames)
                break
        finally:
            self.pipeline.stop()
        print("Imagen de profundidad y nube de puntos PLY guardadas.")

    def save_depth_image(self, depth_frame):
        depth_image = np.asanyarray(depth_frame.get_data())
        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)
        cv2.imwrite('POO/ArchivosDeLaExtraccion/Depth/depth_image.png', depth_colormap)

    def save_color_image(self, aligned_frames):
        color_frame = aligned_frames.get_color_frame()
        color_image = np.asanyarray(color_frame.get_data())
        cv2.imwrite('POO/ArchivosDeLaExtraccion/RGBcolor_image.png', color_image)

    def save_pointcloud(self, depth_frame, aligned_frames):
        pc = rs.pointcloud()
        pc.map_to(aligned_frames.get_color_frame())
        points = pc.calculate(depth_frame)
        points.export_to_ply('POO/ArchivosDeLaExtraccion/Ply/output.ply', aligned_frames.get_color_frame())

# Uso de la clase
processor = BagFileProcessor('Paso1-ExtraerPLYyDepthFrame/BagFile/BacheRef2.bag')
processor.process_frames()
