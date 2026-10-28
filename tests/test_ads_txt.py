"""Regression checks for the public AdSense ads.txt file.

Run: python -m unittest discover -s tests -v
"""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
EXPECTED = "google.com, pub-1445900364467339, DIRECT, f08c47fec0942fa0"


class AdsTxtTests(unittest.TestCase):
    def test_lowercase_filename_and_no_case_variant(self):
        self.assertTrue((ROOT / "ads.txt").is_file())
        self.assertFalse((ROOT / "Ads.txt").exists())

    def test_authorized_seller_matches_page_adsense_account(self):
        ads = (ROOT / "ads.txt").read_text(encoding="utf-8")
        self.assertEqual(ads.splitlines(), [EXPECTED])
        self.assertTrue(ads.endswith(chr(10)), "ads.txt must end with a newline")
        homepage = (ROOT / "index.html").read_text(encoding="utf-8")
        publisher_ids = set(re.findall(r"ca-pub-([0-9]{16})", homepage))
        self.assertEqual(publisher_ids, {"1445900364467339"})


if __name__ == "__main__":
    unittest.main()
