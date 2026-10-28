"""Guard against accidentally blocking Aurora Studio's public website.

Run with: python -m unittest discover -s tests -v
This validates checked-in files; it does not test the live server's HTTP response.
"""

from pathlib import Path
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
SITE = "https://www.aurora-studio.org"
SITEMAP = SITE + "/sitemap.xml"


class RobotsTxtTests(unittest.TestCase):
    def test_public_crawling_policy_and_sitemap(self):
        robots = (ROOT / "robots.txt").read_text(encoding="utf-8")
        directives = [
            line.strip()
            for line in robots.splitlines()
            if line.strip() and not line.lstrip().startswith("#")
        ]
        self.assertEqual(
            directives,
            ["User-agent: *", "Allow: /", "Sitemap: " + SITEMAP],
        )

    def test_sitemap_is_valid_and_uses_canonical_host(self):
        self.assertEqual((ROOT / "CNAME").read_text(encoding="utf-8").strip(),
                         "www.aurora-studio.org")
        tree = ET.parse(ROOT / "sitemap.xml")
        namespace = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
        urls = [loc.text for loc in tree.iter(namespace + "loc")]
        self.assertTrue(urls, "Sitemap must not be empty")
        self.assertIn(SITE + "/", urls, "Sitemap must include the homepage")
        self.assertTrue(
            all(url and url.startswith(SITE + "/") for url in urls),
            "All sitemap URLs must use the canonical website host",
        )
        self.assertEqual(len(urls), len(set(urls)), "Sitemap URLs must be unique")


if __name__ == "__main__":
    unittest.main()
