"""Check the generated pages using only Python's standard library.

Run after news_i18n.py: python -m unittest discover -s tests -v
"""
from pathlib import Path
from html.parser import HTMLParser
import json
import re
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
BASE = 'https://www.aurora-studio.org'
SLUG = 'revenant-of-tsushima-demo-creator-outreach'
LANGS = {'en': 'en', 'zh-hant': 'zh-Hant', 'zh-hans': 'zh-Hans', 'ja': 'ja', 'ko': 'ko'}


class Document(HTMLParser):
    def __init__(self, route):
        super().__init__()
        self.text = (ROOT / route.strip('/') / 'index.html').read_text(encoding='utf-8')
        self.tags = []
        self.feed(self.text)
        self.graph = json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>', self.text)[1])['@graph']

    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, dict(attrs)))

    def find(self, tag, **attrs):
        return [a for t, a in self.tags if t == tag and all(a.get(k) == v for k, v in attrs.items())]


def route(code, article=False):
    return ('' if code == 'en' else '/' + code) + '/news/' + (SLUG + '/' if article else '')


class NewsPages(unittest.TestCase):
    def test_languages_canonicals_and_reciprocal_alternates(self):
        for code, lang in LANGS.items():
            for article in (False, True):
                with self.subTest(code=code, article=article):
                    doc = Document(route(code, article))
                    self.assertEqual(doc.find('html')[0]['lang'], lang)
                    self.assertEqual(doc.find('link', rel='canonical'), [{'rel': 'canonical', 'href': BASE + route(code, article)}])
                    expected = {language: BASE + route(other, article) for other, language in LANGS.items()}
                    expected['x-default'] = BASE + route('en', article)
                    self.assertEqual({a['hreflang']: a['href'] for a in doc.find('link', rel='alternate')}, expected)
                    language_nav = re.search(r'<details class="nav-group nav-language">.*?</details>', doc.text)[0]
                    for other in LANGS:
                        self.assertIn('href="' + route(other, article) + '"', language_nav)
                    self.assertEqual(len(doc.find('h1')), 1)
                    self.assertNotIn('noindex', doc.text)

    def test_archive_is_complete_and_english_destinations_are_labelled(self):
        english = Document(route('en'))
        originals = set(re.findall(r'href="(/news/[^/]+/)"', english.text))
        self.assertEqual(len(originals), 15)
        for code in LANGS:
            doc = Document(route(code))
            rows = re.findall(r'<article>.*?</article>', doc.text)
            self.assertEqual(len(rows), 15)
            items = next(x for x in doc.graph if x['@type'] == 'ItemList')
            self.assertEqual(items['numberOfItems'], 15)
            for row in rows:
                url = re.search(r'<a href="([^"]+)"', row)[1]
                if SLUG in url:
                    self.assertEqual(url, route(code, True))
                else:
                    self.assertIn(url, originals)
                    if code != 'en':
                        label = json.loads((ROOT / 'news/i18n.json').read_text(encoding='utf-8'))[code]['english']
                        self.assertIn(label, re.search(r'<a [^>]+>(.*?)</a>', row)[1])

    def test_article_schema_matches_visible_content_and_social_metadata(self):
        for code, lang in LANGS.items():
            doc = Document(route(code, True))
            item = next(x for x in doc.graph if x['@type'] == 'NewsArticle')
            self.assertEqual(item['inLanguage'], lang)
            self.assertEqual(item['datePublished'], '2026-10-22')
            self.assertEqual(item['url'], BASE + route(code, True))
            self.assertEqual(item['author']['name'], 'Aurora Studio')
            self.assertIn('datetime="2026-10-22"', doc.text)
            self.assertEqual(len(doc.find('h2')), 6)  # Facts and five substantive sections.
            self.assertIn('mailto:revenant-of-tsushima@aurora-studio.org', doc.text)
            for key in ('title', 'description', 'url', 'image', 'locale'):
                self.assertEqual(len(doc.find('meta', property='og:' + key)), 1)
            self.assertEqual(len(doc.find('meta', name='twitter:card')), 1)
            self.assertEqual(len(doc.find('meta', name='description')), 1)
            self.assertFalse(any(x['@type'] == 'FAQPage' for x in doc.graph))

    def test_local_destinations_and_sitemap(self):
        urls = [x.text for x in ET.parse(ROOT / 'sitemap.xml').iter('{http://www.sitemaps.org/schemas/sitemap/0.9}loc')]
        for code in LANGS:
            for article in (False, True):
                doc = Document(route(code, article))
                self.assertEqual(urls.count(BASE + route(code, article)), 1)
                for _, attrs in doc.tags:
                    for key in ('href', 'src'):
                        url = attrs.get(key, '')
                        if url.startswith('/'):
                            self.assertTrue((ROOT / url.split('?', 1)[0].lstrip('/')).exists(), url)
        for code in LANGS:
            if code != 'en':
                self.assertIn('href="' + route(code) + '"', (ROOT / code / 'index.html').read_text(encoding='utf-8'))


if __name__ == '__main__':
    unittest.main()
