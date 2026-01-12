from datetime import datetime
from typing import List, Dict, Tuple
import random

# =============================================================================
# SEASONAL LOGIC
# =============================================================================

def get_current_season() -> str:
    #FW: Sep-Feb (months 9-12, 1-2), SS: Mar-Aug (months 3-8)
    current_month = datetime.now().month
    return "FW" if (current_month >= 9 or current_month <= 2) else "SS"

def get_seasonal_description() -> str:

    season = get_current_season()
    if season == "FW":
        return "Fall/Winter: Layering, rich textures (wool, cashmere, leather), deeper tones, structured silhouettes."
    else:
        return "Spring/Summer: Breathable fabrics (linen, cotton, silk), lighter colors, relaxed fits, minimal layering."

# =============================================================================
# COLOR PALETTES - 30 TOTAL (15 FW + 15 SS)
# =============================================================================

SANZO_WADA_PALETTES = {
    # FALL/WINTER PALETTES (15)

    "FW_CLASSIC_NOIR": {
        "name": "Classic Noir",
        "colors": ["Charcoal (#36454F)", "Deep Navy (#000080)", "Burgundy (#800020)"],
        "season": "FW",
        "mood": "classic",
        "keywords": ["elegant", "formal", "sophisticated", "business", "minimal", "professional", "suit"]
    },

    "FW_WINTER_FOREST": {
        "name": "Winter Forest",
        "colors": ["Forest Green (#228B22)", "Chocolate Brown (#3B2414)", "Charcoal (#36454F)"],
        "season": "FW",
        "mood": "outdoor",
        "keywords": ["outdoor", "rugged", "natural", "adventure", "hiking", "camping", "wilderness"]
    },

    "FW_LUXE_JEWEL": {
        "name": "Luxe Jewel",
        "colors": ["Emerald (#50C878)", "Royal Purple (#7851A9)", "Gold (#D4AF37)"],
        "season": "FW",
        "mood": "bold",
        "keywords": ["luxury", "bold", "party", "evening", "statement", "glamorous", "rich"]
    },

    "FW_URBAN_STEEL": {
        "name": "Urban Steel",
        "colors": ["Graphite (#383428)", "Steel Blue (#4682B4)", "Silver (#C0C0C0)"],
        "season": "FW",
        "mood": "modern",
        "keywords": ["urban", "modern", "tech", "minimalist", "industrial", "contemporary", "sleek"]
    },

    "FW_COZY_NEUTRAL": {
        "name": "Cozy Neutral",
        "colors": ["Camel (#C19A6B)", "Cream (#FFFDD0)", "Taupe (#483C32)"],
        "season": "FW",
        "mood": "neutral",
        "keywords": ["cozy", "comfortable", "neutral", "versatile", "timeless", "soft", "warm"]
    },

    "FW_MIDNIGHT_DEPTH": {
        "name": "Midnight Depth",
        "colors": ["Midnight Blue (#191970)", "Slate Gray (#708090)", "Bone White (#F9F6EE)"],
        "season": "FW",
        "mood": "sophisticated",
        "keywords": ["elegant", "refined", "dark", "mysterious", "sophisticated", "evening", "noir"]
    },

    "FW_TERRACOTTA_WARMTH": {
        "name": "Terracotta Warmth",
        "colors": ["Terracotta (#E2725B)", "Mustard (#FFDB58)", "Clay Brown (#B66325)"],
        "season": "FW",
        "mood": "warm",
        "keywords": ["warm", "inviting", "rustic", "mediterranean", "cozy", "homey", "earthy"]
    },

    "FW_CHARCOAL_REFINED": {
        "name": "Charcoal Refined",
        "colors": ["Charcoal (#36454F)", "Ash Gray (#B2BEB5)", "Ivory (#FFFFF0)"],
        "season": "FW",
        "mood": "minimal",
        "keywords": ["minimal", "clean", "refined", "professional", "sleek", "modern", "monochrome"]
    },

    "FW_BURGUNDY_HERITAGE": {
        "name": "Burgundy Heritage",
        "colors": ["Burgundy (#800020)", "Navy (#000080)", "Beige (#F5F5DC)"],
        "season": "FW",
        "mood": "classic",
        "keywords": ["classic", "heritage", "traditional", "ivy", "preppy", "collegiate", "timeless"]
    },

    "FW_MILITARY_OLIVE": {
        "name": "Military Olive",
        "colors": ["Olive Drab (#6B8E23)", "Khaki (#C3B091)", "Black (#000000)"],
        "season": "FW",
        "mood": "utilitarian",
        "keywords": ["military", "utilitarian", "tactical", "practical", "rugged", "workwear", "cargo"]
    },

    "FW_ESPRESSO_TONES": {
        "name": "Espresso Tones",
        "colors": ["Espresso (#4E312D)", "Latte (#C9A88F)", "Cream (#FFFDD0)"],
        "season": "FW",
        "mood": "warm",
        "keywords": ["warm", "coffee", "neutral", "comfortable", "rich", "inviting", "brown"]
    },

    "FW_PLUM_TWILIGHT": {
        "name": "Plum Twilight",
        "colors": ["Plum (#8E4585)", "Charcoal (#36454F)", "Mauve (#E0B0FF)"],
        "season": "FW",
        "mood": "artistic",
        "keywords": ["artistic", "creative", "unique", "expressive", "bold", "unconventional", "purple"]
    },

    "FW_TEAL_DEPTH": {
        "name": "Teal Depth",
        "colors": ["Teal (#008080)", "Gray (#808080)", "Cream (#FFFDD0)"],
        "season": "FW",
        "mood": "fresh",
        "keywords": ["fresh", "modern", "cool", "balanced", "calm", "sophisticated", "blue-green"]
    },

    "FW_MONOCHROME_EDGE": {
        "name": "Monochrome Edge",
        "colors": ["Black (#000000)", "White (#FFFFFF)", "Concrete Gray (#95918E)"],
        "season": "FW",
        "mood": "stark",
        "keywords": ["minimal", "stark", "bold", "graphic", "modern", "architectural", "black"]
    },

    "FW_CRIMSON_POWER": {
        "name": "Crimson Power",
        "colors": ["Crimson Red (#DC143C)", "Charcoal (#36454F)", "Ivory (#FFFFF0)"],
        "season": "FW",
        "mood": "bold",
        "keywords": ["bold", "powerful", "statement", "confident", "red", "striking", "dramatic"]
    },

    # =========================================================================
    # SPRING/SUMMER PALETTES (15)
    # =========================================================================

    "SS_COASTAL_BREEZE": {
        "name": "Coastal Breeze",
        "colors": ["Sky Blue (#87CEEB)", "Sandy Beige (#F5DEB3)", "Seafoam (#93E9BE)"],
        "season": "SS",
        "mood": "fresh",
        "keywords": ["beach", "vacation", "relaxed", "coastal", "light", "airy", "blue"]
    },

    "SS_PASTEL_DREAM": {
        "name": "Pastel Dream",
        "colors": ["Blush Pink (#FFB6C1)", "Lavender (#E6E6FA)", "Mint (#98FF98)"],
        "season": "SS",
        "mood": "soft",
        "keywords": ["romantic", "soft", "feminine", "gentle", "dreamy", "delicate", "pastel"]
    },

    "SS_CITRUS_POP": {
        "name": "Citrus Pop",
        "colors": ["Lemon Yellow (#FFF44F)", "Coral (#FF7F50)", "Lime (#BFFF00)"],
        "season": "SS",
        "mood": "vibrant",
        "keywords": ["bright", "energetic", "fun", "playful", "bold", "cheerful", "yellow"]
    },

    "SS_MINIMALIST_WHITE": {
        "name": "Minimalist White",
        "colors": ["Pure White (#FFFFFF)", "Light Gray (#D3D3D3)", "Soft Ivory (#FFFFF0)"],
        "season": "SS",
        "mood": "minimal",
        "keywords": ["minimal", "clean", "simple", "elegant", "modern", "pure", "white"]
    },

    "SS_GARDEN_BLOOM": {
        "name": "Garden Bloom",
        "colors": ["Rose Pink (#FF007F)", "Sage Green (#9DC183)", "Buttercream (#FFFACD)"],
        "season": "SS",
        "mood": "natural",
        "keywords": ["floral", "garden", "natural", "fresh", "spring", "botanical", "feminine"]
    },

    "SS_TROPICAL_SUNSET": {
        "name": "Tropical Sunset",
        "colors": ["Tangerine (#F28500)", "Turquoise (#40E0D0)", "Fuchsia (#FF00FF)"],
        "season": "SS",
        "mood": "bold",
        "keywords": ["tropical", "vacation", "sunset", "bold", "exotic", "vibrant", "colorful"]
    },

    "SS_NAUTICAL_STRIPE": {
        "name": "Nautical Stripe",
        "colors": ["Navy Blue (#000080)", "White (#FFFFFF)", "Red (#FF0000)"],
        "season": "SS",
        "mood": "classic",
        "keywords": ["nautical", "maritime", "classic", "preppy", "sailing", "beach", "striped"]
    },

    "SS_LINEN_NATURAL": {
        "name": "Linen Natural",
        "colors": ["Natural Linen (#FAF0E6)", "Sand (#C2B280)", "Stone Gray (#928E85)"],
        "season": "SS",
        "mood": "neutral",
        "keywords": ["natural", "neutral", "organic", "minimal", "relaxed", "earthy", "beige"]
    },

    "SS_AQUA_REFRESH": {
        "name": "Aqua Refresh",
        "colors": ["Aquamarine (#7FFFD4)", "White (#FFFFFF)", "Periwinkle (#CCCCFF)"],
        "season": "SS",
        "mood": "cool",
        "keywords": ["cool", "refreshing", "water", "clean", "bright", "summery", "aqua"]
    },

    "SS_PEACH_SORBET": {
        "name": "Peach Sorbet",
        "colors": ["Peach (#FFCBA4)", "Cream (#FFFDD0)", "Light Pink (#FFB6C1)"],
        "season": "SS",
        "mood": "soft",
        "keywords": ["soft", "sweet", "gentle", "feminine", "warm", "delicate", "peach"]
    },

    "SS_MINT_FRESH": {
        "name": "Mint Fresh",
        "colors": ["Mint Green (#98FF98)", "White (#FFFFFF)", "Light Teal (#AFEEEE)"],
        "season": "SS",
        "mood": "fresh",
        "keywords": ["fresh", "clean", "cool", "minty", "light", "breezy", "green"]
    },

    "SS_SUNSET_SAND": {
        "name": "Sunset Sand",
        "colors": ["Burnt Orange (#CC5500)", "Sand (#C2B280)", "Sky Blue (#87CEEB)"],
        "season": "SS",
        "mood": "warm",
        "keywords": ["sunset", "beach", "warm", "golden", "vacation", "desert", "orange"]
    },

    "SS_LAVENDER_FIELD": {
        "name": "Lavender Field",
        "colors": ["Lavender (#E6E6FA)", "Sage (#BCB88A)", "Cream (#FFFDD0)"],
        "season": "SS",
        "mood": "serene",
        "keywords": ["serene", "calm", "peaceful", "provence", "floral", "herbal", "purple"]
    },

    "SS_OCEAN_DEPTH": {
        "name": "Ocean Depth",
        "colors": ["Deep Teal (#00555A)", "Foam White (#F8F8FF)", "Sand (#C2B280)"],
        "season": "SS",
        "mood": "sophisticated",
        "keywords": ["ocean", "sophisticated", "deep", "elegant", "coastal", "refined", "teal"]
    },

    "SS_PAPAYA_SUNRISE": {
        "name": "Papaya Sunrise",
        "colors": ["Papaya (#FFEFD5)", "Coral (#FF7F50)", "Ivory (#FFFFF0)"],
        "season": "SS",
        "mood": "warm",
        "keywords": ["tropical", "warm", "sunrise", "cheerful", "bright", "fruity", "coral"]
    }
}

# =============================================================================
# ENHANCED PALETTE SELECTION WITH DIVERSITY
# =============================================================================

# Track recently used palettes to avoid repetition
_recent_palettes = []
_MAX_RECENT = 5

def get_palettes_for_season(season: str) -> Dict[str, dict]:
    """Filters palettes by season."""
    return {k: v for k, v in SANZO_WADA_PALETTES.items() if v["season"] == season}

def match_palette_to_keywords(style_keywords: List[str], season: str, avoid_recent: bool = True) -> dict:
    """
    Enhanced matching with diversity - avoids recently used palettes.
    """
    seasonal_palettes = get_palettes_for_season(season)

    if not seasonal_palettes:
        return list(SANZO_WADA_PALETTES.values())[0]

    # Filter out recently used palettes if diversity is enabled
    if avoid_recent and _recent_palettes:
        available = {k: v for k, v in seasonal_palettes.items()
                    if k not in _recent_palettes}
        if available:
            seasonal_palettes = available

    # Score each palette based on keyword matches
    scored_palettes = []
    for palette_key, palette in seasonal_palettes.items():
        score = 0
        # Exact keyword matches
        for keyword in style_keywords:
            keyword_lower = keyword.lower()
            for palette_keyword in palette["keywords"]:
                if keyword_lower in palette_keyword or palette_keyword in keyword_lower:
                    score += 2  # Exact match gets higher score
                elif any(word in palette_keyword for word in keyword_lower.split()):
                    score += 1  # Partial match

        # Bonus for mood match
        if any(mood in ' '.join(style_keywords).lower()
               for mood in [palette["mood"]]):
            score += 3

        scored_palettes.append((score, palette_key, palette))

    # Sort by score, then add randomness for variety
    scored_palettes.sort(key=lambda x: (x[0], random.random()), reverse=True)

    # Get top matches
    if scored_palettes and scored_palettes[0][0] > 0:
        # Use top scored palette
        selected = scored_palettes[0][2]
        palette_key = scored_palettes[0][1]
    else:
        # No matches - pick random to ensure variety
        palette_key = random.choice(list(seasonal_palettes.keys()))
        selected = seasonal_palettes[palette_key]

    # Track usage
    _recent_palettes.append(palette_key)
    if len(_recent_palettes) > _MAX_RECENT:
        _recent_palettes.pop(0)

    return selected

def get_two_color_palettes(style_keywords: List[str]) -> Tuple[dict, dict]:
    """
    Returns TWO different palettes for current season with enhanced diversity.
    Primary for outfit, alternative for tips.
    """
    current_season = get_current_season()
    seasonal_palettes = get_palettes_for_season(current_season)

    if len(seasonal_palettes) < 2:
        all_palettes = list(SANZO_WADA_PALETTES.values())
        return all_palettes[0], all_palettes[1]

    # Get primary palette with diversity
    primary = match_palette_to_keywords(style_keywords, current_season, avoid_recent=True)

    # Get alternative - must be different name AND different mood
    alternative_options = [
        p for p in seasonal_palettes.values()
        if p["name"] != primary["name"] and p["mood"] != primary["mood"]
    ]

    if not alternative_options:
        # Fallback - just different name
        alternative_options = [
            p for p in seasonal_palettes.values()
            if p["name"] != primary["name"]
        ]

    if alternative_options:
        # Add randomness to alternative selection
        alternative = random.choice(alternative_options)
    else:
        alternative = primary

    return primary, alternative

def format_color_palette_for_prompt(palette: dict, include_hex: bool = True) -> str:
    """Formats palette for LLM prompt."""
    if include_hex:
        colors_str = ", ".join(palette["colors"])
    else:
        colors_str = ", ".join([
            color.split(" (#")[0] if " (#" in color else color
            for color in palette["colors"]
        ])

    return f"{palette['name']}: {colors_str}"

# =============================================================================
# TESTING
# =============================================================================

if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("SANZO WADA COLOR PALETTES - 30 TOTAL")
    print("=" * 70 + "\n")

    current_season = get_current_season()
    current_month = datetime.now().month

    print(f"Current: {datetime.now().strftime('%B %d, %Y')} (Month {current_month})")
    print(f"Season: {'Fall/Winter (FW)' if current_season == 'FW' else 'Spring/Summer (SS)'}\n")

    # Count palettes
    fw_count = len(get_palettes_for_season("FW"))
    ss_count = len(get_palettes_for_season("SS"))
    print(f"Total Palettes: {len(SANZO_WADA_PALETTES)}")
    print(f"   • Fall/Winter: {fw_count}")
    print(f"   • Spring/Summer: {ss_count}\n")

    # Test diversity
    print(f"{'=' * 70}")
    print(f"TESTING DIVERSITY (10 consecutive requests)")
    print(f"{'=' * 70}\n")

    test_styles = [
        ["casual", "comfortable"],
        ["elegant", "formal"],
        ["sporty", "athletic"],
        ["minimal", "clean"],
        ["bold", "colorful"],
        ["casual", "relaxed"],
        ["professional", "business"],
        ["outdoor", "rugged"],
        ["artistic", "creative"],
        ["classic", "timeless"]
    ]

    for i, style in enumerate(test_styles, 1):
        primary, alternative = get_two_color_palettes(style)
        print(f"{i:2d}. Style: {', '.join(style):20s} → {primary['name']}")

    print(f"\n Diversity test complete - palettes should vary!")