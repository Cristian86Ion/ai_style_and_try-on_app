def compute_body_measurements(height: int, weight: int, sex: str) -> dict:
    """
    User input:
        height: Înălțime în cm (ex: 180)
        weight: Greutate în kg (ex: 70)
        sex: 'male' sau 'female'

    Return:
        - chest_circumference (cm)
        - waist_circumference (cm)
        - hip_circumference (cm)
        - leg_length (cm)
        - arm_length (cm)
        - shoulder_hip_ratio
        - chest_waist_ratio
        - leg_length_ratio
        - silhouette_gray (pentru mannequin)
    """

    # BMI
    bmi = weight / ((height / 100) ** 2)
    if sex == 'male':
        chest = 50 + (height - 170) * 0.3 + (weight - 70) * 0.4 + (bmi - 22) * 2.0
    else:
        chest = 45 + (height - 160) * 0.3 + (weight - 60) * 0.4 + (bmi - 22) * 1.6

    if sex == 'male':
        waist = 42 + (height - 170) * 0.2 + (weight - 70) * 0.5 + (bmi - 22) * 2.8
    else:
        waist = 70 + (height - 160) * 0.4 + (weight - 60) * 0.8 + (bmi - 22) * 3.2

    if sex == 'male':
        hips = 48 + (height - 170) * 0.25 + (weight - 70) * 0.45 + (bmi - 22) * 1.6
    else:
        hips = 50 + (height - 160) * 0.25 + (weight - 60) * 0.45 + (bmi - 22) * 2.4

    # Leg length
    leg_length = height * 0.52

    # Arm length
    arm_length = height * 0.38

    # Compute ratios
    shoulder_width = chest * 0.95
    shoulder_hip_ratio = round(shoulder_width / hips, 2)
    chest_waist_ratio = round(chest / waist, 2)
    leg_length_ratio = round(leg_length / height, 2)

    silhouette_gray = min(180, max(100, int(100 + (bmi - 22) * 10)))

    return {
        "height": height,
        "weight": weight,
        "sex": sex,
        "chest_circumference": round(chest, 1),
        "waist_circumference": round(waist, 1),
        "hip_circumference": round(hips, 1),
        "leg_length": round(leg_length, 1),
        "arm_length": round(arm_length, 1),
        "shoulder_hip_ratio": f"{shoulder_hip_ratio:.2f}",
        "chest_waist_ratio": f"{chest_waist_ratio:.2f}",
        "leg_length_ratio": f"{leg_length_ratio:.2f}",
        "silhouette_gray": silhouette_gray,
        "bmi": round(bmi, 1)
    }


# Testing
if __name__ == "__main__":

    test_cases = [
        {"height": 173, "weight": 70, "sex": "male"},
        {"height": 165, "weight": 55, "sex": "female"},
        {"height": 180, "weight": 85, "sex": "male"},
    ]

    for i, test in enumerate(test_cases, 1):
        print(f"Test {i}: {test['sex']}, {test['height']}cm, {test['weight']}kg")
        measurements = compute_body_measurements(**test)

        print(f"  Chest: {measurements['chest_circumference']}cm")
        print(f"  Waist: {measurements['waist_circumference']}cm")
        print(f"  Hips: {measurements['hip_circumference']}cm")
        print(f"  Shoulder-to-Hip: {measurements['shoulder_hip_ratio']}")
        print(f"  BMI: {measurements['bmi']}")
        print()