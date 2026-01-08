# input_parser.py
"""
Parses standardized and flexible user input formats.
Prioritizes measurements from the chat message but allows fallback values.
CRITICAL: First word determines sex (male/female).
"""
import re

# Valid body types from frontend dropdown
VALID_BODY_TYPES = [
    "slim",
    "athletic",
    "average",
    "muscular",
    "stocky",
    "plus-size"
]


def parse_user_input_flexible(user_message: str, fallback_body_type: str = "average") -> dict:
    """
    Extremely flexible parser that tries to extract data from a comma-separated string.
    If parsing fails for specific fields, it uses safe defaults.

    CRITICAL: The FIRST WORD determines sex (male/female).
    """
    user_message = user_message.strip()

    # Split by "style:"
    parts = re.split(r'\bstyle:\s*', user_message, flags=re.IGNORECASE)
    measurements_part = parts[0].strip()
    style_description = parts[1].strip() if len(parts) > 1 else "casual comfortable"

    # Split measurements by comma
    measurements = [m.strip() for m in measurements_part.split(',')]

    # 1. Detect Sex (CRITICAL - First word logic)
    # The FIRST word in the message determines male or female
    raw_sex = measurements[0].lower() if len(measurements) > 0 else "male"

    # Enhanced sex detection mapping
    sex_mapping = {
        # Male variations
        'male': 'male',
        'm': 'male',
        'man': 'male',
        'boy': 'male',
        'barbat': 'male',  # Romanian
        'baiat': 'male',  # Romanian
        'b': 'male',
        # Female variations
        'female': 'female',
        'f': 'female',
        'woman': 'female',
        'girl': 'female',
        'femeie': 'female',  # Romanian
        'fata': 'female',  # Romanian
    }

    # Check exact match first
    if raw_sex in sex_mapping:
        sex = sex_mapping[raw_sex]
    # Then check if any key is contained in raw_sex
    elif any(key in raw_sex for key in ['female', 'woman', 'girl', 'femeie', 'fata']):
        sex = 'female'
    elif any(key in raw_sex for key in ['male', 'man', 'boy', 'barbat', 'baiat']):
        sex = 'male'

    print(f"🔍 Sex Detection: raw_sex='{raw_sex}' → detected sex='{sex}'")

    # 2. Extract Numbers (height, weight, age, shoe) with fallbacks based on detected sex
    def get_int(index, default):
        try:
            return int(measurements[index])
        except (ValueError, IndexError):
            return default

    # Sex-specific defaults
    if sex == 'female':
        height = get_int(1, 165)
        weight = get_int(2, 55)
        shoe_size = get_int(4, 38)
    else:  # male
        height = get_int(1, 175)
        weight = get_int(2, 75)
        shoe_size = get_int(4, 42)

    age = get_int(3, 25)  # Age is same for both

    # 3. Body Type (We take it from measurements if exists, but main.py will override)
    body_type = measurements[5].lower() if len(measurements) > 5 else fallback_body_type
    if body_type not in VALID_BODY_TYPES:
        body_type = fallback_body_type

    # 4. Brands
    brands_str = measurements[6] if len(measurements) > 6 else ""
    brands = [b.strip() for b in brands_str.split('-') if b.strip()] if brands_str else []

    result = {
        "sex": sex,
        "height": height,
        "weight": weight,
        "age": age,
        "shoe_size": shoe_size,
        "body_type": body_type,
        "favorite_brands": brands[:3],
        "style_description": style_description
    }

    print(f"✅ Parsed Result: {result}")

    return result


def format_instructions() -> str:
    return """
📝 **Format recomandat:**
`sex, inaltime, greutate, varsta, marime_pantof, tip_corp, branduri, style: descriere`

**Exemplu:**
`female, 165, 56, 25, 37, slim, zara-bershka, style: emo casual with cropped shirts`
`male, 180, 75, 28, 43, athletic, nike-adidas, style: streetwear urban`

**IMPORTANT:** Primul cuvânt (male/female) determină sexul persoanei!
""".strip()


# Testing
if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("INPUT PARSER TESTING")
    print("=" * 70 + "\n")

    test_cases = [
        "male, 173, 70, 22, 42, athletic, nike, style: elegant minimalist",
        "female, 165, 56, 25, 37, slim, zara-bershka, style: emo casual with cropped shirts",
        "male, 180, 85, 30, 44, muscular, style: sporty casual",
        "female, 158, 50, 22, 36, slim, style: romantic soft feminine",
        "man, 175, 72, 28, style: business professional",
        "woman, 168, 60, style: bohemian natural"
    ]

    for i, test in enumerate(test_cases, 1):
        print(f"\nTest {i}: {test[:60]}...")
        result = parse_user_input_flexible(test, fallback_body_type="average")
        print(f"   Sex: {result['sex']}")
        print(f"   Height: {result['height']}cm")
        print(f"   Body Type: {result['body_type']}")
        print(f"   Style: {result['style_description'][:50]}...")

    print("\n" + "=" * 70)
    print("✅ All tests completed!")
    print("=" * 70)