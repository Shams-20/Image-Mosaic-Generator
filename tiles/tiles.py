import os
import numpy as np
import cv2

OUTPUT_FOLDER = 'tiles/'
TILE_SIZE = 50  # Size of each tile (50x50 px)
NUM_TILES = 50  # Number of synthetic tiles to generate

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

for i in range(NUM_TILES):
    # Random or evenly spaced intensity
    intensity = int((i / (NUM_TILES - 1)) * 255)  # From black to white, evenly spaced

    # Create tile filled with that intensity
    tile = np.full((TILE_SIZE, TILE_SIZE, 3), intensity, dtype=np.uint8)

    # Add some random noise or patterns to make it look less flat
    noise = np.random.randint(-10, 10, (TILE_SIZE, TILE_SIZE, 3), dtype=np.int8)
    tile = np.clip(tile + noise, 0, 255).astype(np.uint8)

    filename = os.path.join(OUTPUT_FOLDER, f'tile_{i}.jpg')
    cv2.imwrite(filename, tile)

print(f"Generated {NUM_TILES} synthetic grayscale tiles with varying intensities")
