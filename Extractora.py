import pyrealsense2 as rs
import numpy as np
import cv2
import os

class BagFileProcessor:
    def __init__(self, file_path):
        self.file_path = file_path
        self.config = rs.config()
        rs.config.enable_device_from_file(self.config, self.file_path,repeat_playback=False)
        self.pipeline = rs.pipeline()
        self.align = rs.align(rs.stream.color)
        self.frame_count = 0  # Contador para nombrar los archivos de salida

    def process_frames(self):
        profile = self.pipeline.start(self.config)
        try:
            while True:
                try:
                    frames = self.pipeline.wait_for_frames()
                except RuntimeError:
                    break  # Termina el bucle si no hay más frames

                aligned_frames = self.align.process(frames)

                depth_frame = aligned_frames.get_depth_frame()
                if not depth_frame:
                    continue

                self.save_depth_image(depth_frame)
                self.save_color_image(aligned_frames)
                self.save_pointcloud(depth_frame, aligned_frames)
                self.frame_count += 1

        finally:
            self.pipeline.stop()
        print("Todos los frames de profundidad y nubes de puntos PLY han sido guardados.")

    def save_depth_image(self, depth_frame):
        depth_image = np.asanyarray(depth_frame.get_data())
        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)
        cv2.imwrite(f'ArchivosDeLaExtraccion/Depth/depth_image_{self.frame_count}.png', depth_colormap)

    def save_color_image(self, aligned_frames):
        color_frame = aligned_frames.get_color_frame()
        color_image = np.asanyarray(color_frame.get_data())
        cv2.imwrite(f'ArchivosDeLaExtraccion/RGB/RGBcolor_image_{self.frame_count}.png', color_image)

    def save_pointcloud(self, depth_frame, aligned_frames):
        pc = rs.pointcloud()
        pc.map_to(aligned_frames.get_color_frame())
        points = pc.calculate(depth_frame)
        points.export_to_ply(f'ArchivosDeLaExtraccion/Ply/output_{self.frame_count}.ply', aligned_frames.get_color_frame())

# Uso de la clase
processor = BagFileProcessor('ArchivoBag/BacheRef2.bag')
processor.process_frames()
