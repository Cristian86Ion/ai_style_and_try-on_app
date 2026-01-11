from PIL import Image
import os

def get(item):
    if item is not None:
        if os.path.exists(rf'C:\Users\Matei\Pictures\Haine\{item['brand']}\{item['id']}.png'):
            return Image.open(rf'C:\Users\Matei\Pictures\Haine\{item['brand']}\{item['id']}.png')
    else:
        return None