"""
Processor module - Clothing selection and outfit building.
"""

from .clotheselector import (
    select_outfit_items,
    validate_outfit,
    get_product_links,
    normalize_category,
    filter_by_style,
    filter_by_gender,
    filter_by_brand
)

__all__ = [
    'select_outfit_items',
    'validate_outfit',
    'get_product_links',
    'normalize_category',
    'filter_by_style',
    'filter_by_gender',
    'filter_by_brand'
]