def format_category(category):
    if category == 'pants':
        return ['leggings', 'trousers', 'jeans']
    elif category == 'top':
        return ['t-shirt', 'blouse', 'shirt']
    elif category == 'overshirt':
        return ['hoodie', 'sweater', 'sweatshirt', 'jacket']
    else:
        return category

def select(data, category):
    for d in data:
        if d['category'] in format_category(category):
            return d

    return None