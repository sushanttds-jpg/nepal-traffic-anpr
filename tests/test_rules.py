import unittest
from src.rules.nepali_plates import (
    parse_nepali_plate,
    devanagari_to_arabic_digits,
    arabic_to_devanagari_digits,
)

class TestNepaliPlateRules(unittest.TestCase):
    def test_devanagari_to_arabic_conversion(self):
        self.assertEqual(devanagari_to_arabic_digits("१२३४"), "1234")
        self.assertEqual(devanagari_to_arabic_digits("०९८७६५४३२१"), "0987654321")

    def test_arabic_to_devanagari_conversion(self):
        self.assertEqual(arabic_to_devanagari_digits("1234"), "१२३४")

    def test_parse_old_zone_devanagari(self):
        res = parse_nepali_plate("बा २ ख १२३४")
        self.assertTrue(res["is_valid"])
        self.assertEqual(res["plate_type"], "DEVANAGARI_ZONE_OLD")
        self.assertEqual(res["zone"], "बा")
        self.assertEqual(res["category"], "ख")
        self.assertEqual(res["number_arabic"], "1234")

    def test_parse_provincial_devanagari(self):
        res = parse_nepali_plate("बागमती ०१-०२५ च ५६७८")
        self.assertTrue(res["is_valid"])
        self.assertEqual(res["plate_type"], "DEVANAGARI_PROVINCIAL")
        self.assertEqual(res["province"], "बागमती")
        self.assertEqual(res["category"], "च")
        self.assertEqual(res["number_arabic"], "5678")

    def test_parse_embossed_plate(self):
        res = parse_nepali_plate("BAGMATI 01-028 CA 1234")
        self.assertTrue(res["is_valid"])
        self.assertEqual(res["plate_type"], "EMBOSSED_ENGLISH")
        self.assertEqual(res["province"], "BAGMATI")
        self.assertEqual(res["category"], "CA")
        self.assertEqual(res["number"], "1234")

    def test_parse_invalid_plate(self):
        res = parse_nepali_plate("RANDOM TEXT 999")
        self.assertFalse(res["is_valid"])
        self.assertEqual(res["plate_type"], "UNKNOWN")

if __name__ == "__main__":
    unittest.main()
