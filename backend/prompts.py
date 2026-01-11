from datetime import datetime
from sanzo_wada_colors import get_current_season
import re


# =============================================================================
# SEASON & STYLE DETECTION
# =============================================================================

def get_season_info() -> tuple:
    """Get current season code and name."""
    season = get_current_season()
    return season, "Fall/Winter" if season == "FW" else "Spring/Summer"

def get_date_from_api(data: dict, field: str) -> datetime:
    return datetime.fromisoformat(
        data[field].replace("Z", "+00:00")
    )

def season_from_date(dt: datetime) -> str:
    month = dt.month
    return "FW" if month in (10, 11, 12, 1, 2, 3) else "SS"


# =============================================================================
# STYLE KEYWORD EXTRACTION PROMPT
# =============================================================================

STYLE_KEYWORD_EXTRACTOR = """Extract semantic search keywords from user style description.

USER PROFILE:
- Age: {age}
- Gender: {sex}
- Body Type: {body_type}
- Height: {height}cm, Weight: {weight}kg
- Season: {season_name}
- Style Description: "{style_description}"
- Favorite Brands: {brands}

YOUR TASK:
Extract 5-10 keywords for semantic clothing search. Include:
1. Style keywords (casual, formal, streetwear, sporty, elegant, vintage, punk)
2. Color preferences (black, navy, earth tones, bright, monochrome)
3. Garment types (oversized, fitted, loose, cropped)
4. Patterns (solid, stripes, graphic, minimal)
5. Use datetime to generate correct clothing palette 

OUTPUT FORMAT (JSON):
{{
  "style_keywords": ["keyword1", "keyword2", ...],
  "color_preferences": ["color1", "color2", ...],
  "fit_preferences": ["fit1", "fit2"],
  "season_appropriate": ["seasonal_item1", "seasonal_item2"]
}}

RULES:
- Be specific but flexible
- Consider season ({season_name})
- Match user's age/body type
- If brands mentioned, prioritize those styles
- Return ONLY valid JSON, no extra text"""


# =============================================================================
# DATABASE QUERY BUILDER
# =============================================================================

def build_semantic_filters(keywords: dict, user_data: dict, season: str) -> dict:
    sex = user_data.get('sex', 'male')
    gender_db = 'man' if sex == 'male' else 'woman'

    style_map = {
        'casual': 'casual',
        'sporty': 'sporty',
        'sport': 'sporty',
        'athletic': 'sporty',
        'formal': 'formal',
        'elegant': 'formal',
        'business': 'formal',
        'streetwear': 'streetwear',
        'street': 'streetwear',
        'urban': 'streetwear'
    }

    style_keywords = keywords.get('style_keywords', [])
    detected_style = 'casual'  # default

    for kw in style_keywords:
        kw_lower = kw.lower()
        for key, value in style_map.items():
            if key in kw_lower:
                detected_style = value
                break

    color_prefs = keywords.get('color_preferences', [])
    primary_color = color_prefs[0].lower() if color_prefs else 'black'

    primary_color = primary_color.split()[0]  # "dark blue" -> "dark"

    brands = user_data.get('favorite_brands', [])
    brand = brands[0].lower().replace(' ', '_') if brands else None

    filters = {
        'gender': gender_db,
        'style': detected_style,
        'colors': primary_color
    }

    if brand:
        filters['brand'] = brand

    return filters

# =============================================================================
# 3D MANNEQUIN GENERATION PROMPT
# =============================================================================

MANNEQUIN_PROMPT = """Generate a neutral 3D human shape full body, from head to shoes for clothing overlay.

BODY SPECIFICATIONS:
- Gender: {sex_upper}
- Height: {height}cm
- Weight: {weight}kg
- Body Type: {body_type}
- BMI: {bmi:.1f}

MEASUREMENTS:
- Chest: {chest}cm
- Waist: {waist}cm  
- Hips: {hips}cm
- Leg Length: {leg_length}cm

REQUIREMENTS:
1. **Featureless gray silhouette ** (RGB 180, 180, 180)
2. **NO facial features** - smooth head and smooth face
3. **A-pose**: arms 20° from body, legs parallel, NO hands in pocket
4. **Full body visible**: head to shoes in frame
5. **Studio lighting**: even, no harsh shadows
6. **Clean background**: light gray seamless (RGB 220, 220, 220)
7. **Frontal view**: straight-on camera angle
8. **Professional product photography style**

BODY PROPORTIONS ({sex_upper}):
{body_description}

{height_instruction}
{body_type_instruction}

POSE SPECIFICS:
- Standing upright, neutral expression area (no features)
- Hands visible, fingers slightly separated
- Feet flat, shoulder-width apart
- Torso straight, shoulders level

RENDER QUALITY:
- High-resolution 3D render
- Smooth surface, subtle ambient occlusion
- No clothing, no textures
- Ready for garment overlay

OUTPUT: Single full-body mannequin image, 768x1024px"""

# =============================================================================
# CLOTHING OVERLAY INSTRUCTION
# =============================================================================

CLOTHING_OVERLAY_PROMPT = """Overlay real product images onto 3D mannequin silhouette with natural fitting.

BASE MANNEQUIN: {mannequin_description}

SELECTED CLOTHING ITEMS:
{clothing_items}

OVERLAY INSTRUCTIONS:

1. **TOP ({top_category})**:
   - Product: {top_id} - {top_brand}
   - Colors: {top_colors}
   - Style: {top_style}
   - Fit: Position on torso with natural draping
   - Align shoulders, adjust for body width
   - Show fabric texture and folds

2. **PANTS ({pants_category})**:
   - Product: {pants_id} - {pants_brand}
   - Colors: {pants_colors}
   - Style: {pants_style}
   - Fit: Waist-to-ankle coverage
   - Match leg width, natural stacking at shoes
   - Preserve garment proportions

3. **FOOTWEAR**:
   - Product: {shoe_id} - {shoe_brand}
   - Colors: {shoe_colors}
   - Style: {shoe_style}
   - Position: On feet, soles touching ground
   - Maintain shoe silhouette

4. **LAYER ({layer_category})** (if applicable):
   - Product: {layer_id} - {layer_brand}
   - Colors: {layer_colors}
   - Style: {layer_style}
   - Fit: Over top garment, natural layering
   - Show depth and dimension

RENDERING RULES:
- Preserve original product colors/patterns
- Natural lighting interaction
- Realistic fabric draping (gravity + body shape)
- No distortion of brand logos/graphics
- Smooth garment edges, no clipping
- Professional product photography quality

COMPOSITION:
- Full outfit visible head-to-toe
- Maintain mannequin's neutral pose
- Clean background (light gray)
- Studio lighting setup

OUTPUT: Composite image showing dressed mannequin, 768x1024px"""

# =============================================================================
# STYLING TIPS PROMPT
# =============================================================================

STYLING_TIPS_PROMPT = """Generate brief styling advice for selected outfit.

CLIENT PROFILE:
- Age: {age}, Gender: {sex}
- Body Type: {body_type}
- Season: {season_name}

SELECTED OUTFIT:
- Top: {top_brand} {top_category} ({top_colors})
- Pants: {pants_brand} {pants_category} ({pants_colors})
- Shoes: {shoe_brand} ({shoe_colors})
- Layer: {layer_info}

TASK: Provide 2-3 concise styling tips (max 50 words total).

Consider:
- How to accessorize this outfit
- Best occasions for this style
- Seasonal adjustments
- Color coordination advice

Be specific, practical, and encouraging. Focus on making the outfit work for the client."""


# =============================================================================
# BODY DESCRIPTION HELPERS
# =============================================================================

def get_body_description(height: int, weight: int, body_type: str, sex: str, measurements: dict) -> str:
    """Generate accurate body description for mannequin generation."""

    bmi = measurements.get('bmi', weight / ((height / 100) ** 2))
    chest = measurements.get('chest_circumference', 90)
    waist = measurements.get('waist_circumference', 80)
    hips = measurements.get('hip_circumference', 95)
    leg_length = measurements.get('leg_length', height * 0.52)

    sex_traits = (
        "FEMALE anatomy: narrower shoulders, wider hips, defined waist, feminine curves"
        if sex == "female" else
        "MALE anatomy: broader shoulders, narrower hips, straighter torso, masculine build"
    )

    body_map = {
        "slim": f"Lean frame, minimal body fat. {sex_traits}",
        "athletic": f"Toned, defined muscles. {sex_traits}",
        "muscular": f"Well-developed musculature. {sex_traits}",
        "average": f"Balanced proportions, moderate build. {sex_traits}",
        "stocky": f"Solid build, some muscle mass. {sex_traits}",
        "plus-size": f"Fuller figure, soft curves. {sex_traits}"
    }

    description = body_map.get(body_type, f"{sex_traits}")

    return (f"{height}cm tall, {weight}kg, BMI {bmi:.1f}. "
            f"{description} "
            f"Chest {chest}cm, Waist {waist}cm, Hips {hips}cm.")


def get_height_instruction(height: int) -> str:

    if height < 165:
        return "SHORT stature - compact torso and leg proportions"
    elif height > 185:
        return "TALL stature - elongated torso and legs"
    return "AVERAGE height - standard proportions"


def get_body_type_instruction(body_type: str, sex: str, weight: int) -> str:

    instructions = {
        "slim": f"Slender {sex.upper()} build, narrow frame",
        "athletic": f"Athletic {sex.upper()} physique, toned muscles",
        "muscular": f"Muscular {sex.upper()} build, developed muscles",
        "average": f"Average {sex.upper()} build, balanced proportions",
        "stocky": f"Stocky {sex.upper()} build, solid frame",
        "plus-size": (
            f"Plus-size FEMALE build, fuller curves, wider hips"
            if sex == "female" else
            f"Plus-size MALE build, rounder torso, fuller chest"
        )
    }

    return instructions.get(body_type, f"{body_type.title()} {sex.upper()} build")


# =============================================================================
# MAIN PROMPT BUILDERS
# =============================================================================

def build_style_extraction_prompt(user_data: dict) -> str:

    season, season_name = get_season_info()
    brands = user_data.get('favorite_brands', [])
    brands_str = ", ".join(brands) if brands else "None specified"

    return STYLE_KEYWORD_EXTRACTOR.format(
        age=user_data.get('age', 25),
        sex=user_data.get('sex', 'male'),
        body_type=user_data.get('body_type', 'average'),
        height=user_data.get('height', 170),
        weight=user_data.get('weight', 70),
        season_name=season_name,
        style_description=user_data.get('style_description', 'casual'),
        brands=brands_str
    )


def build_mannequin_prompt(user_data: dict, measurements: dict) -> str:

    sex = user_data.get('sex', 'male')
    height = user_data.get('height', 170)
    weight = user_data.get('weight', 70)
    body_type = user_data.get('body_type', 'average')

    body_desc = get_body_description(height, weight, body_type, sex, measurements)
    height_inst = get_height_instruction(height)
    body_inst = get_body_type_instruction(body_type, sex, weight)

    return MANNEQUIN_PROMPT.format(
        sex_upper=sex.upper(),
        height=height,
        weight=weight,
        body_type=body_type,
        bmi=measurements.get('bmi', 22),
        chest=measurements.get('chest_circumference', 90),
        waist=measurements.get('waist_circumference', 80),
        hips=measurements.get('hip_circumference', 95),
        leg_length=measurements.get('leg_length', height * 0.52),
        body_description=body_desc,
        height_instruction=height_inst,
        body_type_instruction=body_inst
    )


def build_overlay_prompt(user_data: dict, measurements: dict, selected_items: dict) -> str:

    sex = user_data.get('sex', 'male')
    height = user_data.get('height', 170)
    weight = user_data.get('weight', 70)
    body_type = user_data.get('body_type', 'average')

    mannequin_desc = f"{sex.upper()}, {height}cm, {weight}kg, {body_type} build"

    # Format clothing items
    top = selected_items.get('top', {})
    pants = selected_items.get('pants', {})
    shoe = selected_items.get('shoe', {})
    layer = selected_items.get('layer', {})

    clothing_items = f"""
TOP: {top.get('brand', 'N/A')} {top.get('category', 'N/A')}
PANTS: {pants.get('brand', 'N/A')} {pants.get('category', 'N/A')}
SHOES: {shoe.get('brand', 'N/A')}
LAYER: {layer.get('brand', 'N/A') if layer else 'None'}
"""

    return CLOTHING_OVERLAY_PROMPT.format(
        mannequin_description=mannequin_desc,
        clothing_items=clothing_items,
        top_category=top.get('category', 'shirt'),
        top_id=top.get('id', 'N/A'),
        top_brand=top.get('brand', 'N/A'),
        top_colors=', '.join(top.get('colors', ['N/A'])),
        top_style=top.get('style', 'N/A'),
        pants_category=pants.get('category', 'pants'),
        pants_id=pants.get('id', 'N/A'),
        pants_brand=pants.get('brand', 'N/A'),
        pants_colors=', '.join(pants.get('colors', ['N/A'])),
        pants_style=pants.get('style', 'N/A'),
        shoe_id=shoe.get('id', 'N/A'),
        shoe_brand=shoe.get('brand', 'N/A'),
        shoe_colors=', '.join(shoe.get('colors', ['N/A'])),
        shoe_style=shoe.get('style', 'N/A'),
        layer_category=layer.get('category', 'N/A') if layer else 'N/A',
        layer_id=layer.get('id', 'N/A') if layer else 'N/A',
        layer_brand=layer.get('brand', 'N/A') if layer else 'N/A',
        layer_colors=', '.join(layer.get('colors', ['N/A'])) if layer else 'N/A',
        layer_style=layer.get('style', 'N/A') if layer else 'N/A'
    )


def build_styling_tips_prompt(user_data: dict, selected_items: dict) -> str:

    season, season_name = get_season_info()

    top = selected_items.get('top', {})
    pants = selected_items.get('pants', {})
    shoe = selected_items.get('shoe', {})
    layer = selected_items.get('layer')

    layer_info = (
        f"{layer.get('brand', 'N/A')} {layer.get('category', 'N/A')}"
        if layer else "None"
    )

    return STYLING_TIPS_PROMPT.format(
        age=user_data.get('age', 25),
        sex=user_data.get('sex', 'male'),
        body_type=user_data.get('body_type', 'average'),
        season_name=season_name,
        top_brand=top.get('brand', 'N/A'),
        top_category=top.get('category', 'N/A'),
        top_colors=', '.join(top.get('colors', ['N/A'])),
        pants_brand=pants.get('brand', 'N/A'),
        pants_category=pants.get('category', 'N/A'),
        pants_colors=', '.join(pants.get('colors', ['N/A'])),
        shoe_brand=shoe.get('brand', 'N/A'),
        shoe_colors=', '.join(shoe.get('colors', ['N/A'])),
        layer_info=layer_info
    )


# =============================================================================
# VALIDATION
# =============================================================================

VALID_BODY_TYPES = ["slim", "athletic", "average", "muscular", "stocky", "plus-size"]


def validate_user_data(user_data: dict) -> bool:
    required = ["sex", "age", "height", "weight", "body_type"]

    for field in required:
        if field not in user_data or user_data[field] is None:
            raise ValueError(f"Missing required field: {field}")

    if user_data["body_type"] not in VALID_BODY_TYPES:
        raise ValueError(f"Invalid body_type: {user_data['body_type']}")

    if not (10 < user_data["age"] < 100):
        raise ValueError(f"Invalid age: {user_data['age']}")

    if not (140 < user_data["height"] < 220):
        raise ValueError(f"Invalid height: {user_data['height']}")

    if not (40 < user_data["weight"] < 200):
        raise ValueError(f"Invalid weight: {user_data['weight']}")

    return True