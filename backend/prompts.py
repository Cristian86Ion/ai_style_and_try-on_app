import random
from datetime import datetime

from fit_rules import get_fit_for_body_type, determine_style_vibe, get_shoe_recommendation
from body_measurements import compute_body_measurements

# =============================================================================
# SEASON
# =============================================================================

def get_current_season() -> str:
    """FW: Sep-Feb, SS: Mar-Aug"""
    month = datetime.now().month
    return "FW" if month in [9, 10, 11, 12, 1, 2] else "SS"

def get_season_info() -> tuple:
    season = get_current_season()
    return season, "Fall/Winter" if season == "FW" else "Spring/Summer"

# =============================================================================
# HELPERS
# =============================================================================

def safe_get(item: dict, key: str, default: str = 'N/A') -> str:
    if not item:
        return default
    return item.get(key, default)

def safe_get_colors(item: dict) -> list:
    if not item:
        return ["black"]
    return item.get('colors') or ["black"]

# =============================================================================
# STYLE EXTRACTION
# =============================================================================

STYLE_EXTRACTOR = """Extract keywords from: "{style_description}"
User: {sex}, {age}yo, likes: {brands}
Return JSON: {{"style_keywords":["x"],"color_preferences":["x"]}}"""

def build_style_extraction_prompt(user_data: dict) -> str:
    return STYLE_EXTRACTOR.format(
        style_description=user_data.get('style_description', 'casual'),
        sex=user_data.get('sex', 'male'),
        age=user_data.get('age', 25),
        brands=", ".join(user_data.get('favorite_brands', [])) or "any"
    )

# =============================================================================
# DATABASE FILTERS
# =============================================================================

def build_semantic_filters(keywords: dict, user_data: dict, season: str) -> dict:
    sex = user_data.get('sex', 'male')

    style_map = {
        'casual': 'casual', 'sporty': 'sporty', 'sport': 'sporty',
        'formal': 'smart', 'elegant': 'smart', 'smart': 'smart',
        'streetwear': 'street', 'street': 'street', 'urban': 'street',
        'grunge': 'grunge', 'punk': 'grunge', 'classy': 'classy'
    }

    detected = 'casual'
    for kw in keywords.get('style_keywords', []):
        for key, val in style_map.items():
            if key in kw.lower():
                detected = val
                break

    filters = {'gender': 'man' if sex == 'male' else 'woman', 'style': detected}

    brands = user_data.get('favorite_brands', [])
    if brands:
        filters['brand'] = brands[0].lower().replace(' ', '_')

    return filters

# =============================================================================
# AI SHOE GENERATION
# =============================================================================

def generate_ai_shoe_description(style: str, gender: str, outfit_colors: list, season: str, body_type: str = "average") -> dict:
    rec = get_shoe_recommendation(body_type, style, gender)

    shoe_type = random.choice(rec["shoe_types"])
    material = random.choice(rec["materials"])

    # Color matching
    if outfit_colors:
        c = outfit_colors[0].lower().replace('_', ' ')
        if "black" in c or "dark" in c:
            color = "black"
        elif "brown" in c or "tan" in c:
            color = "brown"
        elif "navy" in c or "blue" in c:
            color = "navy"
        elif "white" in c or "cream" in c:
            color = "white"
        else:
            color = random.choice(rec["colors"])
    else:
        color = random.choice(rec["colors"])

    # FW = boots
    if season == "FW" and "sneaker" in shoe_type.lower():
        shoe_type = shoe_type.replace("sneaker", "boot")

    return {
        "description": f"{color} {material} {shoe_type}",
        "colors": [color],
        "fit": rec["fit_profile"],
        "is_ai_generated": True
    }

# =============================================================================
# BODY DESCRIPTION
# =============================================================================

def get_body_description(user_data: dict, measurements: dict) -> str:
    """Create body description with measurements. Gray skin."""
    sex = user_data.get('sex', 'male')
    body_type = user_data.get('body_type', 'average')
    height = user_data.get('height', 175)

    chest = measurements.get('chest_circumference', 95)
    waist = measurements.get('waist_circumference', 85)
    hips = measurements.get('hip_circumference', 95)

    gender = "male" if sex == "male" else "female"

    bodies = {
        "slim": f"slim {gender} with thin arms, thin legs, flat stomach, narrow {chest}cm chest",
        "athletic": f"athletic {gender} with toned muscular arms, defined legs, {chest}cm chest, {waist}cm waist",
        "muscular": f"muscular {gender} with big biceps, thick muscular legs, broad {chest}cm chest",
        "average": f"average {gender} with normal proportions, {chest}cm chest, {waist}cm waist",
        "stocky": f"stocky {gender} with thick arms, thick legs, {waist}cm waist, wide shoulders",
        "plus-size": f"plus-size {gender} with thick arms, thick legs, round {waist}cm belly, {hips}cm hips"
    }

    body = bodies.get(body_type, bodies["average"])

    if height < 165:
        body += ", short"
    elif height > 185:
        body += ", tall"

    return body

# =============================================================================
# CLOTHING FIT
# =============================================================================

def get_clothing_with_fit(item: dict, body_type: str, style_vibe: str, garment_type: str) -> str:
    """Get clothing description with proper fit for body type."""
    if not item:
        return ""

    color = safe_get_colors(item)[0].replace('_', ' ')
    category = item.get('category', 'garment')

    fit = get_fit_for_body_type(body_type, garment_type, style_vibe)

    # Plus-size/stocky = looser clothes
    if body_type in ["plus-size", "stocky"]:
        fit_desc = "loose comfortable"
    elif "loose" in fit.lower() or "relaxed" in fit.lower():
        fit_desc = "relaxed"
    else:
        fit_desc = ""

    if fit_desc:
        return f"{fit_desc} {color} {category}"
    return f"{color} {category}"

# =============================================================================
# OCCASION COLOR LOGIC
# =============================================================================

OCCASION_COLORS = {
    "evening": ["black", "dark navy", "burgundy", "charcoal", "deep purple"],
    "night": ["black", "dark navy", "burgundy", "charcoal", "deep purple"],
    "party": ["black", "burgundy", "gold", "silver", "deep red"],
    "formal": ["black", "navy", "charcoal", "dark grey", "white"],
    "business": ["navy", "charcoal", "black", "grey", "white"],
    "date": ["black", "burgundy", "navy", "deep green"],
    "casual": ["any"],  # no restriction
    "daytime": ["any"],
    "beach": ["white", "light blue", "beige", "pastels"],
    "summer": ["white", "light blue", "beige", "light colors"],
    "sport": ["black", "white", "grey", "bright colors"]
}

def get_occasion_from_style(style_description: str) -> str:
    """Detect occasion from style description."""
    style_lower = style_description.lower()

    for occasion in OCCASION_COLORS.keys():
        if occasion in style_lower:
            return occasion

    # Time-based keywords
    if any(word in style_lower for word in ["night", "evening", "dinner", "club"]):
        return "evening"
    if any(word in style_lower for word in ["office", "work", "meeting", "interview"]):
        return "business"
    if any(word in style_lower for word in ["date", "romantic"]):
        return "date"
    if any(word in style_lower for word in ["party", "celebration"]):
        return "party"

    return "casual"

def get_color_mood_for_occasion(occasion: str) -> str:
    """Get color mood description for prompt."""
    moods = {
        "evening": "dark elegant tones",
        "night": "dark sophisticated colors",
        "party": "rich bold colors",
        "formal": "classic professional colors",
        "business": "professional muted tones",
        "date": "romantic dark colors",
        "casual": "natural everyday colors",
        "beach": "light airy colors",
        "summer": "bright fresh colors",
        "sport": "dynamic colors"
    }
    return moods.get(occasion, "balanced colors")

# =============================================================================
# IMAGE PROMPT
# =============================================================================

def build_image_prompt(user_data: dict, selected_items: dict, ai_shoe: dict, measurements: dict, color_palette: dict = None) -> str:
    """
    Build prompt with:
    - Gray textured skin, NO face/lips/ears
    - Proper body proportions from measurements
    - Colorful clothes with fit rules
    - Occasion-based color mood
    - Full body head to toe
    """

    body_type = user_data.get('body_type', 'average')
    style_desc = user_data.get('style_description', 'casual')
    style_vibe = determine_style_vibe(style_desc)

    # Get occasion and color mood
    occasion = get_occasion_from_style(style_desc)
    color_mood = get_color_mood_for_occasion(occasion)

    # Body description with measurements
    body_desc = get_body_description(user_data, measurements)

    # Build clothes list with fit
    clothes = []

    top = selected_items.get('top')
    if top:
        clothes.append(get_clothing_with_fit(top, body_type, style_vibe, "tops"))

    pants = selected_items.get('pants')
    if pants:
        clothes.append(get_clothing_with_fit(pants, body_type, style_vibe, "pants"))

    layer = selected_items.get('layer')
    if layer:
        color = safe_get_colors(layer)[0].replace('_', ' ')
        clothes.append(f"{color} {layer.get('category', 'jacket')} worn open")

    if ai_shoe:
        clothes.append(ai_shoe.get('description', 'black shoes'))

    clothes_str = ", ".join(clothes)

    prompt = f"""{body_desc} person with gray skin, full body, wearing {clothes_str}.

SKIN: Gray(#808080) skin with realistic skin texture. !!!Smooth head with NO face, NO eyes, NO lips, NO ears, NO nose, NO hair. Just smooth gray head shape.
BODY: Gray neck, gray arms, gray hands with fingers, gray legs. Skin texture visible but gray colored.

OUTFIT: {clothes_str}
COLOR MOOD: {color_mood} (occasion: {occasion})

Clothes are colorful and vibrant (NOT gray). Only skin is gray.
Standing pose, arms relaxed at sides, facing camera.
Fashion catalog photo, studio lighting, clean white background.
Full body from top of head to bottom of shoes.
High quality fashion photography, photorealistic clothes."""

    return prompt

# =============================================================================
# STYLING TIPS
# =============================================================================

def build_styling_tips_prompt(user_data: dict, selected_items: dict, ai_shoe: dict = None, alt_palette: dict = None) -> str:
    season, season_name = get_season_info()
    top = selected_items.get('top') or {}
    pants = selected_items.get('pants') or {}

    shoe = ai_shoe.get('description', 'shoes') if ai_shoe else 'shoes'

    return f"""Style tip for: {safe_get(top,'brand')} {safe_get(top,'category')}, {safe_get(pants,'brand')} {safe_get(pants,'category')}, {shoe}.
Client: {user_data.get('age',25)}yo {user_data.get('sex','male')}, {user_data.get('body_type','average')}, {season_name}.
Give 2 short tips."""

# =============================================================================
# OUTFIT DESCRIPTION
# =============================================================================

def build_outfit_description(selected_items: dict, ai_shoe: dict = None) -> str:
    lines = []
    total = 0

    icons = {'top': '👕', 'pants': '👖', 'layer': '🧥'}

    for key in ['top', 'pants', 'layer']:
        item = selected_items.get(key)
        if item:
            colors = ", ".join(safe_get_colors(item))
            price = safe_get(item, 'price_eur', '0')
            url = item.get('url', '')

            lines.append(f"{icons[key]} {safe_get(item,'brand').title()} {safe_get(item,'category')} ({colors}) - €{price}")
            if url:
                lines.append(f"   🔗 {url}")

            try:
                total += float(price)
            except:
                pass

    if ai_shoe:
        lines.append(f"👟 {ai_shoe.get('description', 'Shoes')} (AI-styled)")

    if total > 0:
        lines.append(f"\n💰 Total: €{total:.0f}")

    return "\n".join(lines) if lines else "No items"

# =============================================================================
# VALIDATION
# =============================================================================

VALID_BODY_TYPES = ["slim", "athletic", "average", "muscular", "stocky", "plus-size"]

def validate_user_data(user_data: dict) -> bool:
    for field in ["sex", "age", "height", "weight", "body_type"]:
        if not user_data.get(field):
            raise ValueError(f"Missing: {field}")
    if user_data["body_type"] not in VALID_BODY_TYPES:
        raise ValueError(f"Invalid body_type")
    return True