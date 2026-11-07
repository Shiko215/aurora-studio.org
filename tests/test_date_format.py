import unittest
from date_format import normalize_dates


class DateFormatTests(unittest.TestCase):
    def test_calendar_dates_use_datetime_value_in_every_language(self):
        for label in ('07 NOV 2026', '2026年11月7日', '2026년 11월 7일', '2026.11.07'):
            self.assertEqual(
                normalize_dates(f'<time datetime="2026-11-07">{label}</time>'),
                '<time datetime="2026-11-07">2026-11-07</time>',
            )

    def test_abbreviated_visible_labels_preserve_month_only_precision(self):
        self.assertEqual(normalize_dates('<span>TAIWAN · 04 SEP 2026</span>'),
                         '<span>TAIWAN · 2026-09-04</span>')
        self.assertEqual(normalize_dates('<span>TOKYO · SEP 2025</span>'),
                         '<span>TOKYO · 2025-09</span>')

    def test_urls_and_date_values_are_preserved_and_result_is_repeatable(self):
        html = '<a href="/news/NOV 2026/"><time datetime="2026-11-07">07 NOV 2026</time></a>'
        formatted = normalize_dates(html)
        self.assertIn('href="/news/NOV 2026/"', formatted)
        self.assertIn('datetime="2026-11-07"', formatted)
        self.assertEqual(normalize_dates(formatted), formatted)


if __name__ == '__main__':
    unittest.main()
