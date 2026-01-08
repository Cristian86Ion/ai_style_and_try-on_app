import os
import requests
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")

openai_client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None


def generate_outfit_pipeline(user_data: dict) -> dict:
    """
    TWO-STEP ARCHITECTURE:
    1. Calculate body measurements from user_data
    2. GPT generates outfit description (text only)
    3. GPT converts outfit description to Flux prompt (compiler, no creativity)
    4. Flux generates image using compiled prompt
    5. GPT generates styling tips with alternative palette
    """
    if not openai_client:
        raise RuntimeError("OPENAI_API_KEY is missing")

    from body_measurements import compute_body_measurements
    from prompts import (
        build_outfit_generation_prompt,
        build_image_prompt_compiler,
        build_styling_tips_prompt,
        format_outfit_response
    )

    print("\n" + "=" * 60)
    print("CALCULATING BODY MEASUREMENTS")
    print("=" * 60)

    # Calculate measurements from height, weight, sex
    measurements = compute_body_measurements(
        height=user_data.get("height", 170),
        weight=user_data.get("weight", 70),
        sex=user_data.get("sex", "male")
    )

    print(f"\n✅ Measurements Calculated:")
    print(f"   Chest: {measurements['chest_circumference']}cm")
    print(f"   Waist: {measurements['waist_circumference']}cm")
    print(f"   Hips: {measurements['hip_circumference']}cm")
    print(f"   BMI: {measurements['bmi']}")

    print("\n" + "=" * 60)
    print("STEP 1: GENERATING OUTFIT DESCRIPTION")
    print("=" * 60)

    # STEP 1: Generate outfit description (text only, with colors and details)
    outfit_prompt = build_outfit_generation_prompt(user_data, measurements)
    outfit_description = generate_outfit_description(outfit_prompt)

    print(f"\n✅ Outfit Description Generated:")
    print(f"{outfit_description[:200]}...")

    # STEP 2: Generate image using compiled Flux prompt
    image_url = None
    if TOGETHER_API_KEY:
        try:
            print("\n" + "=" * 60)
            print("STEP 2: COMPILING FLUX PROMPT")
            print("=" * 60)

            # GPT compiles the Flux prompt from outfit description
            compiler_prompt = build_image_prompt_compiler(user_data, measurements, outfit_description)
            flux_prompt = compile_image_prompt(compiler_prompt)

            print(f"\n✅ Flux Prompt Compiled:")
            print(f"{flux_prompt[:300]}...")

            print("\n" + "=" * 60)
            print("STEP 3: GENERATING IMAGE WITH FLUX")
            print("=" * 60)

            # Generate image
            image_url = generate_outfit_image(flux_prompt)

            if image_url:
                print(f"\n✅ Image Generated: {image_url[:50]}...")
            else:
                print("\n⚠️ Image generation returned no URL")

        except Exception as e:
            print(f"\n❌ Image generation failed: {e}")
            import traceback
            traceback.print_exc()
            image_url = None
    else:
        print("\n⚠️ TOGETHER_API_KEY not found - skipping image generation")

    # STEP 3: Generate styling tips with alternative palette
    print("\n" + "=" * 60)
    print("STEP 4: GENERATING STYLING TIPS")
    print("=" * 60)

    tips_prompt = build_styling_tips_prompt(user_data, measurements, outfit_description)
    styling_tips = generate_styling_tips(tips_prompt)

    print(f"\n✅ Styling Tips Generated:")
    print(f"{styling_tips}")

    # STEP 4: Format response with measurements
    print("\n" + "=" * 60)
    print("FORMATTING FINAL RESPONSE")
    print("=" * 60)

    formatted_text = format_outfit_response(outfit_description, styling_tips, measurements)

    print(f"\n✅ Response Formatted")
    print("=" * 60 + "\n")

    return {
        "outfit_description": outfit_description,
        "image_url": image_url,
        "styling_tips": styling_tips,
        "measurements": measurements,
        "formatted_response": formatted_text  # This includes outfit + tips + measurements
    }


def generate_outfit_description(prompt: str) -> str:
    """
    STEP 1: Generate outfit description (text only).
    This GPT call is the "Outfit Authority" - it decides what clothing to recommend.
    """
    response = openai_client.chat.completions.create(
        model="gpt-4.1-2025-04-14",
        messages=[
            {
                "role": "system",
                "content": "You are a professional fashion stylist. Generate detailed outfit descriptions with explicit color names, fabric types, neckline types, and fit specifications. Be precise and thorough."
            },
            {"role": "user", "content": prompt},
        ],
        max_tokens=600,
        temperature=0.7,
    )
    return response.choices[0].message.content.strip()


def compile_image_prompt(compiler_prompt: str) -> str:
    """
    STEP 2: Compile Flux prompt from outfit description.
    This GPT call is just a "Prompt Compiler" - it MUST NOT change clothing, colors, or add creativity.
    """
    response = openai_client.chat.completions.create(
        model="gpt-4.1-2025-04-14",
        messages=[
            {
                "role": "system",
                "content": """You are a technical prompt compiler. Your ONLY job is to fill in the template with the provided data. 

DO NOT invent clothing. DO NOT change colors. DO NOT add creative elements. DO NOT alter the outfit description.

You are converting structured data into a Flux prompt format. Be precise and literal."""
            },
            {"role": "user", "content": compiler_prompt},
        ],
        max_tokens=1200,
        temperature=0.3,  # Lower temperature for more literal compilation
    )
    return response.choices[0].message.content.strip()


def generate_outfit_image(prompt: str) -> str:
    """
    STEP 3: Generate image using Flux 1.
    """
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
    return response.json()["data"][0]["url"]


def generate_styling_tips(prompt: str) -> str:
    """
    STEP 4: Generate styling tips (50 words max).
    """
    response = openai_client.chat.completions.create(
        model="gpt-4.1-2025-04-14",
        messages=[
            {
                "role": "system",
                "content": "Fashion stylist providing seasonal trend guidance. Be concise, professional, max 50 words."
            },
            {"role": "user", "content": prompt},
        ],
        max_tokens=100,
        temperature=0.7,
    )

    text = response.choices[0].message.content.strip()
    # Ensure 50 word limit
    words = text.split()
    if len(words) > 50:
        text = " ".join(words[:50])
    return text