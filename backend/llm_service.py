import os
import requests
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")

openai_client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None

# Token tracking
total_input_tokens = 0
total_output_tokens = 0


def log_parser_output(user_message: str, parsed_data: dict):
    """Log how input was parsed."""
    print("\n" + "=" * 60)
    print("📝 INPUT PARSER BREAKDOWN")
    print("=" * 60)
    print(f"RAW INPUT: {user_message}")
    print("\nEXTRACTED DATA:")
    print(f"  • Sex: {parsed_data.get('sex')}")
    print(f"  • Height: {parsed_data.get('height')}cm")
    print(f"  • Weight: {parsed_data.get('weight')}kg")
    print(f"  • Age: {parsed_data.get('age')}yo")
    print(f"  • Shoe Size: {parsed_data.get('shoe_size')} EU")
    print(f"  • Body Type: {parsed_data.get('body_type')} (from frontend)")
    print(f"  • Brands: {parsed_data.get('favorite_brands')}")
    print(f"  • Style: {parsed_data.get('style_description')}")
    print("=" * 60)


def generate_outfit_pipeline(user_data: dict) -> dict:
    """
    THREE-STEP PIPELINE for GPT-5-mini with cost optimization.
    1. GPT-5-mini: Generate outfit description
    2. GPT-5-mini: Compile Flux prompt
    3. Flux: Generate image
    4. GPT-5-mini: Generate styling tips
    """
    global total_input_tokens, total_output_tokens

    if not openai_client:
        raise RuntimeError("OPENAI_API_KEY is missing")

    from body_measurements import compute_body_measurements
    from prompts import (
        build_outfit_generation_prompt,
        build_image_prompt_compiler,
        build_styling_tips_prompt,
        format_outfit_response,
        validate_user_data
    )

    # Validate input
    print("\n" + "=" * 60)
    print("🔍 VALIDATING USER DATA")
    print("=" * 60)

    try:
        validate_user_data(user_data)
        print("✅ Validation passed")
    except ValueError as e:
        print(f"❌ Validation Error: {e}")
        raise

    # Calculate measurements
    print("\n" + "=" * 60)
    print("📐 CALCULATING BODY MEASUREMENTS")
    print("=" * 60)

    measurements = compute_body_measurements(
        height=user_data.get("height", 170),
        weight=user_data.get("weight", 70),
        sex=user_data.get("sex", "male")
    )

    print(f"✅ Measurements:")
    print(f"   Chest: {measurements['chest_circumference']}cm")
    print(f"   Waist: {measurements['waist_circumference']}cm")
    print(f"   Hips: {measurements['hip_circumference']}cm")
    print(f"   BMI: {measurements['bmi']}")

    # Show season detection
    from prompts import get_season_info
    from datetime import datetime

    season, season_name = get_season_info()
    print(f"\n📅 Date: {datetime.now().strftime('%B %d, %Y')}")
    print(f"🌡️  Season Detected: {season_name} ({season})")

    # STEP 1: Generate outfit description
    print("\n" + "=" * 60)
    print("👔 STEP 1: GENERATING OUTFIT DESCRIPTION (GPT-5-mini)")
    print("=" * 60)

    outfit_prompt = build_outfit_generation_prompt(user_data, measurements)
    print(f"Prompt length: {len(outfit_prompt)} chars (~{len(outfit_prompt.split())} words)")

    outfit_description = generate_outfit_description(outfit_prompt)

    if not outfit_description or len(outfit_description.strip()) < 50:
        raise ValueError("Outfit description is too short or empty")

    print(f"\n✅ Outfit Generated ({len(outfit_description)} chars):")
    print(f"{outfit_description}")

    # STEP 2: Generate image
    image_url = None
    if TOGETHER_API_KEY:
        try:
            print("\n" + "=" * 60)
            print("🖼️  STEP 2: COMPILING FLUX PROMPT (GPT-5-mini)")
            print("=" * 60)

            compiler_prompt = build_image_prompt_compiler(user_data, measurements, outfit_description)
            print(f"Compiler prompt length: {len(compiler_prompt)} chars")

            flux_prompt = compile_image_prompt(compiler_prompt)

            if not flux_prompt or len(flux_prompt.strip()) < 100:
                raise ValueError("Flux prompt compilation failed")

            print(f"\n✅ Flux Prompt Compiled ({len(flux_prompt)} chars)")

            print("\n" + "=" * 60)
            print("🎨 STEP 3: GENERATING IMAGE WITH FLUX")
            print("=" * 60)

            image_url = generate_outfit_image(flux_prompt)

            if image_url:
                print(f"✅ Image Generated Successfully")
                print(f"   URL: {image_url[:60]}...")
            else:
                print("⚠️  No image URL returned")

        except Exception as e:
            print(f"\n❌ Image generation failed: {e}")
            import traceback
            traceback.print_exc()
            image_url = None
    else:
        print("\n⚠️  TOGETHER_API_KEY not found - skipping image generation")

    # STEP 3: Generate styling tips
    print("\n" + "=" * 60)
    print("💡 STEP 4: GENERATING STYLING TIPS (GPT-5-mini)")
    print("=" * 60)

    tips_prompt = build_styling_tips_prompt(user_data, measurements, outfit_description)
    styling_tips = generate_styling_tips(tips_prompt)

    print(f"✅ Styling Tips ({len(styling_tips)} chars):")
    print(f"   {styling_tips}")

    # Format response
    print("\n" + "=" * 60)
    print("📦 FORMATTING FINAL RESPONSE")
    print("=" * 60)

    formatted_text = format_outfit_response(outfit_description, styling_tips, measurements)

    # Cost summary
    print("\n" + "=" * 60)
    print("💰 TOKEN USAGE & COST ESTIMATE")
    print("=" * 60)
    print(f"Total Input Tokens:  ~{total_input_tokens:,}")
    print(f"Total Output Tokens: ~{total_output_tokens:,}")
    print(f"Image Generation:    1 image")
    print(f"\nEstimated Cost:")
    print(f"  GPT Input:   ${total_input_tokens * 0.00000025:.5f}")
    print(f"  GPT Output:  ${total_output_tokens * 0.000002:.5f}")
    print(f"  Flux Image:  $0.00200")
    total_cost = (total_input_tokens * 0.00000025) + (total_output_tokens * 0.000002) + 0.002
    print(f"  ─────────────────────")
    print(f"  TOTAL:       ${total_cost:.5f}")
    print("=" * 60 + "\n")

    return {
        "outfit_description": outfit_description,
        "image_url": image_url,
        "styling_tips": styling_tips,
        "measurements": measurements,
        "formatted_response": formatted_text
    }


def generate_outfit_description(prompt: str) -> str:
    """STEP 1: Generate outfit description using GPT-5-mini."""
    global total_input_tokens, total_output_tokens

    try:
        response = openai_client.chat.completions.create(
            model="gpt-5-mini",
            messages=[
                {
                    "role": "system",
                    "content": "Professional fashion stylist. Generate detailed outfit with explicit colors, fabrics, and necklines."
                },
                {"role": "user", "content": prompt}
            ]
        )

        # Track tokens
        total_input_tokens += response.usage.prompt_tokens
        total_output_tokens += response.usage.completion_tokens

        print(f"   Input tokens: {response.usage.prompt_tokens}")
        print(f"   Output tokens: {response.usage.completion_tokens}")

        content = response.choices[0].message.content
        if not content:
            raise ValueError("Empty response from GPT-5-mini")

        return content.strip()

    except Exception as e:
        print(f"❌ GPT-5-mini outfit error: {e}")
        raise


def compile_image_prompt(compiler_prompt: str) -> str:
    """STEP 2: Compile Flux prompt using GPT-5-mini."""
    global total_input_tokens, total_output_tokens

    try:
        response = openai_client.chat.completions.create(
            model="gpt-5-mini",
            messages=[
                {
                    "role": "system",
                    "content": "Technical compiler. Fill template with data. DO NOT invent. Be literal."
                },
                {"role": "user", "content": compiler_prompt}
            ]
        )

        # Track tokens
        total_input_tokens += response.usage.prompt_tokens
        total_output_tokens += response.usage.completion_tokens

        print(f"   Input tokens: {response.usage.prompt_tokens}")
        print(f"   Output tokens: {response.usage.completion_tokens}")

        content = response.choices[0].message.content
        if not content:
            raise ValueError("Empty compiler response")

        return content.strip()

    except Exception as e:
        print(f"❌ GPT-5-mini compiler error: {e}")
        raise


def generate_outfit_image(prompt: str) -> str:
    """STEP 3: Generate image using Flux."""
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

        print("   ✅ Flux generation successful")
        return data["data"][0]["url"]

    except requests.exceptions.Timeout:
        print("   ❌ Flux API timeout (45s)")
        raise
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Flux API error: {e}")
        raise


def generate_styling_tips(prompt: str) -> str:
    """STEP 4: Generate styling tips using GPT-5-mini."""
    global total_input_tokens, total_output_tokens

    try:
        response = openai_client.chat.completions.create(
            model="gpt-5-mini",
            messages=[
                {
                    "role": "system",
                    "content": "Fashion stylist. Seasonal guidance. Concise. Max 50 words."
                },
                {"role": "user", "content": prompt}
            ]
        )

        # Track tokens
        total_input_tokens += response.usage.prompt_tokens
        total_output_tokens += response.usage.completion_tokens

        print(f"   Input tokens: {response.usage.prompt_tokens}")
        print(f"   Output tokens: {response.usage.completion_tokens}")

        content = response.choices[0].message.content
        if not content:
            raise ValueError("Empty styling tips")

        text = content.strip()

        # Ensure 50 word limit
        words = text.split()
        if len(words) > 50:
            text = " ".join(words[:50])

        return text

    except Exception as e:
        print(f"❌ GPT-5-mini tips error: {e}")
        raise