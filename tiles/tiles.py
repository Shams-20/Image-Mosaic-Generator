import os
import numpy as np
import cv2

OUTPUT_FOLDER = 'tiles/'
TILE_SIZE = 50  
NUM_TILES = 50  

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

for i in range(NUM_TILES):
    
    intensity = int((i / (NUM_TILES - 1)) * 255)  

    tile = np.full((TILE_SIZE, TILE_SIZE, 3), intensity, dtype=np.uint8)

    noise = np.random.randint(-10, 10, (TILE_SIZE, TILE_SIZE, 3), dtype=np.int8)
    tile = np.clip(tile + noise, 0, 255).astype(np.uint8)

    filename = os.path.join(OUTPUT_FOLDER, f'tile_{i}.jpg')
    cv2.imwrite(filename, tile)

print(f"Generated {NUM_TILES} synthetic grayscale tiles with varying intensities")
