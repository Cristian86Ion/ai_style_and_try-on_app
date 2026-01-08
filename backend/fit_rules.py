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
    """
    Get recommended fit based on body type, garment type, and style vibe.

    Args:
        body_type: slim, athletic, average, muscular, stocky, plus-size
        garment_type: "pants" or "tops"
        style_vibe: "elegant", "casual", or "smart-casual"

    Returns:
        Fit recommendation string
    """
    if body_type not in FIT_RULES:
        body_type = "average"

    if style_vibe not in ["elegant", "casual"]:
        style_vibe = "casual"

    rules = FIT_RULES[body_type]

    if garment_type == "pants":
        return rules["pants"][style_vibe]
    else:
        return rules["tops"][style_vibe]


def adjust_fit_size(base_fit: str, style_description: str, garment_type: str) -> str:
    """
    Adjusts fit based on user's explicit requests.

    Rules:
    - If user requests "oversized", make 30% larger
    - If user requests "slim fit", convert to regular fit
    - Otherwise keep base fit

    Args:
        base_fit: Base fit from FIT_RULES
        style_description: User's style description
        garment_type: "pants" or "tops"

    Returns:
        Adjusted fit string
    """
    style_lower = style_description.lower()

    # Check for oversized request
    oversized_keywords = ["oversized", "baggy", "loose", "relaxed fit", "big"]
    if garment_type == "tops" and any(word in style_lower for word in oversized_keywords):
        return "oversized (30% larger than standard)"

    # Check for slim request - convert to regular
    slim_keywords = ["slim", "fitted", "tight", "skinny"]
    if any(word in style_lower for word in slim_keywords):
        if garment_type == "pants":
            return "regular-fit (slim requested, using regular for proper fit)"
        else:
            return "regular-fit (slim requested, using regular for proper fit)"

    # Return base fit
    return base_fit


def determine_style_vibe(style_description: str) -> str:
    """
    Determines if style is elegant/formal or casual.

    Returns:
        "elegant" or "casual"
    """
    style_lower = style_description.lower()

    elegant_keywords = ["elegant", "formal", "sophisticated", "professional", "business", "refined"]
    casual_keywords = ["casual", "comfortable", "relaxed", "streetwear", "laid-back"]

    elegant_count = sum(1 for kw in elegant_keywords if kw in style_lower)
    casual_count = sum(1 for kw in casual_keywords if kw in style_lower)

    if elegant_count > casual_count:
        return "elegant"
    else:
        return "casual"


# =============================================================================
# TESTING
# =============================================================================

if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("FIT RULES TESTING")
    print("=" * 70 + "\n")

    # Test base fit rules
    test_cases = [
        {"body_type": "slim", "style": "elegant", "garment": "pants"},
        {"body_type": "slim", "style": "casual", "garment": "pants"},
        {"body_type": "athletic", "style": "elegant", "garment": "pants"},
        {"body_type": "athletic", "style": "casual", "garment": "pants"},
        {"body_type": "average", "style": "elegant", "garment": "pants"},
        {"body_type": "muscular", "style": "elegant", "garment": "tops"},
        {"body_type": "athletic", "style": "casual", "garment": "tops"},
    ]

    for test in test_cases:
        result = get_fit_for_body_type(
            test["body_type"],
            test["garment"],
            test["style"]
        )
        print(f"{test['body_type']:12s} + {test['style']:8s} + {test['garment']:5s} → {result}")

    print("\n" + "=" * 70)
    print("FIT ADJUSTMENT TESTING")
    print("=" * 70 + "\n")

    # Test fit adjustments
    adjustment_tests = [
        {
            "base_fit": "regular-fit",
            "style": "oversized streetwear",
            "garment": "tops",
            "expected": "oversized"
        },
        {
            "base_fit": "regular-fit",
            "style": "slim fit elegant",
            "garment": "pants",
            "expected": "regular (slim→regular)"
        },
        {
            "base_fit": "loose-fit",
            "style": "casual comfortable",
            "garment": "pants",
            "expected": "loose-fit (unchanged)"
        },
    ]

    for test in adjustment_tests:
        result = adjust_fit_size(
            test["base_fit"],
            test["style"],
            test["garment"]
        )
        print(f"Base: {test['base_fit']:20s} + Style: '{test['style']}'")
        print(f"   → Result: {result}")
        print(f"   Expected: {test['expected']}\n")

    print("=" * 70)
    print("✅ All tests completed!")
    print("=" * 70)