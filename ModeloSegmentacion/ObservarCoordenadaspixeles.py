#Codigo para ver las coordenadas de los pixeles de la mascara de segmentacion 
# en una imagen aparte
import numpy as np
import cv2

# Replace 'path_to_your_file.txt' with the actual path to your txt file
coordinates_path = 'contorno_escalado.txt'

# Load the coordinates from txt file
coordinates = np.loadtxt(coordinates_path, delimiter=',')

# Assume the size of the mask image is known (replace with actual size)
mask_size = (480,848 )  # Replace with actual size

# Create a blank image
mask_image = np.zeros(mask_size, dtype=np.uint8)

# Draw each point from the txt file onto the image
for point in coordinates:
    # Assuming point[0] is x and point[1] is y
    # Also assuming the coordinates are in the correct range for the image size
    x, y = int(point[0]), int(point[1])
    mask_image[y, x] = 255  # Color the point white

# Save the result to a file
cv2.imwrite('mask_from_coordinates.png', mask_image)

# Or display the image (if you are using a GUI environment)
cv2.imshow('Mask from Coordinates', mask_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
