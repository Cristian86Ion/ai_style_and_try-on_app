# FIT RULES BY BODY TYPE

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
        "shoes": {
            "elegant": "sleek, streamlined silhouette",
            "casual": "clean minimal design",
            "description": "Slim-profile footwear complements lean frame"
        },
        "notes": "Slim body type: regular fits work best. Sleek shoes."
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
        "shoes": {
            "elegant": "structured supportive design",
            "casual": "athletic-inspired with good support",
            "description": "Supportive footwear for athletic builds"
        },
        "notes": "Athletic build needs regular/loose fits. Supportive shoes."
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
        "shoes": {
            "elegant": "versatile classic design",
            "casual": "comfortable balanced proportions",
            "description": "Standard proportions work with any shoe style"
        },
        "notes": "Average build is versatile. Standard shoes work well."
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
        "shoes": {
            "elegant": "substantial presence to balance muscular frame",
            "casual": "chunky athletic style for visual balance",
            "description": "Substantial footwear balances muscular proportions"
        },
        "notes": "Muscular build needs room. Substantial shoes for balance."
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
        "shoes": {
            "elegant": "proportional sturdy design",
            "casual": "solid comfortable construction",
            "description": "Proportional footwear, avoid too delicate styles"
        },
        "notes": "Stocky build works best with straight/regular fits. Solid shoes."
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
        "shoes": {
            "elegant": "comfortable supportive with cushioning",
            "casual": "wide-fit supportive design",
            "description": "Comfortable supportive footwear with good cushioning"
        },
        "notes": "Plus-size build needs comfort. Supportive comfortable shoes."
    }
}

# PANTS CUT OPTIONS

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

# TOP CUT OPTIONS

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

# SHOE STYLE OPTIONS BY OCCASION

SHOE_STYLES_BY_OCCASION = {
    "elegant": {
        "man": {
            "primary": ["oxford", "derby", "loafer", "monk strap"],
            "materials": ["polished leather", "suede", "patent leather"],
            "colors": ["black", "dark brown", "burgundy", "cognac"]
        },
        "woman": {
            "primary": ["pump", "loafer", "ankle boot", "ballet flat", "mule"],
            "materials": ["leather", "suede", "patent", "satin"],
            "colors": ["black", "nude", "burgundy", "navy"]
        }
    },
    "casual": {
        "man": {
            "primary": ["sneaker", "trainer", "slip-on", "desert boot"],
            "materials": ["leather", "suede", "canvas", "mesh"],
            "colors": ["white", "black", "gray", "navy", "tan"]
        },
        "woman": {
            "primary": ["sneaker", "trainer", "flat", "mule", "loafer"],
            "materials": ["leather", "canvas", "knit", "suede"],
            "colors": ["white", "black", "beige", "pink", "tan"]
        }
    },
    "street": {
        "man": {
            "primary": ["chunky sneaker", "high-top", "platform", "basketball shoe"],
            "materials": ["leather", "mesh", "suede", "synthetic"],
            "colors": ["white", "black", "multi-color", "neon accents"]
        },
        "woman": {
            "primary": ["platform sneaker", "chunky trainer", "high-top", "dad shoe"],
            "materials": ["leather", "mesh", "patent", "suede"],
            "colors": ["white", "black", "pink", "beige", "multi"]
        }
    },
    "sporty": {
        "man": {
            "primary": ["running shoe", "athletic trainer", "sport sneaker"],
            "materials": ["mesh", "knit", "synthetic", "foam"],
            "colors": ["white", "black", "gray", "neon", "blue"]
        },
        "woman": {
            "primary": ["running shoe", "athletic sneaker", "sport trainer"],
            "materials": ["mesh", "knit", "flyknit", "foam"],
            "colors": ["white", "black", "pink", "coral", "mint"]
        }
    },
    "grunge": {
        "man": {
            "primary": ["combat boot", "military boot", "platform boot", "chelsea boot"],
            "materials": ["distressed leather", "worn suede", "canvas"],
            "colors": ["black", "brown", "dark brown", "olive"]
        },
        "woman": {
            "primary": ["combat boot", "platform boot", "lace-up boot", "chunky boot"],
            "materials": ["leather", "patent", "distressed leather"],
            "colors": ["black", "burgundy", "brown", "olive"]
        }
    },
    "classy": {
        "man": {
            "primary": ["italian oxford", "premium loafer", "dress boot", "brogue"],
            "materials": ["italian leather", "premium suede", "cordovan"],
            "colors": ["black", "cognac", "burgundy", "chocolate"]
        },
        "woman": {
            "primary": ["stiletto", "kitten heel", "slingback", "elegant mule"],
            "materials": ["fine leather", "suede", "satin", "silk"],
            "colors": ["black", "nude", "red", "gold", "silver"]
        }
    }
}

# SHOE FIT RULES BY BODY TYPE

SHOE_FIT_BY_BODY_TYPE = {
    "slim": {
        "profile": "sleek, streamlined",
        "avoid": "overly chunky or heavy",
        "recommendation": "Clean lines that complement lean frame"
    },
    "athletic": {
        "profile": "supportive, structured",
        "avoid": "too narrow or delicate",
        "recommendation": "Good arch support with room for movement"
    },
    "average": {
        "profile": "versatile, balanced",
        "avoid": "extremes in either direction",
        "recommendation": "Standard proportions work well"
    },
    "muscular": {
        "profile": "substantial, grounded",
        "avoid": "too delicate or slim profile",
        "recommendation": "Visual weight to balance muscular frame"
    },
    "stocky": {
        "profile": "proportional, solid",
        "avoid": "overly delicate or thin soles",
        "recommendation": "Sturdy construction with good support"
    },
    "plus-size": {
        "profile": "wide-fit, cushioned",
        "avoid": "narrow toe boxes or thin soles",
        "recommendation": "Extra cushioning and support essential"
    }
}

# HELPER FUNCTIONS

def get_fit_for_body_type(body_type: str, garment_type: str, style_vibe: str) -> str:
  #outfit based on personal style
    if body_type not in FIT_RULES:
        body_type = "average"
    if style_vibe not in ["elegant", "casual"]:
        style_vibe = "casual"
    rules = FIT_RULES[body_type]

    if garment_type == "pants":
        return rules["pants"][style_vibe]
    elif garment_type == "shoes":
        return rules["shoes"][style_vibe]
    else:
        return rules["tops"][style_vibe]


def get_shoe_recommendation(body_type: str, style: str, gender: str) -> dict:

    if body_type not in SHOE_FIT_BY_BODY_TYPE:
        body_type = "average"

    # Map style
    style_map = {
        "smart": "elegant",
        "formal": "elegant",
        "casual": "casual",
        "street": "street",
        "sporty": "sporty",
        "grunge": "grunge",
        "classy": "classy"
    }
    occasion = style_map.get(style.lower(), "casual")

    # Get fit recommendation
    fit_rec = SHOE_FIT_BY_BODY_TYPE[body_type]

    # Get style options
    gender_key = "woman" if gender.lower() in ["woman", "female"] else "man"
    style_options = SHOE_STYLES_BY_OCCASION.get(occasion, SHOE_STYLES_BY_OCCASION["casual"])
    gender_styles = style_options.get(gender_key, style_options["man"])

    return {
        "fit_profile": fit_rec["profile"],
        "avoid": fit_rec["avoid"],
        "recommendation": fit_rec["recommendation"],
        "shoe_types": gender_styles["primary"],
        "materials": gender_styles["materials"],
        "colors": gender_styles["colors"]
    }

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
    # elegant/formal
    style_lower = style_description.lower()
    elegant_keywords = ["elegant", "formal", "sophisticated", "professional", "business", "refined"]
    casual_keywords = ["casual", "comfortable", "relaxed", "streetwear", "laid-back"]
    elegant_count = sum(1 for kw in elegant_keywords if kw in style_lower)
    casual_count = sum(1 for kw in casual_keywords if kw in style_lower)
    return "elegant" if elegant_count > casual_count else "casual"


def get_age_styling_rules(age: int, style_vibe: str) -> str:
    # style related to age
    if age < 25:
        return "Focus on bold silhouettes, contemporary layering, and trendy accessories."
    elif age < 45:
        return "Emphasize quality materials, well-proportioned tailoring, and sophisticated color palettes."
    else:
        return "Focus on timeless elegance, premium textures, and clean structured lines."


def get_accessories_rules(age: int, style_vibe: str) -> str:
    # accessories based on age
    if style_vibe == "elegant":
        return "Minimalist watch, leather belt, optional pocket square."
    return "Practical accessories: premium sunglasses or a structured backpack."


def get_shoe_styling_prompt(body_type: str, style: str, gender: str, outfit_colors: list) -> str:
    #shoe recommendation
    rec = get_shoe_recommendation(body_type, style, gender)

    if outfit_colors:
        # Find a matching or complementary color
        outfit_primary = outfit_colors[0].lower() if outfit_colors else "black"
        if "black" in outfit_primary:
            shoe_color = "black"
        elif "brown" in outfit_primary or "tan" in outfit_primary:
            shoe_color = "brown or tan"
        elif "navy" in outfit_primary or "blue" in outfit_primary:
            shoe_color = "navy or dark blue"
        else:
            shoe_color = "neutral (black, white, or brown)"
    else:
        import random
        shoe_color = random.choice(rec["colors"])

    import random
    shoe_type = random.choice(rec["shoe_types"])
    material = random.choice(rec["materials"])

    return f"""
SHOE SPECIFICATION:
Type: {shoe_type}
Material: {material}
Color: {shoe_color}
Fit Profile: {rec["fit_profile"]}
Style Note: {rec["recommendation"]}

RENDERING: Photorealistic, high-detail, proper proportions for body type.
"""