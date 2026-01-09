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
# DETAILED BODY TYPE DEFINITIONS (INTERNAL STRUCTURE - NOT VISIBLE)
# =============================================================================
BODY_TYPE_VISUAL_RULES = {
    "slim": (
        "Lean and slender frame, narrow shoulders, minimal muscle mass. "
        "Body fat: 8-12%. Very thin arms and legs, delicate bone structure, flat stomach."
    ),
    "average": (
        "Standard rectangular body shape with minimal muscle development. "
        "Body fat: 15-20%. Balanced, non-toned proportions, straight torso without significant definition."
    ),
    "athletic": (
        "V-shaped or toned rectangular frame, lean but with visible muscle definition. "
        "Body fat: 9-15%. Defined arms (biceps/triceps above average), visible muscle contours, fit and lean core."
    ),
    "muscular": (
        "Broad powerful build with voluminous muscle mass. "
        "Body fat: 13-23%. Heavily developed chest and shoulders, thick muscular arms and thighs, well-defined physical power."
    ),
    "stocky": (
        "Solid, compact, and voluminous build. "
        "Body fat: 23-30%. Large muscle mass underneath a layer of body fat, broad thick frame, powerful but less defined than 'muscular'."
    ),
    "plus-size": (
        "Fuller, generous figure with soft contours. "
        "Body fat: 30-40%. Prominent stomach area, thick arms and thighs where fat hangs naturally with gravity. "
        "Rounded shoulders, wide torso, soft physical appearance regardless of height."
    )
}

# =============================================================================
# ANATOMICAL CLOTHING CORRELATION RULES
# =============================================================================
CLOTHING_ANATOMY_CORRELATION = {
    "slim": {
        "tops": "Garments drape loosely with visible air gaps between fabric and torso. Minimal fabric tension at shoulders.",
        "pants": "Excess fabric pools at ankles, waistband sits naturally without pulling. Clear space between fabric and legs.",
        "fit_notes": "All clothing appears 1-2 sizes too large, hanging with natural gravity folds."
    },
    "average": {
        "tops": "Fabric flows smoothly over torso with moderate draping. Natural fabric movement at sides.",
        "pants": "Standard drape with slight fabric pooling at ankles. Comfortable fit through thighs and calves.",
        "fit_notes": "Clothing appears relaxed but not oversized, with balanced proportions."
    },
    "athletic": {
        "tops": "Extra fabric room at shoulders and chest to accommodate muscle definition. Fabric hangs without stretching.",
        "pants": "Additional space through thighs, fabric flows loosely past knees. No fabric tension at quads.",
        "fit_notes": "Garments sized up to prevent tightness at muscular areas while maintaining drape."
    },
    "muscular": {
        "tops": "Significant extra volume at chest and shoulders. Fabric creates pronounced draping shadows to show separation from body.",
        "pants": "Wide leg openings with substantial fabric volume through thighs. Deep shadow creases show fabric separation.",
        "fit_notes": "All garments substantially oversized to avoid any appearance of strain or tightness."
    },
    "stocky": {
        "tops": "Relaxed fit with flowing fabric at torso. No fabric tension at midsection.",
        "pants": "Straight leg with generous room through seat and thighs. Fabric falls naturally without clinging.",
        "fit_notes": "Comfortable, flowing fits that provide movement freedom without appearing baggy."
    },
    "plus-size": {
        "tops": "Flowing fabrics with substantial drape. Fabric hangs independently from body contours with deep shadow gaps.",
        "pants": "Relaxed straight fit with significant fabric volume. Multiple natural fabric folds and creases showing separation.",
        "fit_notes": "Maximum comfort prioritized - all garments appear 2+ sizes larger with extensive draping."
    }
}

# =============================================================================
# STEP 1: GPT OUTFIT GENERATION - TEXT DESCRIPTION
# =============================================================================

GPT_OUTFIT_GENERATION_PROMPT = """
TIMESTAMP: {timestamp}
SEASON: {season} ({season_description})
CLIENT: {age}yo {sex}, {height}cm, {weight}kg, {body_type}
BRANDS: {brands}
STYLE: {style_description}

COLOR PALETTE (USE THESE VIBRANT COLORS): {color_palette}
PANTS/BOTTOMS COLORS: Navy, Black, Charcoal Gray, Khaki, Beige, Olive, Brown, White, Cream

⚠️ CRITICAL: You MUST use colors from the palette above. NEVER generate colorless outfits.
⚠️ EVERY garment must have an EXPLICIT COLOR NAME stated.

FIT RULES:
- Body: {body_type} in {style_vibe} style
- Bottoms: {pants_fit} → RELAXED, full-length
- Tops: {tops_fit} → RELAXED, not tight
- {fit_multiplier}

AGE RULES ({age}yo): {age_styling_rules}

═══════════════════════════════════════════════════════════════════════════
OUTPUT FORMAT (4-6 sentences) - COLORS MANDATORY
═══════════════════════════════════════════════════════════════════════════

CRITICAL RULE: State EXPLICIT COLOR for EVERY garment. NO exceptions.

1. TOP + NECKLINE:
"Start with [SPECIFIC COLOR from palette] [fabric] [NECKLINE] [garment], relaxed fit."
Examples: "Sky Blue cotton", "Emerald Green wool", "Blush Pink silk"
NEVER: "light colored", "neutral", "dark" - ALWAYS name the color

2. BOTTOMS - FULL-LENGTH:
"Pair with [SPECIFIC COLOR] [fabric] [trouser/skirt/pants], [fit], full-length."
Examples: "Navy Blue wool trousers", "Charcoal Gray cotton pants", "Black denim jeans"

3. FOOTWEAR - BE SPECIFIC:
"Complete with [COLOR] [material] [specific shoe type]."
Examples: "Black leather boots", "White canvas sneakers", "Tan suede loafers"

4. OUTERWEAR ({season_outerwear}):
"Layer [SPECIFIC COLOR from palette] [fabric] [jacket/coat], [length]."
Examples: "Forest Green wool coat", "Burgundy leather jacket"

5. ACCESSORIES: {accessories_rules}

FEMALE-SPECIFIC ADDITIONS:
- Can include dresses, skirts, blouses
- Footwear: heels, flats, sandals, boots
- Accessories: scarves, jewelry, handbags

MALE-SPECIFIC:
- Shirts, sweaters, blazers
- Footwear: oxfords, boots, sneakers, loafers

EXAMPLE (GOOD - WITH COLORS):
"Start with Sky Blue linen button-down shirt with spread collar, relaxed fit. Pair with Navy Blue cotton chinos, straight-fit, full-length. Complete with White leather minimalist sneakers. Layer Seafoam Green cotton bomber jacket, hip-length."

EXAMPLE (BAD - NO COLORS):
"A nice shirt with pants and shoes." ❌ NEVER DO THIS

✅ REMEMBER: Every garment MUST have explicit color name!
""".strip()

# =============================================================================
# STEP 2: FLUX IMAGE COMPILER - GRAY MANNEQUIN FULLY CLOTHED
# =============================================================================

GPT_IMAGE_PROMPT_COMPILER = """
Convert outfit to Flux prompt for gray mannequin visualization. DO NOT change clothing/colors.

INPUT:
Sex: {sex}, Age: {age}, Height: {height}cm, Body: {body_type}
Outfit: {outfit_description}

INTERNAL BODY STRUCTURE (NOT VISIBLE - FOUNDATION ONLY): {body_description}

═══════════════════════════════════════════════════════════════════════════
FLUX PROMPT OUTPUT - GRAY MANNEQUIN FULLY CLOTHED
═══════════════════════════════════════════════════════════════════════════

Professional fashion photography: Full-body gray mannequin COMPLETELY CLOTHED in outfit, A-pose, front view, studio lighting.

🎯 CRITICAL INSTRUCTION: The mannequin body is NEVER VISIBLE. Only clothing is visible. The mannequin is the INVISIBLE FOUNDATION that gives natural shape to the clothes.

MANNEQUIN FOUNDATION (COMPLETELY HIDDEN BY CLOTHING):
- Single monochromatic gray mannequin (HEX #808080, RGB 128,128,128)
- ZERO facial features: smooth featureless egg-shaped head (no eyes, no nose, no mouth, no ears)
- Complete gray surface underneath all clothing
- {sex} proportions, {body_type} build providing natural clothing structure
- Height: {height}cm
- Internal anatomy: {body_description}
- ⚠️ MANNEQUIN BODY IS 100% COVERED - NO GRAY SKIN VISIBLE ANYWHERE
- ⚠️ Only head/neck area shows gray surface (featureless)
- ⚠️ Hands are gray (featureless, smooth, no details)

CRITICAL COVERAGE RULES:
✓ Gray mannequin head: VISIBLE (featureless, smooth, egg-shaped)
✓ Gray mannequin neck: VISIBLE up to collar line
✓ Gray mannequin hands: VISIBLE (smooth, no fingernails/lines)
✓ Gray mannequin body/torso: 100% HIDDEN under clothing
✓ Gray mannequin arms: 100% HIDDEN under sleeves
✓ Gray mannequin legs: 100% HIDDEN under pants
✓ Gray mannequin feet: 100% HIDDEN inside shoes
✓ NO gray surface visible except head, neck, and hands

POSE SPECIFICATION (MANDATORY):
- Strict A-pose: standing upright, perfectly frontal orientation
- Feet shoulder-width apart, parallel, flat on ground
- Arms extended exactly 20° from body sides
- Palms facing forward, fingers naturally extended
- ⚠️ HANDS COMPLETELY VISIBLE AND OUTSIDE ALL CLOTHING
- ⚠️ Hands positioned AWAY from any pockets/sides
- ⚠️ NO hands in pockets - hands must be clearly visible outside garments
- ⚠️ Arms hang naturally at 20° angle, NOT touching pockets
- Head centered, facing forward (featureless)
- Spine straight, shoulders level
- Weight evenly distributed on both feet
- Static neutral product photography stance

OUTFIT RENDERING (FULLY COVERING MANNEQUIN):
{outfit_description}

⚠️ ABSOLUTE REQUIREMENT: Every garment from the outfit description MUST be visibly present and accurately rendered in the final image.

CLOTHING-TO-BODY CORRELATION:
The invisible mannequin body structure creates natural clothing shape:
{clothing_fit_rules}

FIT SPECIFICATIONS:
- {fit_instruction}
- Clothing sized LARGER than mannequin body to create natural draping
- Significant air gaps between fabric and hidden body structure
- Natural fabric draping with gravity folds
- Deep shadows in creases show fabric-to-body separation
- NO tight/shrink-wrapped appearance on any garment
- Clothing hangs loosely with volume and movement
- Fabric behaves independently, responding to gravity

FABRIC PHYSICS:
- Realistic fabric weight pulls downward naturally
- Wrinkles and folds from natural draping
- Shadow depth indicates separation from hidden mannequin body
- Fabric tension only where garment naturally rests (shoulders, waist)
- NO vacuum-sealed appearance
- Natural bunching and stacking at joints

PANTS CRITICAL RULES:
- Full-length reaching TOP of shoes
- Fabric pools slightly at ankles creating natural "break"
- Realistic fabric stacking above footwear
- NO gray mannequin ankles/legs visible - completely covered
- Pants completely hide gray mannequin legs
- Fabric naturally covers shoe opening

FOOTWEAR RENDERING:
- Volumetric 3D shoes completely enclosing mannequin feet
- NO gray mannequin feet visible - feet 100% INSIDE shoes
- Dimensional construction with thick soles (2-4cm)
- Shoes firmly on ground, supporting weight
- Realistic material textures (leather grain, canvas weave)
- Proper shoe anatomy: toe box, vamp, quarters, heel, outsole

NECKLINE ACCURACY (CRITICAL):
- Match outfit description EXACTLY
- "crewneck" → round neckline at base of neck (NO HOOD, shows gray neck)
- "turtleneck" → high collar covering gray neck (NO HOOD)
- "button-down" → collared shirt with visible buttons (shows gray neck)
- "v-neck" → V-shaped neckline (shows gray neck)
- "henley" → partial button placket (shows gray neck)
- NO hoods unless explicitly stated in outfit description

SLEEVES AND ARMS:
- Long sleeves: cover gray mannequin arms completely to wrists
- Short sleeves: cover gray mannequin arms to mid-bicep or elbow
- Sleeveless: gray mannequin arms visible
- Fabric hangs loosely from arms, not tight
- Natural sleeve draping and fabric folds

TOP GARMENTS:
- Cover gray mannequin torso completely (chest, stomach, back)
- Fabric hangs with natural volume and draping
- Relaxed fit shows air gaps through shadow depth
- NO gray mannequin body visible through or under top

OUTERWEAR (if present):
- Layered over base top garment
- Covers underlying garments appropriately
- Shows depth through layering shadows
- Natural fabric weight creates realistic drape

COLOR RENDERING (FROM SANZO WADA PALETTES):
- Extract EXACT colors from outfit description
- Render colors VIBRANT and accurately saturated
- Maintain true color values from description
- Examples from outfit: "Camel" → warm tan #C19A6B, "Navy" → deep blue #000080
- NO color desaturation or shifting
- Colors remain consistent across all lighting

FABRIC TEXTURE RENDERING:
- Cotton: soft matte surface with subtle weave
- Wool: visible knit pattern, texture depth, matte finish
- Denim: pronounced twill weave with natural fade
- Leather: natural grain texture, subtle sheen
- Linen: textured weave with natural slubs
- Silk: smooth surface with lustrous sheen
- Cashmere: ultra-fine texture, soft appearance
- Canvas: rough textured weave, matte

LIGHTING SETUP:
- Professional studio three-point lighting
- Key light: 45° frontal-right, soft diffused
- Fill light: 45° frontal-left, lower intensity  
- Rim light: behind subject, edge definition
- Even illumination on all garments
- Soft shadows showing fabric depth and draping
- Highlights enhance color vibrancy and texture
- Subtle ambient occlusion in fabric folds

CAMERA SPECIFICATIONS:
- Full body shot: head to feet completely visible
- Subject centered with balanced composition
- Eye-level camera position
- 50mm equivalent focal length (no distortion)
- Sharp focus on all garments
- Professional fashion photography framing

BACKGROUND:
- Seamless studio backdrop: light neutral gray (RGB 220,220,220)
- Infinite sweep (no visible floor/wall junction)
- Slight gradient: lighter at top
- Clean professional studio environment

CRITICAL QUALITY CHECKS:
✓ Gray mannequin head VISIBLE: featureless, smooth, egg-shaped (HEX #808080)
✓ Gray mannequin neck VISIBLE: up to collar line (HEX #808080)
✓ Gray mannequin hands VISIBLE: smooth, featureless (HEX #808080)
✓ Gray mannequin body: 100% HIDDEN under clothing (NOT VISIBLE)
✓ Gray mannequin arms: 100% HIDDEN under sleeves (NOT VISIBLE)
✓ Gray mannequin legs: 100% HIDDEN under pants (NOT VISIBLE)
✓ Gray mannequin feet: 100% HIDDEN inside shoes (NOT VISIBLE)
✓ ONE mannequin only (not multiple)
✓ ZERO facial features (no eyes/nose/mouth)
✓ Fabrics LOOSE/RELAXED: {fit_instruction}
✓ ⚠️ HANDS OUTSIDE POCKETS - arms extended 20°, palms visible
✓ ⚠️ NO hands in pockets - hands away from body
✓ Shoes completely enclose feet (NO gray visible)
✓ Pants cover legs fully (NO gray visible)
✓ All garments from outfit description present and visible
✓ Colors match description exactly (vibrant, accurate)
✓ Neckline correct per description
✓ Professional studio lighting

AVOID (CRITICAL FAILURES):
❌ Visible gray mannequin body/torso under clothing
❌ Visible gray mannequin arms under sleeves
❌ Visible gray mannequin legs under pants
❌ Visible gray mannequin feet (must be inside shoes)
❌ ANY facial features (eyes, nose, mouth, ears)
❌ Hands in pockets (NEVER)
❌ Arms touching or near pockets
❌ Multiple mannequins
❌ Tight/clingy clothing
❌ Missing garments from outfit description
❌ Wrong colors or desaturated colors
❌ Wrong necklines (hoods when not specified)

MANDATORY RENDERING PRINCIPLE:
The gray mannequin (#808080) is the INVISIBLE STRUCTURAL FOUNDATION that gives natural human shape to the clothing. Like a department store mannequin, only the head, neck, and hands are visible in gray - the entire body is COMPLETELY HIDDEN by the clothing. The outfit must match the description EXACTLY with all garments visible and properly fitted according to {fit_instruction}.

FINAL OUTPUT DESCRIPTION:
Professional fashion product photography of FULLY CLOTHED outfit on gray mannequin (#808080). Featureless gray head, neck, and hands visible. Mannequin in strict A-pose with hands outside pockets, arms at 20°. Complete outfit as described covering entire mannequin body. Relaxed-fit garments with natural draping. Vibrant accurate colors from Sanzo Wada palettes. Professional studio lighting. Clean backdrop.

═══════════════════════════════════════════════════════════════════════════
KEY VISUALIZATION PRINCIPLE:
═══════════════════════════════════════════════════════════════════════════
Think: Department store display mannequin wearing complete outfit.
- Gray featureless head (#808080): VISIBLE
- Gray neck (#808080): VISIBLE to collar
- Gray hands (#808080): VISIBLE, positioned away from body
- Gray body: INVISIBLE (under clothing)
- Clothing: FULLY VISIBLE with all garments present
- Result: Professional outfit visualization on mannequin base
""".strip()

# =============================================================================
# STYLING TIPS
# =============================================================================

GPT_STYLING_TIPS_PROMPT = """
SEASON: {season}
CLIENT: {age}yo {sex}, {height}cm, {body_type}
ALTERNATIVE COLORS: {alternative_palette}

Generate 50-word max seasonal guidance. DO NOT describe outfit.

Include: fabrics, silhouettes, footwear, 3 colors from alternative palette, styling technique.

Professional, concise, max 50 words.
""".strip()


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_age_styling_rules(age: int, style_vibe: str) -> str:
    """Age-appropriate rules."""
    if age < 20:
        return "NO ties/bowties. Youthful, modern pieces. Watch and belt only." if style_vibe == "elegant" else "Youthful trends, sneakers, relaxed."
    elif age < 30:
        return "Balance trends with sophistication."
    elif age < 40:
        return "Quality over trends."
    return "Classic, sophisticated."


def get_accessories_rules(age: int, style_vibe: str) -> str:
    """Accessories by age."""
    if age < 20 and style_vibe == "elegant":
        return "Watch, belt ONLY. NO ties."
    return "Watch, belt, optional tie if elegant."


def get_fit_multiplier(body_type: str) -> tuple:
    """Get fit multiplier based on body type.

    Returns:
        tuple: (multiplier_text, flux_instruction)
    """
    multipliers = {
        "slim": ("Garments 1.7x larger than standard for comfortable drape",
                 "ALL garments 1.7x LARGER than standard"),
        "athletic": ("Garments 1.8x larger than standard for relaxed athletic fit",
                     "ALL garments 1.8x LARGER than standard (extra room for athletic build)"),
        "average": ("Garments 1.8x larger than standard for comfortable relaxed fit",
                    "ALL garments 1.8x LARGER than standard"),
        "muscular": ("Garments 1.9x larger than standard with extra room for muscle mass",
                     "ALL garments 1.9x LARGER than standard (significant room for muscles)"),
        "stocky": ("Garments 2.5x larger than standard for maximum comfort and flow",
                   "ALL garments 2.5x LARGER than standard (MORE THAN DOUBLE SIZE for comfort)"),
        "plus-size": ("Garments 2.6x larger than standard for flowing comfortable fit",
                      "ALL garments 2.6x LARGER than standard (MORE THAN DOUBLE SIZE for flowing fit)")
    }
    return multipliers.get(body_type, multipliers["average"])


def get_anatomy_correlation(body_type: str, sex: str) -> str:
    """Get anatomical correlation rules for clothing fit.

    Args:
        body_type: Body type classification
        sex: Gender for anatomical adjustments

    Returns:
        str: Detailed anatomical correlation rules
    """
    base_rules = CLOTHING_ANATOMY_CORRELATION.get(body_type, CLOTHING_ANATOMY_CORRELATION["average"])

    anatomy_desc = f"""
The invisible mannequin body ({body_type}) creates these natural clothing behaviors:

TOPS: {base_rules['tops']}
PANTS: {base_rules['pants']}
OVERALL: {base_rules['fit_notes']}

GENDER STRUCTURE ({sex.upper()}):
"""

    if sex.lower() == "male":
        anatomy_desc += """- Broader shoulder structure creates fabric draping from shoulder points
- Straighter torso silhouette with minimal waist definition
- Pants hang straight from hips with relaxed leg silhouette"""
    else:
        anatomy_desc += """- Narrower shoulder structure with softer draping
- Natural waist definition may show in fitted styles
- Pants accommodate hip curves in relaxed fits"""

    return anatomy_desc.strip()


def get_body_type_description(body_type: str, age: int) -> str:
    """Get detailed body description for internal structure."""
    return BODY_TYPE_VISUAL_RULES.get(body_type, BODY_TYPE_VISUAL_RULES["average"])


def get_clothing_fit_rules(body_type: str) -> str:
    """Get specific clothing fit rules for body type.

    Args:
        body_type: Body type classification

    Returns:
        str: Clothing-to-body fit correlation rules
    """
    rules = CLOTHING_ANATOMY_CORRELATION.get(body_type, CLOTHING_ANATOMY_CORRELATION["average"])

    return f"""
TOPS FIT: {rules['tops']}
PANTS FIT: {rules['pants']}
GENERAL FIT NOTES: {rules['fit_notes']}
""".strip()


def get_sex_description(sex: str) -> str:
    return "male" if sex.lower() == "male" else "female"


def build_outfit_generation_prompt(user_data: dict, measurements: dict) -> str:
    """Build outfit generation prompt."""
    style_description = user_data.get("style_description", "casual")
    body_type = user_data.get("body_type", "average")
    height = user_data.get("height", 170)
    sex = user_data.get("sex", "male")
    age = user_data.get("age", 25)

    brands = user_data.get("favorite_brands", [])
    brands_str = ", ".join(brands) if brands else "None"

    style_vibe = determine_style_vibe(style_description)
    pants_fit = get_fit_for_body_type(body_type, "pants", style_vibe)
    tops_fit = get_fit_for_body_type(body_type, "tops", style_vibe)

    fit_multiplier, _ = get_fit_multiplier(body_type)

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
        brands=brands_str,
        style_description=style_description[:100],
        color_palette=color_palette_str,
        style_vibe=style_vibe,
        pants_fit=pants_fit,
        tops_fit=tops_fit,
        fit_multiplier=fit_multiplier,
        season_outerwear=season_outerwear,
        age_styling_rules=age_styling_rules,
        accessories_rules=accessories_rules
    )


def build_image_prompt_compiler(user_data: dict, measurements: dict, outfit_description: str) -> str:
    """Build image compiler prompt - gray mannequin fully clothed.

    Args:
        user_data: User profile data
        measurements: Body measurements dictionary
        outfit_description: Generated outfit description text

    Returns:
        str: Complete Flux prompt for gray mannequin visualization
    """
    sex = user_data.get("sex", "male")
    age = user_data.get("age", 25)
    height = user_data.get("height", 170)
    body_type = user_data.get("body_type", "average")

    # Get internal body structure description (not visible, foundation only)
    body_description = get_body_type_description(body_type, age)

    # Get fit instruction
    _, fit_instruction = get_fit_multiplier(body_type)

    # Get clothing fit rules based on invisible body structure
    clothing_fit_rules = get_clothing_fit_rules(body_type)

    # Validate required parameters
    if not all([sex, age, height, body_type, body_description, outfit_description]):
        raise ValueError("Missing required parameters for image prompt compilation")

    try:
        return GPT_IMAGE_PROMPT_COMPILER.format(
            sex=sex,
            age=age,
            height=height,
            body_type=body_type,
            body_description=body_description,
            outfit_description=outfit_description,
            fit_instruction=fit_instruction,
            clothing_fit_rules=clothing_fit_rules
        )
    except KeyError as e:
        raise ValueError(f"Missing template variable in prompt: {e}")
    except Exception as e:
        raise RuntimeError(f"Failed to build image prompt: {e}")


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
    """Format response with measurements."""
    dimensions = [
        f"Chest: {measurements.get('chest_circumference', 'N/A')}cm",
        f"Waist: {measurements.get('waist_circumference', 'N/A')}cm",
        f"Hips: {measurements.get('hip_circumference', 'N/A')}cm",
        f"Leg: {measurements.get('leg_length', 'N/A')}cm",
        f"Arm: {measurements.get('arm_length', 'N/A')}cm",
        f"S/H: {measurements.get('shoulder_hip_ratio', 'N/A')}",
        f"BMI: {measurements.get('bmi', 'N/A')}"
    ]

    return f"""{outfit_description}

💡 Styling Tip: {styling_tips}

📏 Measurements: {' | '.join(dimensions)}"""


# =============================================================================
# VALIDATION FUNCTIONS
# =============================================================================

def validate_user_data(user_data: dict) -> bool:
    """Validate user data has all required fields."""
    required_fields = ["sex", "age", "height", "weight", "body_type"]

    for field in required_fields:
        if field not in user_data:
            raise ValueError(f"Missing required field: {field}")
        if user_data[field] is None:
            raise ValueError(f"Field cannot be None: {field}")

    if user_data["body_type"] not in BODY_TYPE_VISUAL_RULES:
        raise ValueError(
            f"Invalid body type: {user_data['body_type']}. "
            f"Must be one of: {', '.join(BODY_TYPE_VISUAL_RULES.keys())}"
        )

    if not (0 < user_data["age"] < 120):
        raise ValueError(f"Invalid age: {user_data['age']}")
    if not (100 < user_data["height"] < 250):
        raise ValueError(f"Invalid height: {user_data['height']}")
    if not (30 < user_data["weight"] < 300):
        raise ValueError(f"Invalid weight: {user_data['weight']}")

    return True


def validate_outfit_description(outfit_description: str) -> bool:
    """Validate outfit description contains required elements."""
    if not outfit_description or len(outfit_description.strip()) < 50:
        raise ValueError("Outfit description is too short or empty")

    color_indicators = ["blue", "red", "green", "black", "white", "gray", "grey", "brown",
                        "navy", "olive", "khaki", "beige", "tan", "camel", "cream", "ivory"]
    color_count = sum(1 for color in color_indicators if color.lower() in outfit_description.lower())

    if color_count < 2:
        raise ValueError("Outfit description missing color specifications")

    return True


# =============================================================================
# CONSTANTS
# =============================================================================

VALID_BODY_TYPES = ["slim", "athletic", "average", "muscular", "stocky", "plus-size"]
VALID_SEXES = ["male", "female"]
VALID_SEASONS = ["FW", "SS"]


# =============================================================================
# ERROR HANDLING UTILITIES
# =============================================================================

def safe_format_prompt(template: str, **kwargs) -> str:
    """Safely format prompt template with error handling.

    Args:
        template: Prompt template string
        **kwargs: Template variables

    Returns:
        str: Formatted prompt

    Raises:
        ValueError: If template formatting fails
    """
    try:
        return template.format(**kwargs)
    except KeyError as e:
        raise ValueError(f"Missing template variable: {e}")
    except Exception as e:
        raise ValueError(f"Prompt formatting failed: {e}")