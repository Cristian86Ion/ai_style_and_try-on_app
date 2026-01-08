# models.py
"""
Data models și structuri pentru aplicație.
Definește formatul datelor folosite între componente.
"""

from dataclasses import dataclass
from typing import List, Optional, Dict


@dataclass
class UserData:
    """
    Date despre user din input și ProfileModal.
    """
    sex: str  # 'male' sau 'female'
    height: int  # cm
    weight: int  # kg
    age: int
    shoe_size: int  # EU
    body_type: str  # slim/athletic/average/muscular/stocky/plus-size (din ProfileModal)
    favorite_brands: List[str]  # Max 3 branduri
    style_description: str  # Max 30 cuvinte


@dataclass
class BodyMeasurements:
    """
    Măsurători calculate de body_measurements.py
    """
    height: int
    weight: int
    sex: str
    chest_circumference: float
    waist_circumference: float
    hip_circumference: float
    leg_length: float
    arm_length: float
    shoulder_hip_ratio: str
    chest_waist_ratio: str
    leg_length_ratio: str
    silhouette_gray: int
    bmi: float


@dataclass
class ColorPalette:
    """
    Paletă de culori Sanzo Wada
    """
    name: str  # Ex: "SET_01"
    colors: List[str]  # 3 culori cu hex: ["Deep Navy (#002366)", ...]
    season: str  # 'FW' sau 'SS'
    mood: str  # 'classic', 'bold', 'minimal', etc.


@dataclass
class OutfitResult:
    """
    Rezultatul complet al generării outfit-ului
    """
    outfit_description: str  # Descrierea outfit-ului de la GPT
    image_url: str  # URL imagine de la Flux
    styling_tips: str  # Tips de la GPT (≤45 cuvinte)
    outfit_palette: ColorPalette  # Paleta folosită pentru outfit
    tips_palette: ColorPalette  # Paleta alternativă sugerată în tips
    user_data: UserData
    measurements: BodyMeasurements
    season: str  # 'FW' sau 'SS'
    timestamp: str  # ISO format timestamp


@dataclass
class APIResponse:
    """
    Răspuns standardizat de la API
    """
    success: bool
    data: Optional[Dict] = None
    error: Optional[str] = None
    message: Optional[str] = None


# Constante pentru validare (matches ProfileModal.tsx)
VALID_SEXES = ['male', 'female', 'm', 'f', 'barbat', 'femeie']
VALID_BODY_TYPES = ['slim', 'athletic', 'average', 'muscular', 'stocky', 'plus-size']
VALID_SEASONS = ['FW', 'SS']

# Range-uri valide
HEIGHT_RANGE = (140, 220)  # cm
WEIGHT_RANGE = (40, 200)  # kg
AGE_RANGE = (10, 100)
SHOE_SIZE_RANGE = (35, 50)  # EU
MAX_BRANDS = 3
MAX_STYLE_WORDS = 30


def validate_user_data(data: dict) -> tuple[bool, str]:
    """
    Validează datele user-ului.

    Args:
        data: Dict cu date user

    Returns:
        (is_valid, error_message)
    """
    # Check required fields
    required = ['sex', 'height', 'weight', 'age', 'shoe_size', 'body_type']
    for field in required:
        if field not in data:
            return False, f"Missing required field: {field}"

    # Validate ranges
    if not HEIGHT_RANGE[0] <= data['height'] <= HEIGHT_RANGE[1]:
        return False, f"Height must be between {HEIGHT_RANGE[0]}-{HEIGHT_RANGE[1]}cm"

    if not WEIGHT_RANGE[0] <= data['weight'] <= WEIGHT_RANGE[1]:
        return False, f"Weight must be between {WEIGHT_RANGE[0]}-{WEIGHT_RANGE[1]}kg"

    if not AGE_RANGE[0] <= data['age'] <= AGE_RANGE[1]:
        return False, f"Age must be between {AGE_RANGE[0]}-{AGE_RANGE[1]}"

    if not SHOE_SIZE_RANGE[0] <= data['shoe_size'] <= SHOE_SIZE_RANGE[1]:
        return False, f"Shoe size must be between {SHOE_SIZE_RANGE[0]}-{SHOE_SIZE_RANGE[1]} EU"

    # Validate body_type (matches ProfileModal.tsx)
    if data['body_type'] not in VALID_BODY_TYPES:
        return False, f"Invalid body_type. Must be one of: {', '.join(VALID_BODY_TYPES)}"

    # Validate style description length
    if 'style_description' in data:
        word_count = len(data['style_description'].split())
        if word_count > MAX_STYLE_WORDS:
            return False, f"Style description too long ({word_count} words). Max {MAX_STYLE_WORDS} words."

    return True, ""


# Testing
if __name__ == "__main__":
    print("\n✅ Testing Data Models\n")

    # Test validation
    test_data = {
        'sex': 'male',
        'height': 180,
        'weight': 70,
        'age': 30,
        'shoe_size': 43,
        'body_type': 'athletic',
        'favorite_brands': ['nike', 'adidas'],
        'style_description': 'casual streetwear'
    }

    is_valid, error = validate_user_data(test_data)
    print(f"Validation: {'✅ PASS' if is_valid else '❌ FAIL'}")
    if not is_valid:
        print(f"Error: {error}")

    # Test invalid data
    invalid_data = test_data.copy()
    invalid_data['height'] = 300  # Too tall

    is_valid, error = validate_user_data(invalid_data)
    print(f"\nInvalid data test: {'✅ Caught error' if not is_valid else '❌ Should have failed'}")
    if not is_valid:
        print(f"Error message: {error}")