"""
Local Store - Loads all clothing items from JSON files in the Haine folder.
Replaces PostgreSQL database for local development.
"""

import os
import json
from pathlib import Path
from typing import List, Dict

# Cache for loaded items
_items_cache: List[Dict] = []
_cache_loaded: bool = False


def get_haine_folder() -> Path:
    """Find the Haine folder relative to the backend."""
    # Try different possible locations
    possible_paths = [
        Path(__file__).parent.parent.parent / "Haine",  # /backend/local -> /Haine
        Path(__file__).parent.parent / "Haine",  # Alternative
        Path.cwd().parent / "Haine",  # From backend folder
        Path.cwd() / "Haine",  # From project root
        Path("/home/claude/project/Haine"),  # Absolute fallback
    ]

    for path in possible_paths:
        if path.exists() and path.is_dir():
            return path

    # Last resort: create it
    fallback = Path(__file__).parent.parent.parent / "Haine"
    fallback.mkdir(parents=True, exist_ok=True)
    return fallback


def load_all_items(force_reload: bool = False) -> List[Dict]:
    """
    Load all items from JSON files in the Haine folder and its subfolders.

    Structure expected:
    Haine/
    ├── zara.json
    ├── bershka.json
    ├── hm.json
    └── brand_folders/
        └── items.json
    """
    global _items_cache, _cache_loaded

    if _cache_loaded and not force_reload:
        return _items_cache

    items = []
    haine_folder = get_haine_folder()

    if not haine_folder.exists():
        print(f"⚠️ Haine folder not found at {haine_folder}")
        return []

    json_files = []

    # Find all JSON files
    for file in haine_folder.rglob("*.json"):
        # Skip node_modules, .next, etc.
        if any(skip in str(file) for skip in ["node_modules", ".next", "__pycache__"]):
            continue
        json_files.append(file)

    # Load each JSON file
    for json_file in json_files:
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

                if isinstance(data, list):
                    items.extend(data)
                elif isinstance(data, dict):
                    # Single item or wrapped list
                    if "items" in data:
                        items.extend(data["items"])
                    else:
                        items.append(data)

        except json.JSONDecodeError as e:
            print(f"⚠️ JSON error in {json_file.name}: {e}")
        except Exception as e:
            print(f"⚠️ Error loading {json_file.name}: {e}")

    # Ensure all items have required fields
    valid_items = []
    for item in items:
        if not isinstance(item, dict):
            continue

        # Ensure required fields exist
        if "id" not in item:
            continue

        # Normalize fields
        item.setdefault("brand", "unknown")
        item.setdefault("category", "unknown")
        item.setdefault("gender", "unisex")
        item.setdefault("colors", [])
        item.setdefault("style", "casual")
        item.setdefault("url", "")
        item.setdefault("price_eur", 0)

        # Ensure colors is a list
        if isinstance(item["colors"], str):
            item["colors"] = [item["colors"]]

        # Normalize price
        if isinstance(item["price_eur"], str):
            try:
                item["price_eur"] = float(item["price_eur"])
            except ValueError:
                item["price_eur"] = 0

        valid_items.append(item)

    _items_cache = valid_items
    _cache_loaded = True

    print(f"✓ Loaded {len(valid_items)} items from {len(json_files)} JSON files")

    return valid_items


def get_items_by_category(category: str) -> List[Dict]:
    """Get all items matching a category."""
    items = load_all_items()
    return [i for i in items if i.get("category", "").lower() == category.lower()]


def get_items_by_brand(brand: str) -> List[Dict]:
    """Get all items from a specific brand."""
    items = load_all_items()
    return [i for i in items if i.get("brand", "").lower() == brand.lower()]


def get_items_by_gender(gender: str) -> List[Dict]:
    """Get all items for a specific gender (man/woman/unisex)."""
    items = load_all_items()
    return [i for i in items if i.get("gender", "").lower() == gender.lower()]


def clear_cache():
    """Clear the items cache."""
    global _items_cache, _cache_loaded
    _items_cache = []
    _cache_loaded = False


# =============================================================================
# TESTING
# =============================================================================

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("📦 LOCAL STORE TEST")
    print("=" * 60 + "\n")

    items = load_all_items()

    print(f"\nTotal items: {len(items)}")

    # Category breakdown
    categories = {}
    for item in items:
        cat = item.get("category", "unknown")
        categories[cat] = categories.get(cat, 0) + 1

    print("\nCategories:")
    for cat, count in sorted(categories.items()):
        print(f"  • {cat}: {count}")

    # Brand breakdown
    brands = {}
    for item in items:
        brand = item.get("brand", "unknown")
        brands[brand] = brands.get(brand, 0) + 1

    print("\nBrands:")
    for brand, count in sorted(brands.items()):
        print(f"  • {brand}: {count}")

    # Sample item
    if items:
        print("\nSample item:")
        print(json.dumps(items[0], indent=2))
