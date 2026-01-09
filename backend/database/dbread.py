import json
import queryfactory
from decimal import Decimal

def get_filters_from_user():
    filters = {
        "brand": None,
        "category": None,
        "gender": None,
        "colors": None,
        "style": None,
        "price_eur": None
    }
    #TODO habar n am cum o pun pe asta in front

def query_db(cur):
    #filters = get_filters_from_user()
    filters = {
        "gender": "man",
        "brand": "zara"
    }
    full_query, parameters = queryfactory.create(filters)
    cur.execute(full_query, parameters)
    return cur.fetchall()

def default_converter(obj):
    if isinstance(obj, Decimal):
        return float(obj)  # Or use str(obj) to keep exact precision
    raise TypeError(f"Type {type(obj)} not serializable")

def query_to_json(rez):
    with open("file.json", "w") as f:
        json.dump(rez, f, default=default_converter)
