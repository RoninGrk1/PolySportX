LOW = "LOW"
MEDIUM = "MEDIUM"
HIGH = "HIGH"
VERY_HIGH = "VERY_HIGH"


def label_for(score: int) -> str:
    if score >= 90:
        return VERY_HIGH
    if score >= 70:
        return HIGH
    if score >= 40:
        return MEDIUM
    return LOW
