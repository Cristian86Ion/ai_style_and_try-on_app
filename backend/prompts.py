from sanzo_wada_colors import (
    get_two_color_palettes,
    format_color_palette_for_prompt,
    get_current_season
)
from fit_rules import (
    FIT_RULES,
    get_fit_for_body_type,
    determine_style_vibe,
    adjust_fit_size
)
from datetime import datetime

# =============================================================================
# STEP 1: GPT OUTFIT GENERATION - TEXT DESCRIPTION ONLY
# =============================================================================

GPT_OUTFIT_GENERATION_PROMPT = """
TIMESTAMP: {timestamp}
SEASON: {season} ({season_description})

CLIENT: {age}yo {sex}, {height}cm, {weight}kg, {body_type}
STYLE: {style_description}

COLOR PALETTE (for tops/outerwear): {color_palette}
PANTS COLORS (basic only): Navy, Black, Charcoal Gray, Khaki, Beige, Olive, Brown

FIT: {body_type} in {style_vibe} style
- Pants: {pants_fit} (relaxed, full-length covering ankles)
- Tops: {tops_fit} (relaxed, NOT tight)

AGE-APPROPRIATE ({age}yo):
{age_styling_rules}

═══════════════════════════════════════════════════════════════════════
OUTPUT FORMAT (4-6 sentences)
═══════════════════════════════════════════════════════════════════════

1. TOP - MUST INCLUDE NECKLINE TYPE:
"Start with a [COLOR] [fabric] [NECKLINE TYPE] [garment], offering relaxed fit."

NECKLINES (NEVER say just "sweater"):
- Crewneck sweater (round neckline, NO HOOD)
- Turtleneck sweater (high collar, NO HOOD)  
- V-neck sweater (V-shaped, NO HOOD)
- Button-down shirt (collared with buttons)
- Polo shirt (short button placket)

2. PANTS - FULL-LENGTH:
"Pair with [BASIC COLOR] [fabric] trousers in [fit], full-length covering ankles to shoes."

3. FOOTWEAR - BE SPECIFIC:
"Complete with [color] [material] [specific shoe type with details]."

4. OUTERWEAR ({season_outerwear}):
"Layer a [COLOR] [fabric] [jacket/coat], [length]."

5. ACCESSORIES: {accessories_rules}

EXAMPLE:
"Start with a Forest Green merino wool crewneck sweater with cable-knit, offering relaxed fit. Pair with Charcoal Gray wool trousers in straight-fit, full-length covering ankles to shoes. Complete with Black leather Chelsea boots with elastic panels. Layer a Navy Blue wool overcoat, knee-length. Finish with brown leather belt."
""".strip()

# =============================================================================
# STEP 2: GPT IMAGE PROMPT COMPILER - GRAY FIGURE VERSION
# =============================================================================

GPT_IMAGE_PROMPT_COMPILER = """
You are a technical prompt compiler. Convert outfit description into Flux prompt.

DO NOT change clothing, colors, or add creativity. Use EXACT data provided.

INPUT:
- Sex: {sex}, Age: {age}, Height: {height}cm, Weight: {weight}kg, Body: {body_type}
- Outfit: {outfit_description}

═══════════════════════════════════════════════════════════════════════
FLUX PROMPT TEMPLATE
═══════════════════════════════════════════════════════════════════════

Professional fashion product photography: Abstract gray humanoid figure wearing complete outfit, studio lighting, front view, A-pose.

FIGURE BASE - UNIFORM GRAY SILHOUETTE:
A single monochromatic gray 3D humanoid figure (RGB: 128, 128, 128 / #808080) with:
- Featureless smooth oval head (no face, hair, or features)
- Natural {sex} body proportions
- Height: {height}cm, Build: {body_type}, Age: {age}
- {body_type_description}
- Smooth matte gray surface on HEAD and NECK only (everything else covered by clothes)
- Human anatomical structure, NOT mannequin or robot

POSE:
- Static A-pose, standing upright, front-facing
- Feet shoulder-width apart, parallel
- Arms slightly away from body at 15-20 degrees
- Completely still, neutral stance

OUTFIT WORN BY FIGURE (USE EXACT DESCRIPTION):
{outfit_description}

GARMENT FIT - ANTI-SHRINK-WRAP (CRITICAL):
✓ ALL garments RELAXED and DRAPED with natural folds
✓ Significant AIR GAPS between fabric and gray body
✓ Fabrics hang loosely with gravity, showing separation from body
✓ Deep shadows in folds prove fabric is NOT painted on
✓ NO tight/form-fitting clothes - everything has breathing room

PANTS (CRITICAL):
✓ Full-length covering ankles COMPLETELY
✓ Fabric reaches top of shoes, natural break
✓ Relaxed fit with draping through legs
✓ NO gray legs visible below pants

FOOTWEAR (CRITICAL - PREVENTS GRAY FEET):
✓ Shoes are VOLUMETRIC 3D OBJECTS that COMPLETELY ENCLOSE feet
✓ NO gray feet visible - feet are INSIDE shoes
✓ Shoes fully wrap around foot from all angles
✓ Dimensional soles with thickness, sitting ON ground
✓ Laces/closures visible as 3D elements

NECKLINE ACCURACY (CRITICAL):
✓ If description says "crewneck" → render crewneck (NO HOOD)
✓ If description says "turtleneck" → render turtleneck (NO HOOD)
✓ If description says "button-down" → render collared shirt
✓ NEVER add hoods unless explicitly specified

COLOR EXTRACTION:
- Extract EXACT color from each garment description
- "Forest Green sweater" → render Forest Green
- "Charcoal Gray trousers" → render Charcoal Gray
- "Black boots" → render Black
- Colors must be VIBRANT and SATURATED on fabrics

FABRIC TEXTURES:
- Cotton: visible weave, matte
- Wool: knit texture with depth
- Linen: crosshatch weave, wrinkles
- Leather: grain texture, slight sheen
All fabrics show realistic textile properties

LIGHTING:
- Professional studio softbox, front and slightly above
- Even diffused illumination
- Shadows in fabric folds show separation
- Makes colors vibrant

CAMERA:
- Full body head to feet, eye-level
- 50mm lens, no distortion
- Centered framing, sharp focus

BACKGROUND:
- Smooth light gray (RGB: 235, 235, 235)
- Clean studio backdrop

CRITICAL CHECKS:
✓ ONE gray figure only (not multiple)
✓ Head properly sized (1/7.5 of height)
✓ Fabrics RELAXED with air gaps (not tight)
✓ Neckline matches description (no hoods unless specified)
✓ Shoes enclose feet completely (no gray feet)
✓ Pants cover ankles (no gray legs)
✓ Colors match description exactly

AVOID:
❌ Real human appearance (use gray figure)
❌ Tight shrink-wrapped clothes
❌ Hoods when not specified
❌ Visible gray feet/hands (must be covered)
❌ Multiple figures
❌ Wrong necklines

OUTPUT: Gray humanoid figure ({sex}, {age}yo, {height}cm, {body_type}) wearing the exact outfit described, with relaxed fits, proper colors, and complete coverage.
""".strip()

# =============================================================================
# STYLING TIPS
# =============================================================================

GPT_STYLING_TIPS_PROMPT = """
SEASON: {season}
CLIENT: {age}yo {sex}, {height}cm, {body_type}
ALTERNATIVE COLORS: {alternative_palette}

Generate 50-word max trend guidance for {season}. Do NOT describe outfit.

Include: fabrics, silhouettes, footwear, 3 colors from alternative palette, 1 styling technique.

Max 50 words, professional tone.
""".strip()


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_age_styling_rules(age: int, style_vibe: str) -> str:
    """Age rules."""
    if age < 20:
        if style_vibe == "elegant":
            return "NO ties/bowties (too formal). Structured but youthful. Watch and belt only."
        return "Youthful trends. Sneakers. Relaxed fits."
    elif age < 30:
        return "Balance trends with sophistication."
    elif age < 50:
        return "Quality over trends. Refined pieces."
    return "Classic sophisticated pieces."


def get_accessories_rules(age: int, style_vibe: str) -> str:
    """Accessories."""
    if age < 20 and style_vibe == "elegant":
        return "Watch, belt ONLY. NO ties/bowties."
    return "Watch, belt, optional tie/pocket square if elegant."


def get_body_type_description(body_type: str, age: int) -> str:
    """Body description."""
    desc = {
        "slim": "Lean frame with minimal body fat, narrow build",
        "athletic": f"Toned with MODERATE muscle definition - fit but NOT heavily muscular, active {age}yo build",
        "average": "Balanced proportions, healthy typical build",
        "muscular": "Heavily developed musculature, broad powerful build",
        "stocky": "Solid compact build with substance",
        "plus-size": "Fuller figure with natural curves"
    }
    return desc.get(body_type, "Balanced build")


def get_sex_description(sex: str) -> str:
    return "male" if sex.lower() == "male" else "female"


def build_outfit_generation_prompt(user_data: dict, measurements: dict) -> str:
    """Build outfit generation prompt."""
    style_description = user_data.get("style_description", "casual")
    body_type = user_data.get("body_type", "average")
    height = user_data.get("height", 170)
    sex = user_data.get("sex", "male")
    age = user_data.get("age", 25)

    style_vibe = determine_style_vibe(style_description)
    pants_fit = get_fit_for_body_type(body_type, "pants", style_vibe)
    tops_fit = get_fit_for_body_type(body_type, "tops", style_vibe)

    season = get_current_season()
    timestamp = datetime.now().strftime("%B %d, %Y")

    style_keywords = style_description.lower().split()[:5]
    outfit_palette, _ = get_two_color_palettes(style_keywords)
    color_palette_str = format_color_palette_for_prompt(outfit_palette, include_hex=False)

    season_description = "Fall/Winter" if season == "FW" else "Spring/Summer"
    season_outerwear = "Required" if season == "FW" else "Optional"

    age_styling_rules = get_age_styling_rules(age, style_vibe)
    accessories_rules = get_accessories_rules(age, style_vibe)

    return GPT_OUTFIT_GENERATION_PROMPT.format(
        timestamp=timestamp,
        season=season,
        season_description=season_description,
        age=age,
        sex=sex,
        height=height,
        weight=user_data.get("weight", 70),
        body_type=body_type,
        style_description=style_description[:100],
        color_palette=color_palette_str,
        style_vibe=style_vibe,
        pants_fit=pants_fit,
        tops_fit=tops_fit,
        season_outerwear=season_outerwear,
        age_styling_rules=age_styling_rules,
        accessories_rules=accessories_rules
    )


def build_image_prompt_compiler(user_data: dict, measurements: dict, outfit_description: str) -> str:
    """Build image compiler prompt."""
    sex = user_data.get("sex", "male")
    age = user_data.get("age", 25)
    height = user_data.get("height", 170)
    weight = user_data.get("weight", 70)
    body_type = user_data.get("body_type", "average")

    body_type_description = get_body_type_description(body_type, age)

    return GPT_IMAGE_PROMPT_COMPILER.format(
        sex=sex,
        age=age,
        height=height,
        weight=weight,
        body_type=body_type,
        outfit_description=outfit_description,
        body_type_description=body_type_description
    )


def build_styling_tips_prompt(user_data: dict, measurements: dict, outfit_description: str) -> str:
    """Build styling tips prompt."""
    style_keywords = user_data.get("style_description", "").lower().split()[:5]
    _, alternative_palette = get_two_color_palettes(style_keywords)

    season = get_current_season()

    alt_colors = alternative_palette.get("colors", [])
    color_names = [color.split(" (#")[0] if " (#" in color else color for color in alt_colors]
    alternative_palette_str = ", ".join(color_names[:3])

    return GPT_STYLING_TIPS_PROMPT.format(
        season=season,
        age=user_data.get("age", 25),
        sex=user_data.get("sex", "male"),
        height=user_data.get("height", 170),
        body_type=user_data.get("body_type", "average"),
        alternative_palette=alternative_palette_str
    )


def format_outfit_response(outfit_description: str, styling_tips: str, measurements: dict) -> str:
    """
    Format the outfit response with dimensions at the end.
    This returns a structured string for the API response.
    """
    # Build dimensions section
    dimensions = []
    dimensions.append(f"Chest: {measurements.get('chest_circumference', 'N/A')}cm")
    dimensions.append(f"Waist: {measurements.get('waist_circumference', 'N/A')}cm")
    dimensions.append(f"Hips: {measurements.get('hip_circumference', 'N/A')}cm")
    dimensions.append(f"Leg Length: {measurements.get('leg_length', 'N/A')}cm")
    dimensions.append(f"Arm Length: {measurements.get('arm_length', 'N/A')}cm")
    dimensions.append(f"Shoulder/Hip Ratio: {measurements.get('shoulder_hip_ratio', 'N/A')}")
    dimensions.append(f"BMI: {measurements.get('bmi', 'N/A')}")

    dimensions_text = " | ".join(dimensions)

    # Combine all parts
    response = f"""{outfit_description}

💡 Styling Tip: {styling_tips}

📏 Body Measurements: {dimensions_text}"""

    return response


# =============================================================================
# CONSTANTS
# =============================================================================

VALID_BODY_TYPES = ["slim", "athletic", "average", "muscular", "stocky", "plus-size"]