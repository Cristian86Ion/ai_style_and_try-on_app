"""
Local module - JSON-based clothing database.
"""

from .local_store import load_all_items, get_items_by_category, get_items_by_brand, get_items_by_gender
from .local_query import query, semantic_query

__all__ = [
    'load_all_items',
    'get_items_by_category', 
    'get_items_by_brand',
    'get_items_by_gender',
    'query',
    'semantic_query'
]
