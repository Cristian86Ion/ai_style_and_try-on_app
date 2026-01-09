
from sanzo_wada_colors import get_two_color_palettes, format_color_palette_for_prompt, get_current_season
from fit_rules import get_fit_for_body_type, determine_style_vibe
from datetime import datetime

# =============================================================================
# BODY TYPE VISUAL CORRELATION (Height + Weight + Body Type)
# =============================================================================

def get_body_visual_description(height: int, weight: int, body_type: str, sex: str) -> str:
    """Generate precise body description based on measurements."""
    bmi = weight / ((height / 100) ** 2)

    base_descriptions = {
        "slim": f"Lean {sex} frame ({height}cm, {weight}kg, BMI {bmi:.1f}). Narrow shoulders, minimal body fat, thin limbs.",
        "average": f"Balanced {sex} build ({height}cm, {weight}kg, BMI {bmi:.1f}). Standard proportions, moderate frame.",
        "athletic": f"Athletic {sex} build ({height}cm, {weight}kg, BMI {bmi:.1f}). Defined muscles, V-shaped torso, lean.",
        "muscular": f"Muscular {sex} build ({height}cm, {weight}kg, BMI {bmi:.1f}). Broad shoulders, developed chest, thick limbs.",
        "stocky": f"Stocky {sex} build ({height}cm, {weight}kg, BMI {bmi:.1f}). Solid frame, muscle with fat layer, broad torso.",
        "plus-size": f"Plus-size {sex} ({height}cm, {weight}kg, BMI {bmi:.1f}). Fuller figure, soft contours."
    }

    description = base_descriptions.get(body_type, base_descriptions["average"])

    # Add sex-specific fat distribution for plus-size
    if body_type == "plus-size":
        if sex == "female":
            description += " Fat distributed in hips, thighs (thicker legs), and bust. Pear or hourglass shape."
        else:
            description += " Fat concentrated in stomach area (belly), chest, and face. Apple shape with protruding abdomen."

    return description

FIT_MULTIPLIERS = {
    "slim": "1.7x larger",
    "average": "1.8x larger",
    "athletic": "1.8x larger",
    "muscular": "1.9x larger",
    "stocky": "2.5x larger",
    "plus-size": "2.6x larger"
}

# =============================================================================
# OUTFIT GENERATION PROMPT (Step 1)
# =============================================================================

OUTFIT_PROMPT = """Generate outfit with EXPLICIT colors.

CLIENT: {age}yo {sex}, {height}cm, {weight}kg, {body_type}
DATE: {date}
SEASON: {season} ({season_name})
STYLE: {style_description}
BRANDS: {brands}

COLORS (MANDATORY): {color_palette}
BOTTOMS: Navy, Black, Charcoal, Khaki, Beige

FIT: Bottoms={pants_fit}, Tops={tops_fit}, Size={fit_multiplier}

FORMAT (4-6 sentences):
1. TOP: "[COLOR] [fabric] [neckline type], relaxed"
2. BOTTOMS: "[COLOR] [fabric] [type], full-length to shoes"
3. FOOTWEAR: "[COLOR] [material] [shoe type]" (MANDATORY)
4. {layering_instruction}
5. ACCESSORIES: {accessories}

{female_note}

CRITICAL: Name EXACT color for EVERY item. Example: "Sky Blue cotton crewneck" NOT "light top".
"""

# =============================================================================
# IMAGE COMPILER PROMPT (Step 2) - COST OPTIMIZED
# =============================================================================

IMAGE_COMPILER = """Convert to Flux prompt. Match outfit EXACTLY.

INPUT:
{sex}, {age}yo, {height}cm, {weight}kg, {body_type}
Body: {body_visual}
Outfit: {outfit_description}

FLUX PROMPT:

Professional fashion photo. Gray mannequin (#808080) FULLY CLOTHED, A-pose, front view.

MANNEQUIN:
- Featureless gray head/neck/hands (#808080) - smooth, NO face
- {sex} {body_type} build, {height}cm
- {body_shape_note}
- Body 100% HIDDEN by clothing

POSE:
- Standing, frontal, arms 20° from sides
- Hands OUTSIDE pockets, visible
- Feet parallel, shoulder-width

OUTFIT (EXACT):
{outfit_description}

FIT: {fit_multiplier} - loose draping, natural folds, deep shadows
PANTS: Full-length covering ankles, stacking at shoes
SHOES: Volumetric 3D {shoe_color} shoes, NO gray feet visible, thick soles (2-4cm)
COLORS: Vibrant, saturated, match description exactly
LIGHTING: Studio 3-point, soft shadows
BACKGROUND: Light gray (RGB 220,220,220)

CRITICAL:
✓ Gray head/neck/hands visible
✓ Body/arms/legs 100% hidden
✓ Hands outside pockets
✓ Shoes fully visible and colored
✓ All garments present
✓ Colors match exactly
"""

# =============================================================================
# STYLING TIPS PROMPT (Step 3)
# =============================================================================

TIPS_PROMPT = """50-word max seasonal tip.

SEASON: {season}
CLIENT: {age}yo {sex}, {body_type}
ALTERNATIVE: {alternative_palette}

Include: fabrics, silhouettes, 3 colors. Professional. Max 50 words.
"""

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_season_info() -> tuple:
    """Get current season with full name."""
    season = get_current_season()
    season_name = "Fall/Winter" if season == "FW" else "Spring/Summer"
    return season, season_name

def get_layering_instruction(season: str, style_vibe: str) -> str:
    """Layering rules based on season."""
    if season == "FW":
        if style_vibe == "elegant":
            return "LAYER: \"[COLOR] [fabric] blazer/coat\" (MANDATORY for F/W)"
        return "LAYER: \"[COLOR] [fabric] jacket\" (MANDATORY for F/W)"
    return "OUTERWEAR: Optional light jacket if desired"

def get_accessories(age: int, style_vibe: str) -> str:
    """Age-appropriate accessories."""
    if age < 20:
        return "Watch, belt only" if style_vibe == "elegant" else "Minimal accessories"
    return "Watch, belt, optional tie (if elegant)"

def get_body_shape_note(body_type: str, sex: str) -> str:
    """Body shape notes for image generation."""
    if body_type == "plus-size":
        if sex == "female":
            return "CRITICAL: Thicker legs (fat in thighs), wider hips, fuller figure"
        else:
            return "CRITICAL: Protruding stomach (belly fat), broader midsection, rounded torso"
    return "Standard proportions for body type"

def extract_shoe_color(outfit_description: str) -> str:
    """Extract shoe color from outfit description for emphasis."""
    # Look for shoe color mentions
    words = outfit_description.lower().split()
    common_shoes = ["sneakers", "boots", "loafers", "oxfords", "shoes"]

    for i, word in enumerate(words):
        if any(shoe in word for shoe in common_shoes):
            # Get color word before shoe type
            if i > 0:
                return words[i-1].capitalize()

    return "Black"  # Default

# =============================================================================
# PROMPT BUILDERS
# =============================================================================

def build_outfit_generation_prompt(user_data: dict, measurements: dict) -> str:
    """Build outfit prompt - optimized for low token count."""

    # Extract data
    style_description = user_data.get("style_description", "casual")
    body_type = user_data.get("body_type", "average")
    height = user_data.get("height", 170)
    weight = user_data.get("weight", 70)
    sex = user_data.get("sex", "male")
    age = user_data.get("age", 25)
    brands = ", ".join(user_data.get("favorite_brands", [])) or "None"

    # Date and season
    date = datetime.now().strftime("%B %d, %Y")
    season, season_name = get_season_info()

    # Style analysis
    style_vibe = determine_style_vibe(style_description)
    pants_fit = get_fit_for_body_type(body_type, "pants", style_vibe)
    tops_fit = get_fit_for_body_type(body_type, "tops", style_vibe)
    fit_multiplier = FIT_MULTIPLIERS.get(body_type, "1.8x larger")

    # Colors
    style_keywords = style_description.lower().split()[:5]
    outfit_palette, _ = get_two_color_palettes(style_keywords)
    color_palette_str = format_color_palette_for_prompt(outfit_palette, include_hex=False)

    # Layering
    layering_instruction = get_layering_instruction(season, style_vibe)

    # Accessories
    accessories = get_accessories(age, style_vibe)

    # Female note
    female_note = "FEMALE: Can use dresses, skirts, blouses, heels, flats" if sex == "female" else ""

    return OUTFIT_PROMPT.format(
        age=age,
        sex=sex,
        height=height,
        weight=weight,
        body_type=body_type,
        date=date,
        season=season,
        season_name=season_name,
        style_description=style_description[:80],
        brands=brands,
        color_palette=color_palette_str,
        pants_fit=pants_fit,
        tops_fit=tops_fit,
        fit_multiplier=fit_multiplier,
        layering_instruction=layering_instruction,
        accessories=accessories,
        female_note=female_note
    )

def build_image_prompt_compiler(user_data: dict, measurements: dict, outfit_description: str) -> str:
    """Build image compiler - cost-optimized."""

    sex = user_data.get("sex", "male")
    age = user_data.get("age", 25)
    height = user_data.get("height", 170)
    weight = user_data.get("weight", 70)
    body_type = user_data.get("body_type", "average")

    # Body visual description
    body_visual = get_body_visual_description(height, weight, body_type, sex)

    # Body shape note for plus-size
    body_shape_note = get_body_shape_note(body_type, sex)

    # Fit multiplier
    fit_multiplier = FIT_MULTIPLIERS.get(body_type, "1.8x larger")

    # Extract shoe color
    shoe_color = extract_shoe_color(outfit_description)

    return IMAGE_COMPILER.format(
        sex=sex,
        age=age,
        height=height,
        weight=weight,
        body_type=body_type,
        body_visual=body_visual,
        body_shape_note=body_shape_note,
        outfit_description=outfit_description,
        fit_multiplier=fit_multiplier,
        shoe_color=shoe_color
    )

def build_styling_tips_prompt(user_data: dict, measurements: dict, outfit_description: str) -> str:
    """Build styling tips - minimal tokens."""

    style_keywords = user_data.get("style_description", "").lower().split()[:5]
    _, alternative_palette = get_two_color_palettes(style_keywords)

    season, _ = get_season_info()

    alt_colors = alternative_palette.get("colors", [])
    color_names = [c.split(" (#")[0] if " (#" in c else c for c in alt_colors]
    alternative_palette_str = ", ".join(color_names[:3])

    return TIPS_PROMPT.format(
        season=season,
        age=user_data.get("age", 25),
        sex=user_data.get("sex", "male"),
        body_type=user_data.get("body_type", "average"),
        alternative_palette=alternative_palette_str
    )

def format_outfit_response(outfit_description: str, styling_tips: str, measurements: dict) -> str:
    """Format final response."""
    dims = [
        f"Chest: {measurements.get('chest_circumference', 'N/A')}cm",
        f"Waist: {measurements.get('waist_circumference', 'N/A')}cm",
        f"Hips: {measurements.get('hip_circumference', 'N/A')}cm",
        f"BMI: {measurements.get('bmi', 'N/A')}"
    ]

    return f"""{outfit_description}

💡 Styling Tip: {styling_tips}

📏 Measurements: {' | '.join(dims)}"""

# =============================================================================
# VALIDATION
# =============================================================================

VALID_BODY_TYPES = ["slim", "athletic", "average", "muscular", "stocky", "plus-size"]

def validate_user_data(user_data: dict) -> bool:
    """Validate user data."""
    required = ["sex", "age", "height", "weight", "body_type"]

    for field in required:
        if field not in user_data or user_data[field] is None:
            raise ValueError(f"Missing field: {field}")

    if user_data["body_type"] not in VALID_BODY_TYPES:
        raise ValueError(f"Invalid body_type: {user_data['body_type']}")

    if not (10 < user_data["age"] < 100):
        raise ValueError(f"Invalid age: {user_data['age']}")
    if not (140 < user_data["height"] < 220):
        raise ValueError(f"Invalid height: {user_data['height']}")
    if not (40 < user_data["weight"] < 200):
        raise ValueError(f"Invalid weight: {user_data['weight']}")

    return True