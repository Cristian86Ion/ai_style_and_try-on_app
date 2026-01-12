import os
import json
import requests
from dotenv import load_dotenv
from openai import OpenAI
from random import choice

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")

openai_client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None


# CATEGORY MAPPING

CATEGORIES = {
    "top": ["t-shirt", "shirt", "hoodie", "jumper", "sweater", "top", "sweatshirt",
            "tank_top", "cardigan", "blouse", "bodysuit", "polo"],
    "pants": ["pants", "trousers", "jeans", "jorts", "skirt", "leggings",
              "joggers", "jogger", "shorts", "dress"],
    "layer": ["jacket", "coat", "blazer", "overshirt", "parka", "vest", "bomber"]
}

def get_category(raw: str) -> str | None:
    raw = raw.lower().strip()
    for cat, variants in CATEGORIES.items():
        if raw in variants or any(v in raw for v in variants):
            return cat
    return None


# ITEM SELECTION

def select_item(items: list, category: str, filters: dict) -> dict | None:
    gender = filters.get("gender", "man")
    style = filters.get("style", "casual")
    brand = filters.get("brand")

    matches = [i for i in items
               if get_category(i.get("category", "")) == category
               and i.get("gender") == gender]

    if not matches:
        matches = [i for i in items if get_category(i.get("category", "")) == category]

    if not matches:
        return None

    # Prefer brand
    if brand:
        branded = [m for m in matches if m.get("brand", "").lower() == brand.lower()]
        if branded:
            matches = branded

    # Prefer style
    styled = [m for m in matches if m.get("style") == style]
    if styled:
        matches = styled

    return choice(matches)


# MAIN PIPELINE

def generate_outfit_pipeline(user_data: dict) -> dict:

    if not openai_client:
        raise RuntimeError("OPENAI_API_KEY missing")

    from body_measurements import compute_body_measurements
    from sanzo_wada_colors import get_current_season, get_two_color_palettes, format_color_palette_for_prompt
    from prompts import (
        build_style_extraction_prompt, build_semantic_filters,
        build_image_prompt, build_styling_tips_prompt,
        build_outfit_description, validate_user_data,
        generate_ai_shoe_description, safe_get_colors
    )
    from local.local_store import load_all_items

    # Validate
    validate_user_data(user_data)

    # Body measurements for accurate proportions
    measurements = compute_body_measurements(
        height=user_data["height"],
        weight=user_data["weight"],
        sex=user_data["sex"]
    )
    print(
        f"Body: chest={measurements['chest_circumference']}cm, waist={measurements['waist_circumference']}cm, BMI={measurements['bmi']}")

    # Season from datetime
    season = get_current_season()
    print(f"Season: {season}")

    # Style extraction
    style_prompt = build_style_extraction_prompt(user_data)
    style_keywords = extract_style_keywords(style_prompt)
    print(f"Style keywords: {style_keywords.get('style_keywords', [])}")

    # Get Sanzo Wada color palettes
    primary_palette, alt_palette = get_two_color_palettes(style_keywords.get('style_keywords', ['casual']))
    print(f"Palette: {primary_palette['name']} ({primary_palette['mood']})")
    print(f"Alt palette: {alt_palette['name']}")

    # Filters
    filters = build_semantic_filters(style_keywords, user_data, season)
    print(f"Filters: {filters}")

    # Load items
    all_items = load_all_items()
    print(f"Loaded {len(all_items)} items")

    # Select outfit
    selected_items = {
        "top": select_item(all_items, "top", filters),
        "pants": select_item(all_items, "pants", filters),
        "layer": select_item(all_items, "layer", filters)
    }

    # Log with colors and URLs
    for key, item in selected_items.items():
        if item:
            colors = safe_get_colors(item)
            url = item.get('url', 'no url')[:50]
            print(f"{key.upper()}: {item.get('brand')} {item.get('category')} | {colors} | {url}...")

    if not selected_items["top"] and not selected_items["pants"]:
        raise RuntimeError("No clothing found!")

    # Collect colors for shoe matching
    outfit_colors = []
    for item in selected_items.values():
        if item:
            outfit_colors.extend(safe_get_colors(item))

    # Generate AI shoe with fit rules
    ai_shoe = generate_ai_shoe_description(
        style=filters.get('style', 'casual'),
        gender=filters.get('gender', 'man'),
        outfit_colors=outfit_colors,
        season=season,
        body_type=user_data.get('body_type', 'average')
    )
    print(f"Shoe: {ai_shoe.get('description')} ({ai_shoe.get('fit')})")

    # Generate image with all features
    image_url = None
    if TOGETHER_API_KEY:
        try:
            prompt = build_image_prompt(
                user_data,
                selected_items,
                ai_shoe,
                measurements,
                primary_palette
            )
            print(f"Prompt ({len(prompt)} chars)")
            image_url = generate_image(prompt)
            print(f"Image generated!")
        except Exception as e:
            print(f"Image failed: {e}")

    # Styling tips with alt palette
    tips = generate_tips(build_styling_tips_prompt(user_data, selected_items, ai_shoe, alt_palette))

    # Product links
    product_links = {k: v['url'] for k, v in selected_items.items() if v and v.get('url')}

    return {
        "outfit_description": build_outfit_description(selected_items, ai_shoe),
        "image_url": image_url,
        "styling_tips": tips,
        "measurements": measurements,
        "product_links": product_links,
        "selected_items": selected_items,
        "ai_shoe": ai_shoe,
        "season": season,
        "color_palette": format_color_palette_for_prompt(primary_palette),
        "alternative_palette": format_color_palette_for_prompt(alt_palette)
    }


# =============================================================================
# LLM CALLS
# =============================================================================

def extract_style_keywords(prompt: str) -> dict:
    try:
        resp = openai_client.chat.completions.create(
            model="gpt-5-mini",
            messages=[
                {"role": "system", "content": "Return JSON only."},
                {"role": "user", "content": prompt}
            ]
        )
        content = resp.choices[0].message.content.strip()
        if "```" in content:
            content = content.split("```")[1].replace("json", "").strip()
        return json.loads(content)
    except:
        return {"style_keywords": ["casual"], "color_preferences": ["black"]}


def generate_image(prompt: str) -> str:
    resp = requests.post(
        "https://api.together.xyz/v1/images/generations",
        headers={"Authorization": f"Bearer {TOGETHER_API_KEY}", "Content-Type": "application/json"},
        json={
            "model": "black-forest-labs/FLUX.1-schnell",
            "prompt": prompt,
            "width": 768,
            "height": 1024,
            "steps": 4,
            "n": 1
        },
        timeout=60
    )
    resp.raise_for_status()
    return resp.json()["data"][0]["url"]


def generate_tips(prompt: str) -> str:
    try:
        resp = openai_client.chat.completions.create(
            model="gpt-5-mini",
            messages=[
                {"role": "system", "content": "Fashion stylist. 2 sentences max."},
                {"role": "user", "content": prompt}
            ]
        )
        return resp.choices[0].message.content.strip()[:250]
    except:
        return "Style with confidence!"