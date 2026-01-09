"""
Fit determination logic for outfit generation.
Defines rules for different body types and style preferences.
UPDATED VERSION - With size adjustment logic.
"""

# =============================================================================
# FIT RULES BY BODY TYPE
# =============================================================================

FIT_RULES = {
    "slim": {
        "pants": {
            "elegant": "regular-fit",
            "casual": "regular-fit",
            "description": "Regular fit works well for slim builds"
        },
        "tops": {
            "elegant": "regular-fit",
            "casual": "regular-fit",
            "description": "Regular fit highlights lean build without being too tight"
        },
        "notes": "Slim body type: regular fits work best. User can request oversized/slim for adjustments."
    },
    "athletic": {
        "pants": {
            "elegant": "regular-fit (regular upper leg, standard length)",
            "casual": "loose-fit (regular upper leg, looser lower leg, standard length)",
            "description": "Regular upper leg, standard length unless requested otherwise"
        },
        "tops": {
            "elegant": "regular-fit (room for shoulders)",
            "casual": "relaxed-fit",
            "description": "Room for athletic shoulders and chest"
        },
        "notes": "Athletic build needs regular/loose fits. Casual=loose, Elegant=regular. Standard length pants."
    },
    "average": {
        "pants": {
            "elegant": "regular-fit (standard length)",
            "casual": "loose-fit (standard length)",
            "description": "Versatile - regular fit, standard length"
        },
        "tops": {
            "elegant": "regular-fit",
            "casual": "relaxed-fit",
            "description": "Balanced proportions work with most fits"
        },
        "notes": "Average build is versatile. Casual=loose, Elegant=regular. Standard length pants."
    },
    "muscular": {
        "pants": {
            "elegant": "straight-fit with room in thighs (standard length)",
            "casual": "straight-fit with room in thighs (standard length)",
            "description": "Need room for muscle mass in thighs, standard length"
        },
        "tops": {
            "elegant": "regular-fit with room for chest/shoulders",
            "casual": "regular-fit with room for chest/shoulders",
            "description": "Room for developed chest and shoulders"
        },
        "notes": "Muscular build needs room. Avoid tight pants. Regular tops with space for muscle mass."
    },
    "stocky": {
        "pants": {
            "elegant": "straight-fit (standard length)",
            "casual": "straight-fit (standard length)",
            "description": "Straight fit, standard length"
        },
        "tops": {
            "elegant": "regular-fit",
            "casual": "relaxed-fit",
            "description": "Regular to relaxed, avoid tight"
        },
        "notes": "Stocky build works best with straight/regular fits. Standard length pants."
    },
    "plus-size": {
        "pants": {
            "elegant": "straight-fit for comfort (standard length)",
            "casual": "relaxed-fit for comfort (standard length)",
            "description": "Comfortable, flowing fits, standard length"
        },
        "tops": {
            "elegant": "relaxed-fit with flowing fabrics",
            "casual": "relaxed-fit",
            "description": "Comfortable, non-clingy fabrics"
        },
        "notes": "Plus-size build needs comfort. Straight/relaxed pants, relaxed tops. Standard length."
    }
}

# =============================================================================
# PANTS CUT OPTIONS
# =============================================================================

PANTS_CUTS = {
    "slim": {
        "name": "Slim Fit",
        "description": "Fitted through entire leg",
        "best_for": ["slim"],
        "keywords": ["slim", "fitted", "tight", "skinny"]
    },
    "regular": {
        "name": "Regular Fit",
        "description": "Regular upper leg, standard length",
        "best_for": ["slim", "athletic", "average"],
        "keywords": ["regular", "classic", "standard"]
    },
    "straight": {
        "name": "Straight Fit",
        "description": "Consistent width from hip to ankle",
        "best_for": ["athletic", "average", "muscular", "stocky"],
        "keywords": ["straight", "classic straight"]
    },
    "loose": {
        "name": "Loose Fit",
        "description": "Regular upper leg, looser lower leg - relaxed comfort",
        "best_for": ["athletic", "average", "muscular", "stocky", "plus-size"],
        "keywords": ["loose", "relaxed", "comfortable"]
    },
    "baggy": {
        "name": "Baggy / Wide-Leg",
        "description": "Very wide through entire leg, streetwear style",
        "best_for": ["all"],
        "keywords": ["baggy", "wide", "wide-leg", "oversized"]
    },
}

# =============================================================================
# TOP CUT OPTIONS
# =============================================================================

TOP_CUTS = {
    "regular": {
        "name": "Regular Fit",
        "description": "Classic fit with slight room",
        "best_for": ["all"],
        "keywords": ["regular", "classic", "standard"]
    },
    "relaxed": {
        "name": "Relaxed Fit",
        "description": "Comfortable with extra room",
        "best_for": ["athletic", "average", "muscular", "stocky", "plus-size"],
        "keywords": ["relaxed", "comfortable", "easy"]
    },
    "oversized": {
        "name": "Oversized",
        "description": "Intentionally large, 30% bigger than standard",
        "best_for": ["all"],
        "keywords": ["oversized", "loose", "baggy"]
    },
}

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_fit_for_body_type(body_type: str, garment_type: str, style_vibe: str) -> str:
    """Get recommended fit based on body type, garment type, and style vibe."""
    if body_type not in FIT_RULES:
        body_type = "average"
    if style_vibe not in ["elegant", "casual"]:
        style_vibe = "casual"
    rules = FIT_RULES[body_type]
    return rules["pants"][style_vibe] if garment_type == "pants" else rules["tops"][style_vibe]


def adjust_fit_size(base_fit: str, style_description: str, garment_type: str) -> str:
    """Adjusts fit based on user's explicit requests (oversized/slim)."""
    style_lower = style_description.lower()
    oversized_keywords = ["oversized", "baggy", "loose", "relaxed fit", "big"]
    if garment_type == "tops" and any(word in style_lower for word in oversized_keywords):
        return "oversized (30% larger than standard)"
    slim_keywords = ["slim", "fitted", "tight", "skinny"]
    if any(word in style_lower for word in slim_keywords):
        return "regular-fit (slim requested, using regular for proper fit)"
    return base_fit


def determine_style_vibe(style_description: str) -> str:
    """Determines if style is elegant/formal or casual."""
    style_lower = style_description.lower()
    elegant_keywords = ["elegant", "formal", "sophisticated", "professional", "business", "refined"]
    casual_keywords = ["casual", "comfortable", "relaxed", "streetwear", "laid-back"]
    elegant_count = sum(1 for kw in elegant_keywords if kw in style_lower)
    casual_count = sum(1 for kw in casual_keywords if kw in style_lower)
    return "elegant" if elegant_count > casual_count else "casual"


def get_age_styling_rules(age: int, style_vibe: str) -> str:
    """Return styling rules based on age."""
    if age < 25:
        return "Focus on bold silhouettes, contemporary layering, and trendy accessories."
    elif age < 45:
        return "Emphasize quality materials, well-proportioned tailoring, and sophisticated color palettes."
    else:
        return "Focus on timeless elegance, premium textures, and clean structured lines."


def get_accessories_rules(age: int, style_vibe: str) -> str:
    """Return accessory rules based on age and style."""
    if style_vibe == "elegant":
        return "Minimalist watch, leather belt, optional pocket square."
    return "Practical accessories: premium sunglasses or a structured backpack."
