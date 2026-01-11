"""
LLM Service for Semantic Search-Based Outfit Generation
Pipeline: Style Extraction → DB Query → Mannequin → Clothing Overlay → Tips
"""

import os
import json
import requests
from dotenv import load_dotenv
from openai import OpenAI
from random import shuffle

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")

openai_client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None


# =============================================================================
# PIPELINE ORCHESTRATOR
# =============================================================================

def generate_outfit_pipeline(user_data: dict) -> dict:
    """
    Five-step pipeline for real clothing database outfit generation.

    1. Extract style keywords (GPT)
    2. Query database with semantic filters
    3. Select outfit items (top/pants/shoe/layer)
    4. Generate mannequin + overlay clothing (Flux)
    5. Generate styling tips (GPT)
    """

    if not openai_client:
        raise RuntimeError("OPENAI_API_KEY is missing")

    from body_measurements import compute_body_measurements
    from prompts import (
        build_style_extraction_prompt,
        build_semantic_filters,
        build_mannequin_prompt,
        build_overlay_prompt,
        build_styling_tips_prompt,
        validate_user_data
    )
    from backend.database import dbread
    from processor.clotheselector import select_outfit_items, validate_outfit, get_product_links
    from processor.getimages import get as get_image


    print("\n" + "=" * 60)
    print("VALIDATING USER DATA")
    print("=" * 60)

    try:
        validate_user_data(user_data)
        print("Validation passed")
    except ValueError as e:
        print(f"Validation Error: {e}")
        raise

    # Calculate measurements
    print("\n" + "=" * 60)
    print("CALCULATING BODY MEASUREMENTS")
    print("=" * 60)

    measurements = compute_body_measurements(
        height=user_data.get("height", 170),
        weight=user_data.get("weight", 70),
        sex=user_data.get("sex", "male")
    )

    print(f"Measurements:")
    print(f"   Chest: {measurements['chest_circumference']}cm")
    print(f"   Waist: {measurements['waist_circumference']}cm")
    print(f"   Hips: {measurements['hip_circumference']}cm")
    print(f"   Leg Length: {measurements['leg_length']}cm")
    print(f"   BMI: {measurements['bmi']:.1f}")

    # STEP 1: Extract style keywords
    print("\n" + "=" * 60)
    print("STEP 1: EXTRACTING STYLE KEYWORDS (GPT)")
    print("=" * 60)

    style_prompt = build_style_extraction_prompt(user_data)
    style_keywords = extract_style_keywords(style_prompt)

    print(f"Keywords extracted:")
    print(f"   Style: {style_keywords.get('style_keywords', [])}")
    print(f"   Colors: {style_keywords.get('color_preferences', [])}")
    print(f"   Fit: {style_keywords.get('fit_preferences', [])}")

    # STEP 2: Query database
    print("\n" + "=" * 60)
    print("🗄STEP 2: QUERYING DATABASE")
    print("=" * 60)

    filters = build_semantic_filters(style_keywords, user_data, "FW")
    print(f"   Filters: {filters}")

    db_results = dbread.query(filters)
    print(f"Found {len(db_results)} items in database")

    if len(db_results) == 0:
        raise ValueError("No items found matching filters. Try different style/brand.")


    shuffle(db_results)

    print("\n" + "=" * 60)
    print("STEP 3: SELECTING OUTFIT ITEMS")
    print("=" * 60)

    outfit = select_outfit_items(db_results)
    is_valid, missing = validate_outfit(outfit)

    if not is_valid:
        raise ValueError(f"Incomplete outfit - missing: {', '.join(missing)}")

    print(f"Outfit selected:")
    print(f"   TOP: {outfit['top']['brand']} {outfit['top']['category']} - {outfit['top']['id']}")
    print(f"   PANTS: {outfit['pants']['brand']} {outfit['pants']['category']} - {outfit['pants']['id']}")
    print(f"   SHOE: {outfit['shoe']['brand']} - {outfit['shoe']['id']}")
    if outfit.get('layer'):
        print(f"   LAYER: {outfit['layer']['brand']} {outfit['layer']['category']} - {outfit['layer']['id']}")
    else:
        print(f"   LAYER: None")

    product_links = get_product_links(outfit)

    image_url = None
    if TOGETHER_API_KEY:
        try:
            print("\n" + "=" * 60)
            print("🖼STEP 4: GENERATING MANNEQUIN + CLOTHING OVERLAY")
            print("=" * 60)

            # First generate mannequin
            mannequin_prompt = build_mannequin_prompt(user_data, measurements)
            print(f"   Generating base mannequin...")

            # Then add clothing overlay instructions
            overlay_prompt = build_overlay_prompt(user_data, measurements, outfit)

            # Combine prompts
            full_prompt = f"{mannequin_prompt}\n\n{overlay_prompt}"

            print(f"   Prompt length: {len(full_prompt)} chars")

            image_url = generate_outfit_image(full_prompt)

            if image_url:
                print(f"Image generated successfully")
                print(f"   URL: {image_url[:60]}...")
            else:
                print("⚠No image URL returned")

        except Exception as e:
            print(f"Image generation failed: {e}")
            import traceback
            traceback.print_exc()
            image_url = None
    else:
        print("\nTOGETHER_API_KEY not found - skipping image generation")

    print("\n" + "=" * 60)
    print("STEP 5: GENERATING STYLING TIPS (GPT)")
    print("=" * 60)

    tips_prompt = build_styling_tips_prompt(user_data, outfit)
    styling_tips = generate_styling_tips(tips_prompt)

    print(f"Styling tips generated ({len(styling_tips)} chars)")
    print(f"   {styling_tips}")


    print("\n" + "=" * 60)
    print("FINAL RESPONSE")
    print("=" * 60)

    outfit_description = format_outfit_description(outfit, product_links)
    formatted_response = format_complete_response(
        outfit_description,
        styling_tips,
        measurements,
        product_links
    )

    print(f"Response complete")
    print("=" * 60 + "\n")

    return {
        "outfit_description": outfit_description,
        "image_url": image_url,
        "styling_tips": styling_tips,
        "measurements": measurements,
        "product_links": product_links,
        "formatted_response": formatted_response,
        "selected_items": outfit
    }


# =============================================================================
# LLM FUNCTIONS
# =============================================================================

def extract_style_keywords(prompt: str) -> dict:
    """
    STEP 1: Use GPT to extract semantic style keywords.
    Returns JSON dict with style_keywords, color_preferences, etc.
    """

    try:
        response = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a fashion AI that extracts semantic keywords. Return ONLY valid JSON, no markdown, no extra text."
                },
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )

        content = response.choices[0].message.content.strip()

        # Remove markdown if present
        if content.startswith("```"):
            content = content.split("```")[1]
            if content.startswith("json"):
                content = content[4:]

        keywords = json.loads(content)

        if not isinstance(keywords, dict):
            raise ValueError("Response is not a dict")

        return keywords

    except json.JSONDecodeError as e:
        print(f"JSON parse error: {e}")
        print(f"   Raw response: {content}")
        # Return defaults
        return {
            "style_keywords": ["casual"],
            "color_preferences": ["black"],
            "fit_preferences": ["regular"],
            "season_appropriate": []
        }
    except Exception as e:
        print(f"GPT keyword extraction error: {e}")
        raise


def generate_outfit_image(prompt: str) -> str:
    """
    STEP 4: Generate mannequin + clothing overlay using Flux.
    """

    try:
        print("   Sending request to Flux API...")

        response = requests.post(
            "https://api.together.xyz/v1/images/generations",
            headers={
                "Authorization": f"Bearer {TOGETHER_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": "black-forest-labs/FLUX.1-schnell",
                "prompt": prompt,
                "width": 768,
                "height": 1024,
                "steps": 4,
                "n": 1,
            },
            timeout=45
        )
        response.raise_for_status()

        data = response.json()
        if "data" not in data or len(data["data"]) == 0:
            raise ValueError("No image data in response")

        print("Flux generation successful")
        return data["data"][0]["url"]

    except requests.exceptions.Timeout:
        print("Flux API timeout (45s)")
        raise
    except requests.exceptions.RequestException as e:
        print(f"Flux API error: {e}")
        raise


def generate_styling_tips(prompt: str) -> str:
    """
    STEP 5: Generate styling tips using GPT.
    """

    try:
        response = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "Fashion stylist. Concise, practical advice. Max 50 words."
                },
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )

        content = response.choices[0].message.content
        if not content:
            raise ValueError("Empty styling tips")

        text = content.strip()

        # Enforce 50 word limit
        words = text.split()
        if len(words) > 50:
            text = " ".join(words[:50]) + "..."

        return text

    except Exception as e:
        print(f"GPT styling tips error: {e}")
        raise


# =============================================================================
# FORMATTING HELPERS
# =============================================================================

def format_outfit_description(outfit: dict, product_links: dict) -> str:
    """Format outfit items into readable description."""

    lines = []

    top = outfit.get('top', {})
    lines.append(
        f"TOP: {top.get('brand', 'N/A').upper()} "
        f"{top.get('category', 'N/A').replace('_', ' ').title()} - "
        f"{', '.join(top.get('colors', ['N/A']))}"
    )

    pants = outfit.get('pants', {})
    lines.append(
        f"PANTS: {pants.get('brand', 'N/A').upper()} "
        f"{pants.get('category', 'N/A').replace('_', ' ').title()} - "
        f"{', '.join(pants.get('colors', ['N/A']))}"
    )

    shoe = outfit.get('shoe', {})
    lines.append(
        f"SHOE: {shoe.get('brand', 'N/A').upper()} - "
        f"{', '.join(shoe.get('colors', ['N/A']))}"
    )

    layer = outfit.get('layer')
    if layer:
        lines.append(
            f"LAYER: {layer.get('brand', 'N/A').upper()} "
            f"{layer.get('category', 'N/A').replace('_', ' ').title()} - "
            f"{', '.join(layer.get('colors', ['N/A']))}"
        )

    return "\n".join(lines)


def format_complete_response(
        outfit_description: str,
        styling_tips: str,
        measurements: dict,
        product_links: dict
) -> str:
    """Format complete response with outfit + tips + links."""

    parts = [
        "=== YOUR OUTFIT ===",
        outfit_description,
        "",
        "=== PRODUCT LINKS ===",
        f"TOP: {product_links.get('top', 'N/A')}",
        f"PANTS: {product_links.get('pants', 'N/A')}",
        f"SHOE: {product_links.get('shoe', 'N/A')}",
    ]

    if product_links.get('layer'):
        parts.append(f"LAYER: {product_links['layer']}")

    parts.extend([
        "",
        "=== STYLING TIP ===",
        styling_tips,
        "",
        "=== YOUR MEASUREMENTS ===",
        f"Chest: {measurements.get('chest_circumference', 'N/A')}cm | "
        f"Waist: {measurements.get('waist_circumference', 'N/A')}cm | "
        f"Hips: {measurements.get('hip_circumference', 'N/A')}cm | "
        f"BMI: {measurements.get('bmi', 'N/A'):.1f}"
    ])

    return "\n".join(parts)


def log_parser_output(user_message: str, parsed_data: dict):

    print("\n" + "=" * 60)
    print("INPUT PARSER BREAKDOWN")
    print("=" * 60)
    print(f"RAW INPUT: {user_message}")
    print("\nEXTRACTED DATA:")
    print(f"  • Sex: {parsed_data.get('sex')}")
    print(f"  • Height: {parsed_data.get('height')}cm")
    print(f"  • Weight: {parsed_data.get('weight')}kg")
    print(f"  • Age: {parsed_data.get('age')}yo")
    print(f"  • Body Type: {parsed_data.get('body_type')}")
    print(f"  • Brands: {parsed_data.get('favorite_brands')}")
    print(f"  • Style: {parsed_data.get('style_description')}")
    print("=" * 60)