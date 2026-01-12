"""
Clothes Selector - Selects outfit items from available inventory.
"""

from random import choice
from typing import Dict, List, Optional, Tuple

CATEGORY_MAP = {
    "top": [
        "t-shirt", "shirt", "hoodie", "jumper", "sweater", "top",
        "sweatshirt", "tank_top", "polo_shirt", "cardigan", "blouse"
    ],
    "pants": [
        "pants", "trousers", "jeans", "jorts", "skirt", "leggings",
        "joggers", "shorts", "chinos"
    ],
    "shoe": [
        "shoe", "shoes", "sneaker", "sneakers", "trainer", "trainers",
        "boot", "boots", "footwear", "running-shoes", "casual-shoes",
        "sandals", "loafers"
    ],
    "layer": [
        "jacket", "coat", "blazer", "overshirt", "parka", "vest",
        "cardigan", "bomber"
    ]
}


def normalize_category(raw: str) -> Optional[str]:
    """Map raw category to canonical type."""
    raw = raw.lower().strip()
    for canonical, variants in CATEGORY_MAP.items():
        if raw in variants:
            return canonical
        for variant in variants:
            if variant in raw or raw in variant:
                return canonical
    return None


def select_outfit_items(items: List[Dict]) -> Dict[str, Optional[Dict]]:
    """
    Select one item from each category.
    Returns dict with keys: top, pants, shoe, layer (any can be None).
    """
    buckets = {
        "top": [],
        "pants": [],
        "shoe": [],
        "layer": []
    }

    for item in items:
        category = normalize_category(item.get("category", ""))
        if category and category in buckets:
            buckets[category].append(item)

    outfit = {}
    for key, candidates in buckets.items():
        if candidates:
            outfit[key] = choice(candidates)
        else:
            outfit[key] = None

    return outfit


def validate_outfit(outfit: Dict[str, Optional[Dict]]) -> Tuple[bool, List[str]]:
    """
    Validate that outfit has minimum required items.
    Returns (is_valid, list_of_missing_items).

    We now only require EITHER top OR pants, not both.
    """
    has_top = outfit.get("top") is not None
    has_pants = outfit.get("pants") is not None

    # Need at least one essential item
    if not has_top and not has_pants:
        return False, ["top", "pants"]

    return True, []


def get_product_links(outfit: Dict[str, Optional[Dict]]) -> Dict[str, str]:
    """Extract product URLs from outfit items."""
    return {
        key: item.get("url")
        for key, item in outfit.items()
        if item and item.get("url")
    }


def filter_by_style(items: List[Dict], style: str) -> List[Dict]:
    """Filter items by style."""
    style_lower = style.lower()
    return [i for i in items if i.get("style", "").lower() == style_lower]


def filter_by_gender(items: List[Dict], gender: str) -> List[Dict]:
    """Filter items by gender."""
    gender_lower = gender.lower()
    return [
        i for i in items
        if i.get("gender", "").lower() in [gender_lower, "unisex"]
    ]


def filter_by_brand(items: List[Dict], brands: List[str]) -> List[Dict]:
    """Filter items by preferred brands."""
    if not brands:
        return items

    brand_set = {b.lower().replace(" ", "_").replace("-", "_") for b in brands}
    return [
        i for i in items
        if i.get("brand", "").lower().replace(" ", "_").replace("-", "_") in brand_set
    ]