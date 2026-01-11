from PIL import Image
import os

def get(item):
    if item is not None:
        if os.path.exists(rf'C:\Users\ioncr\OneDrive\Desktop\test0\my-app\backend\processor\Haine{item["brand"]}\{item["id"]}.png'):
            return Image.open(rf'C:\Users\ioncr\OneDrive\Desktop\test0\my-app\backend\processor\Haine{item["brand"]}\{item["id"]}.png')
    else:
        return None
    # "brand" -> 'brand' pt alte versiuni in afara de 3.10