"""
Local Query - Filters clothing items based on criteria.
Replaces PostgreSQL queries for local development.
"""

from typing import List, Dict, Optional


def query(items: List[Dict], filters: Dict) -> List[Dict]:
    """
    Filter items based on provided filters.

    Supported filters:
    - gender: "man" or "woman"
    - brand: brand name (e.g., "zara", "hm")
    - category: category name (e.g., "pants", "jacket")
    - style: style type (e.g., "casual", "sporty", "formal")
    - colors: single color or list of colors
    - price_min: minimum price (EUR)
    - price_max: maximum price (EUR)
    """
    results = items.copy()

    # Filter by gender
    if filters.get("gender"):
        gender = filters["gender"].lower()
        results = [
            i for i in results
            if i.get("gender", "").lower() == gender
               or i.get("gender", "").lower() == "unisex"
        ]

    # Filter by brand
    if filters.get("brand"):
        brand = filters["brand"].lower().replace("-", "_").replace(" ", "_")
        results = [
            i for i in results
            if i.get("brand", "").lower().replace("-", "_").replace(" ", "_") == brand
        ]

    # Filter by category
    if filters.get("category"):
        category = filters["category"].lower()
        results = [
            i for i in results
            if i.get("category", "").lower() == category
        ]

    # Filter by style
    if filters.get("style"):
        style = filters["style"].lower()
        results = [
            i for i in results
            if i.get("style", "").lower() == style
        ]

    # Filter by colors (any match)
    if filters.get("colors"):
        color_filter = filters["colors"]
        if isinstance(color_filter, str):
            color_filter = [color_filter]

        color_filter = [c.lower() for c in color_filter]

        def has_color(item):
            item_colors = item.get("colors", [])
            if isinstance(item_colors, str):
                item_colors = [item_colors]
            item_colors = [c.lower() for c in item_colors]

            for fc in color_filter:
                for ic in item_colors:
                    if fc in ic or ic in fc:
                        return True
            return False

        results = [i for i in results if has_color(i)]

    # Filter by price range
    if filters.get("price_min"):
        min_price = float(filters["price_min"])
        results = [
            i for i in results
            if float(i.get("price_eur", 0)) >= min_price
        ]

    if filters.get("price_max"):
        max_price = float(filters["price_max"])
        results = [
            i for i in results
            if float(i.get("price_eur", 0)) <= max_price
        ]

    return results


def semantic_query(items: List[Dict], keywords: Dict, user_data: Dict) -> List[Dict]:
    """
    Semantic search based on style keywords.

    keywords format:
    {
        "style_keywords": ["casual", "elegant"],
        "color_preferences": ["black", "navy"],
        "fit_preferences": ["regular", "loose"],
        "season_appropriate": ["jacket", "coat"]
    }
    """
    results = items.copy()

    # Filter by gender from user_data
    gender = "man" if user_data.get("sex") == "male" else "woman"
    results = [
        i for i in results
        if i.get("gender", "").lower() in [gender, "unisex"]
    ]

    # Score items based on style matches
    scored_results = []

    style_keywords = keywords.get("style_keywords", [])
    color_prefs = keywords.get("color_preferences", [])

    for item in results:
        score = 0

        # Style match
        item_style = item.get("style", "").lower()
        for kw in style_keywords:
            if kw.lower() in item_style or item_style in kw.lower():
                score += 3

        # Color match
        item_colors = item.get("colors", [])
        if isinstance(item_colors, str):
            item_colors = [item_colors]

        for pref in color_prefs:
            for color in item_colors:
                if pref.lower() in color.lower() or color.lower() in pref.lower():
                    score += 2
                    break

        # Brand preference
        fav_brands = user_data.get("favorite_brands", [])
        item_brand = item.get("brand", "").lower()
        for brand in fav_brands:
            if brand.lower() == item_brand:
                score += 5
                break

        scored_results.append((score, item))

    # Sort by score (highest first)
    scored_results.sort(key=lambda x: x[0], reverse=True)

    return [item for score, item in scored_results]


# =============================================================================
# TESTING
# =============================================================================

if __name__ == "__main__":
    # Test with sample data
    sample_items = [
        {"id": "1", "brand": "zara", "category": "pants", "gender": "man", "style": "casual",
         "colors": ["black", "navy"]},
        {"id": "2", "brand": "hm", "category": "t-shirt", "gender": "man", "style": "casual", "colors": ["white"]},
        {"id": "3", "brand": "zara", "category": "jacket", "gender": "woman", "style": "formal", "colors": ["black"]},
    ]

    print("Testing query function:")

    # Test gender filter
    results = query(sample_items, {"gender": "man"})
    print(f"Gender=man: {len(results)} items")

    # Test brand filter
    results = query(sample_items, {"brand": "zara"})
    print(f"Brand=zara: {len(results)} items")

    # Test combined filters
    results = query(sample_items, {"gender": "man", "style": "casual"})
    print(f"Gender=man + Style=casual: {len(results)} items")
