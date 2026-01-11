def format_category(category):
    category_map = {
        'top': ['t-shirt', 'blouse', 'shirt', 'tank top', 'polo shirt'],
        'pants': ['pants', 'trousers', 'jeans', 'leggings', 'shorts', 'jorts', 'skirt'],
        'shoe': ['sneakers', 'boots', 'shoes', 'loafers', 'heels'],
        'layer': ['hoodie', 'sweater', 'sweatshirt', 'jacket', 'cardigan','coat', 'blazer', 'overshirt', 'jumper']
    }
    return category_map.get(category, [category])


def select_by_category(data: list, category: str) -> dict:

    valid_categories = format_category(category)

    for item in data:
        item_category = item.get('category', '').lower()

        if item_category in valid_categories:
            return item

    return None


def select_outfit_items(database_results: list) -> dict:
    outfit = {
        'top': select_by_category(database_results, 'top'),
        'pants': select_by_category(database_results, 'pants'),
        'shoe': select_by_category(database_results, 'shoe'),
        'layer': select_by_category(database_results, 'layer')
    }
    return outfit

def validate_outfit(outfit: dict) -> tuple:
    required = ['top', 'pants', 'shoe']
    missing = [item for item in required if outfit.get(item) is None]

    return (len(missing) == 0, missing)


def get_product_links(outfit: dict) -> dict:
    links = {}

    for key in ['top', 'pants', 'shoe', 'layer']:
        item = outfit.get(key)
        if item:
            links[key] = item.get('url', 'N/A')
        else:
            links[key] = None

    return links