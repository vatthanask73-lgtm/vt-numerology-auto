from __future__ import annotations

import re
from datetime import date, datetime
from typing import Any

MASTER_NUMBERS = frozenset({11, 22, 33})

LETTER_VALUES = {
    "A": 1, "B": 2, "C": 3, "D": 4, "E": 5, "F": 6,
    "G": 7, "H": 8, "I": 9, "J": 1, "K": 2, "L": 3,
    "M": 4, "N": 5, "O": 6, "P": 7, "Q": 8, "R": 9,
    "S": 1, "T": 2, "U": 3, "V": 4, "W": 5, "X": 6,
    "Y": 7, "Z": 8,
}
VOYEL_LETTERS = set("AEIOUY")


def reduce_number(value: int, *, keep_master_numbers: bool = False) -> int:
    """Reduce a number to a single digit by default, preserving 11/22/33 when requested."""
    if value < 0:
        value = abs(value)

    while value > 9 and (not keep_master_numbers or value not in MASTER_NUMBERS):
        value = sum(int(digit) for digit in str(value))

    return value


def _normalize_date(value: Any) -> date:
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    if isinstance(value, str):
        text = value.strip()
        if not text:
            raise ValueError("Date string cannot be blank")
        patterns = [
            "%Y-%m-%d",
            "%m/%d/%Y",
            "%m-%d-%Y",
            "%Y/%m/%d",
            "%d/%m/%Y",
            "%d-%m-%Y",
        ]
        for pattern in patterns:
            try:
                return datetime.strptime(text, pattern).date()
            except ValueError:
                continue
        cleaned = re.sub(r"[^0-9]", "", text)
        if len(cleaned) != 8:
            raise ValueError(f"Unsupported date value: {value!r}")
        return datetime.strptime(cleaned, "%Y%m%d").date()

    raise TypeError(f"Unsupported date value type: {type(value).__name__}")


def _digit_total(value: Any) -> int:
    digits = re.sub(r"[^0-9]", "", str(value))
    if not digits:
        return 0
    return sum(int(digit) for digit in digits)


def calculate_life_path(date_value: Any) -> int:
    """Return the life path number from a birth date."""
    birth_date = _normalize_date(date_value)
    raw_total = _digit_total(f"{birth_date.year}{birth_date.month:02d}{birth_date.day:02d}")
    return reduce_number(raw_total, keep_master_numbers=False)


def _letters_to_digits(name: str, *, selector: str | None = None, keep_master_numbers: bool = False) -> int:
    cleaned = re.sub(r"[^A-Za-z]", "", name.upper())
    if not cleaned:
        raise ValueError("Name does not contain letters")

    if selector == "vowels":
        cleaned = "".join(ch for ch in cleaned if ch in VOYEL_LETTERS)
    elif selector == "consonants":
        cleaned = "".join(ch for ch in cleaned if ch not in VOYEL_LETTERS)

    if not cleaned:
        raise ValueError("Selector produced no letters")

    total = sum(LETTER_VALUES.get(ch, 0) for ch in cleaned)
    return reduce_number(total, keep_master_numbers=keep_master_numbers)


def calculate_expression_number(name: str, *, keep_master_numbers: bool = False) -> int:
    """Reduce the sum of a full name into a numerology value."""
    total = 0
    for character in re.sub(r"[^A-Za-z]", "", name.upper()):
        total += LETTER_VALUES.get(character, 0)
    return reduce_number(total, keep_master_numbers=keep_master_numbers)


def calculate_name_number(name: str, *, keep_master_numbers: bool = False) -> int:
    return calculate_expression_number(name, keep_master_numbers=keep_master_numbers)


def calculate_soul_number(name: str, *, keep_master_numbers: bool = False) -> int:
    return _letters_to_digits(name, selector="vowels", keep_master_numbers=keep_master_numbers)


def calculate_personality_number(name: str, *, keep_master_numbers: bool = False) -> int:
    return _letters_to_digits(name, selector="consonants", keep_master_numbers=keep_master_numbers)


def calculate_compatibility(left: Any, right: Any) -> float:
    """Return a compatibility percentage between two life paths."""
    left_path = calculate_life_path(left)
    right_path = calculate_life_path(right)
    delta = abs(left_path - right_path)
    score = 100 - min(delta * 10, 90)
    return max(0.0, float(score))


def calculate_report(name: str, birth_date: Any) -> dict[str, Any]:
    return {
        "life_path": calculate_life_path(birth_date),
        "expression_number": calculate_expression_number(name),
        "soul_number": calculate_soul_number(name),
        "personality_number": calculate_personality_number(name),
    }
