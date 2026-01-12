import re

VALID_BODY_TYPES = ["slim", "athletic", "average", "muscular", "stocky", "plus-size"]

def parse_user_input_flexible(user_message: str, fallback_body_type: str = "average") -> dict:

    user_message = user_message.strip()

    parts = re.split(r'\bstyle:\s*', user_message, flags=re.IGNORECASE) #separare masuri de stil
    measurements_part = parts[0].strip()
    style_description = parts[1].strip() if len(parts) > 1 else ""

    tokens = [t.strip() for t in measurements_part.split(',') if t.strip()]

    raw_sex = tokens[0].lower() if len(tokens) > 0 else "male"
    sex = "female" if any(x in raw_sex for x in ["female", "woman", "femeie", "fata"]) else "male"

    def extract_number(index):
        if len(tokens) > index:
            match = re.search(r'\d+', str(tokens[index]))
            return int(match.group()) if match else None
        return None

    height = extract_number(1)
    weight = extract_number(2)
    age = extract_number(3)
    shoe_size = extract_number(4)

    brands = []
    if len(tokens) > 5:
        brands_token = tokens[5]
        if brands_token.lower() not in VALID_BODY_TYPES:

            brands = [b.strip() for b in brands_token.split(' ') if b.strip()]

    return {
        "sex": sex,
        "height": height,
        "weight": weight,
        "age": age,
        "shoe_size": shoe_size,
        "body_type": fallback_body_type,
        "favorite_brands": brands,
        "style_description": style_description
    }


if __name__ == "__main__":
    test_input = "male, 178, 80, 26, 43, zara massimo-dutti, style: elegant with regular fit chinos"
    result = parse_user_input_flexible(test_input, fallback_body_type="athletic")

    print(f"Sex: {result['sex']}")
    print(f"Height: {result['height']} | Weight: {result['weight']}")
    print(f"Brands Extracted: {result['favorite_brands']}")
    print(f"Style: {result['style_description']}")
    print(f"Body Type (from frontend): {result['body_type']}")