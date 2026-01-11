from backend.database import dbread
from random import shuffle
import clotheselector as clotheselector
import getimages as getimages


def process(filters: dict) -> dict:
    data = dbread.query(filters)

    shuffle(data)

    outfit = clotheselector.select_outfit_items(data)

    is_valid, missing = clotheselector.validate_outfit(outfit)


    images = {
        'top': getimages.get(outfit.get('top')),
        'pants': getimages.get(outfit.get('pants')),
        'shoe': getimages.get(outfit.get('shoe')),
        'layer': getimages.get(outfit.get('layer'))
    }

    return {
        'items': outfit,
        'images': images,
        'valid': is_valid,
        'missing': missing
    }


def get_outfit_summary(outfit_items: dict) -> str:

    lines = []

    for key in ['top', 'pants', 'shoe', 'layer']:
        item = outfit_items.get(key)
        if item:
            brand = item.get('brand', 'Unknown').upper()
            category = item.get('category', 'item').title()
            colors = ', '.join(item.get('colors', ['N/A']))

            lines.append(f"{key.upper()}: {brand} {category} ({colors})")

    return "\n".join(lines)