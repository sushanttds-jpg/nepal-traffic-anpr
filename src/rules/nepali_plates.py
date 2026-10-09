"""
Nepali License Plate Syntax Rules and Format Validators.
Handles both traditional Devanagari plates and modern Embossed English plates.
"""

import re
from typing import Optional, Dict, Any

# Standard Nepali Vehicle Categories (सवारी साधन वर्ग)
NEPALI_VEHICLE_SYMBOLS = {
    "क": "Heavy Commercial (Truck, Bus)",
    "ख": "Public Transport (Micro, Minibus)",
    "ग": "Heavy Equipment / Tanker",
    "घ": "Government (General)",
    "ङ": "Corporation / Semi-Govt",
    "च": "Car / Jeep / Van (Private)",
    "छ": "Taxi / Rental",
    "ज": "Rental Vehicle",
    "झ": "Government Special",
    "ञ": "Diplomatic",
    "त": "Tractor",
    "थ": "Trailer",
    "प": "Motorcycle / Scooter (Two-Wheeler)",
    "फ": "Three-Wheeler (Tempo / Auto-rickshaw)",
    "ब": "Ambulance / Firetruck",
}

# 7 Provinces of Nepal (Devanagari and Latin)
PROVINCES_DEVANAGARI = [
    "कोशी", "मधेश", "बागमती", "गण्डकी", "लुम्बिनी", "कर्णाली", "सुदूरपश्चिम"
]

ZONES_DEVANAGARI = [
    "मेची", "कोशी", "सगरमाथा", "जनकपुर", "बागमती", "नारायणी", "गण्डकी",
    "लुम्बिनी", "धौलागिरी", "राप्ती", "कर्णाली", "भेरी", "सेती", "महाकाली",
    "मे", "को", "स", "ज", "बा", "ना", "ग", "लु", "धौ", "रा", "क", "भे", "से", "म"
]

# Devanagari to Arabic digits mapping
DEVANAGARI_TO_ARABIC = {
    '०': '0', '१': '1', '२': '2', '३': '3', '४': '4',
    '५': '5', '६': '6', '७': '7', '८': '8', '९': '9'
}

ARABIC_TO_DEVANAGARI = {v: k for k, v in DEVANAGARI_TO_ARABIC.items()}


def devanagari_to_arabic_digits(text: str) -> str:
    """Converts Devanagari numerals in text to standard Arabic numerals."""
    return "".join(DEVANAGARI_TO_ARABIC.get(ch, ch) for ch in text)


def arabic_to_devanagari_digits(text: str) -> str:
    """Converts Arabic numerals in text to Devanagari numerals."""
    return "".join(ARABIC_TO_DEVANAGARI.get(ch, ch) for ch in text)


def clean_plate_text(text: str) -> str:
    """Normalize whitespace and strip extraneous punctuation."""
    cleaned = re.sub(r'[\t\r\n]+', ' ', text)
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    return cleaned


def parse_nepali_plate(raw_text: str) -> Dict[str, Any]:
    """
    Parses and categorizes a recognized license plate string.
    Returns metadata including standard format, plate type, and validity.
    """
    cleaned = clean_plate_text(raw_text)
    
    # 1. Check for Modern Embossed Format (Latin)
    # Examples: "BAGMATI 01-028 CA 1234", "BA 02 PA 5678"
    embossed_pattern = r'^(?P<province>[A-Z\s]+)\s+(?P<lot>\d{1,2}(?:-\d{3})?)\s+(?P<cat>[A-Z]{1,2})\s+(?P<num>\d{4})$'
    match_embossed = re.match(embossed_pattern, cleaned)
    if match_embossed:
        return {
            "is_valid": True,
            "plate_type": "EMBOSSED_ENGLISH",
            "raw_text": cleaned,
            "province": match_embossed.group("province").strip(),
            "lot": match_embossed.group("lot"),
            "category": match_embossed.group("cat"),
            "number": match_embossed.group("num"),
            "normalized": f"{match_embossed.group('province').strip()} {match_embossed.group('lot')} {match_embossed.group('cat')} {match_embossed.group('num')}"
        }
        
    # 2. Check for Traditional Provincial Devanagari Format
    # Examples: "बागमती ०१-०२५ च ५६७८", "गण्डकी प्रदेश ०२ प १२३४"
    # Matches when province contains known province names or has provincial lot structure (xx-xxx)
    prov_names = "|".join(PROVINCES_DEVANAGARI)
    prov_pattern = rf'^(?P<province>(?:{prov_names})(?:\s+प्रदेश)?)\s+(?P<lot>[०-९\d]{{1,2}}(?:-[०-९\d]{{3}})?)\s+(?P<cat>[क-ह])\s+(?P<num>[०-९\d]{{1,4}})$'
    match_prov = re.match(prov_pattern, cleaned)
    if match_prov:
        cat_symbol = match_prov.group("cat")
        return {
            "is_valid": True,
            "plate_type": "DEVANAGARI_PROVINCIAL",
            "raw_text": cleaned,
            "province": match_prov.group("province"),
            "lot": match_prov.group("lot"),
            "category": cat_symbol,
            "category_meaning": NEPALI_VEHICLE_SYMBOLS.get(cat_symbol, "Unknown"),
            "number": match_prov.group("num"),
            "number_arabic": devanagari_to_arabic_digits(match_prov.group("num")),
            "normalized": f"{match_prov.group('province')} {match_prov.group('lot')} {cat_symbol} {match_prov.group('num')}"
        }

    # 3. Check for Traditional Zone Devanagari Format (Old)
    # Examples: "बा २ ख १२३४", "ना ५५ प ९९९९"
    zone_names = "|".join(ZONES_DEVANAGARI)
    zone_pattern = rf'^(?P<zone>{zone_names}|[क-ह]{{1,2}})\s+(?P<lot>[०-९\d]{{1,2}})\s+(?P<cat>[क-ह])\s+(?P<num>[०-९\d]{{1,4}})$'
    match_zone = re.match(zone_pattern, cleaned)
    if match_zone:
        cat_symbol = match_zone.group("cat")
        return {
            "is_valid": True,
            "plate_type": "DEVANAGARI_ZONE_OLD",
            "raw_text": cleaned,
            "zone": match_zone.group("zone"),
            "lot": match_zone.group("lot"),
            "category": cat_symbol,
            "category_meaning": NEPALI_VEHICLE_SYMBOLS.get(cat_symbol, "Unknown"),
            "number": match_zone.group("num"),
            "number_arabic": devanagari_to_arabic_digits(match_zone.group("num")),
            "normalized": f"{match_zone.group('zone')} {match_zone.group('lot')} {cat_symbol} {match_zone.group('num')}"
        }

    return {
        "is_valid": False,
        "plate_type": "UNKNOWN",
        "raw_text": cleaned,
        "normalized": cleaned
    }
