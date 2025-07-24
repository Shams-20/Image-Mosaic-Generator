import os
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

def adjust_mean(tile, target_val):
    diff = target_val - tile.mean()
    return np.clip(tile + diff, 0, 255).astype(np.uint8)

def load_tiles(folder, size):
    tiles, means = [], []
    for filename in os.listdir(folder):
        path = os.path.join(folder, filename)
        try:
            img = Image.open(path).convert('L').resize(size)
            arr = np.array(img)
            tiles.append(arr)
            means.append(arr.mean())
        except:
            pass  
    return tiles, means

def find_best_tile(means, val):
    diffs = np.abs(np.array(means) - val)
    return np.argmin(diffs)

def create_single_mosaic(tile, big_img, scale=0.05):
    print("🔧 Creating single tile mosaic...")
    small = np.array(Image.fromarray(big_img).resize(
        (int(big_img.shape[1] * scale), int(big_img.shape[0] * scale))
    ))
    h, w = tile.shape
    mosaic = np.zeros((small.shape[0] * h, small.shape[1] * w), dtype=np.uint8)
    for i in range(small.shape[0]):
        for j in range(small.shape[1]):
            mosaic[i*h:(i+1)*h, j*w:(j+1)*w] = adjust_mean(tile, small[i, j])
    return mosaic

def create_photo_mosaic(big_img, tiles, means, tile_size, scale=0.05):
    print("🎨 Creating photo mosaic...")
    small = np.array(Image.fromarray(big_img).resize(
        (int(big_img.shape[1] * scale), int(big_img.shape[0] * scale))
    ))
    h, w = tile_size
    mosaic = np.zeros((small.shape[0] * h, small.shape[1] * w), dtype=np.uint8)
    for i in range(small.shape[0]):
        print(f"   Row {i+1}/{small.shape[0]}")  
        for j in range(small.shape[1]):
            idx = find_best_tile(means, small[i, j])
            mosaic[i*h:(i+1)*h, j*w:(j+1)*w] = tiles[idx]
    return mosaic

tile_path = "shrek.jpeg"       
source_path = "mona.png"        
tiles_folder = "tiles"           
tile_size = (32, 32)           
scale_factor = 0.1          

if not os.path.exists(tile_path) or not os.path.exists(source_path):
    print("Your image files are MIA. Check your paths.")
    exit()

# 📸 Load images
big_img = np.array(Image.open(source_path).convert('L'))
tile_img = np.array(Image.open(tile_path).convert('L'))
tiles, tile_means = load_tiles(tiles_folder, tile_size)

if not tiles:
    print("Your tiles folder is either empty or full of garbage. Feed better tiles")
    exit()

mosaic_single = create_single_mosaic(tile_img, big_img, scale=scale_factor)
mosaic_multi = create_photo_mosaic(big_img, tiles, tile_means, tile_size, scale=scale_factor)

plt.figure(figsize=(12, 6))
plt.subplot(1, 2, 1); plt.imshow(mosaic_single, cmap='gray'); plt.title("Single Tile Mosaic"); plt.axis('off')
plt.subplot(1, 2, 2); plt.imshow(mosaic_multi, cmap='gray'); plt.title("Photomosaic"); plt.axis('off')
plt.tight_layout(); plt.show()

Image.fromarray(mosaic_single).save("mosaic_single.png")
Image.fromarray(mosaic_multi).save("mosaic_photo.png")
print("Done! Saved 'mosaic_single.png' & 'mosaic_photo.png' ")
