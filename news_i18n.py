"""Generate the five news indexes and October 22 article, using only the stdlib.

Run independently to preserve other checked-in pages, or after the site generators.
Older article bodies remain English; translated cards label those destinations.
"""
from pathlib import Path
from html import escape, unescape
import ast
import json
import re
from date_format import normalize_dates

ROOT = Path(__file__).parent
BASE = 'https://www.aurora-studio.org'
SLUG = 'revenant-of-tsushima-demo-creator-outreach'
LANGS = {'en': 'en', 'zh-hant': 'zh-Hant', 'zh-hans': 'zh-Hans', 'ja': 'ja', 'ko': 'ko'}
OG_LOCALES = {'en': 'en_US', 'zh-hant': 'zh_TW', 'zh-hans': 'zh_CN', 'ja': 'ja_JP', 'ko': 'ko_KR'}
LABELS = {'en': 'EN', 'zh-hant': '繁', 'zh-hans': '简', 'ja': '日', 'ko': '한'}
EMAIL = 'revenant-of-tsushima@aurora-studio.org'
DEMO = 'https://shikosama.itch.io/revenant-of-tsushima'


def route(code, article=False):
    return ('' if code == 'en' else '/' + code) + '/news/' + (SLUG + '/' if article else '')


def replace_inner(text, tag, value):
    return re.sub(fr'(<{tag}(?: [^>]*)?>).*?(</{tag}>)',
                  lambda m: m[1] + value + m[2], text, count=1, flags=re.S)


def plain(text):
    return unescape(re.sub('<[^>]+>', '', text))


def source_article():
    tree = ast.parse((ROOT / 'build.py').read_text(encoding='utf-8'))
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'news_updates' for t in node.targets):
            return next(item for item in ast.literal_eval(node.value) if item['slug'] == SLUG)
    raise ValueError('October 22 article source is missing')


def translated_listing(main, code, copy):
    # Translate structured cards by slug, never by their position in the archive.
    def card(match):
        row = match[0]
        slug = re.search(r'href="/news/([^/]+)/"', row)[1]
        if code != 'en':
            title, summary = (copy['article_title'], copy['article_summary']) if slug == SLUG else copy['stories'][slug]
            row = replace_inner(row, 'h2', escape(title))
            row = replace_inner(row, 'p', escape(summary))
            category = re.search(r'<span>(.*?)</span>', row)[1]
            row = replace_inner(row, 'span', escape(copy['ui'][unescape(category)]))
            label = copy['read'] + ('' if slug == SLUG else ' (' + copy['english'] + ')') + ' ↗'
            row = re.sub(r'(<a href="/news/[^/]+/">).*?(</a>)', lambda m: m[1] + escape(label) + m[2], row)
            if slug == SLUG:
                row = row.replace('/news/' + SLUG + '/', route(code, True))
        return row
    main = re.sub(r'<article>.*?</article>', card, main, flags=re.S)
    if code != 'en':
        # Match complete text nodes so category names cannot corrupt longer labels.
        for original, translation in copy['ui'].items():
            main = main.replace('>' + original + '<', '>' + escape(translation) + '<')
        main = main.replace('2025 / PROJECT NUMAZU', '2025 / Project Numazu')
        main = main.replace('alt="Aurora Publishing: Indie Games, Beyond Borders announcement artwork"',
                            'alt="' + escape(copy['ui']['Indie Games, Beyond Borders.']) + '"')
        if code != 'ko':
            main = main.replace('href="/media/"', 'href="/' + code + '/media/"')
    count = len(re.findall(r'<article>', main))
    main = re.sub(r'<span>(?:\d+ updates|共 \d+ 則消息|共 \d+ 则消息|全 \d+ 件|소식 \d+건)</span>',
                  '<span>' + copy['updates'].format(count=count) + '</span>', main)
    return main


def article_main(code, copy, source):
    title = source['title'] if code == 'en' else copy['article_title']
    summary = source['summary'] if code == 'en' else copy['article_summary']
    paragraphs = source['paragraphs'] if code == 'en' else copy['paragraphs']
    assert len(paragraphs) == len(copy['headings']) + 1
    body = '<p>' + escape(paragraphs[0]) + '</p>'
    for heading, paragraph in zip(copy['headings'], paragraphs[1:]):
        body += '<h2>' + escape(heading) + '</h2><p>' + escape(paragraph) + '</p>'
    facts = copy['facts']
    quick = ('<aside class="news-facts" aria-labelledby="demo-facts"><h2 id="demo-facts">' + escape(copy['facts_title']) + '</h2><dl>'
             + '<dt>' + escape(facts[0]) + '</dt><dd>' + escape(facts[1]) + '</dd>'
             + '<dt>' + escape(facts[2]) + '</dt><dd>' + escape(facts[3]) + '</dd>'
             + '<dt>' + escape(facts[4]) + '</dt><dd><a href="mailto:' + EMAIL + '">' + EMAIL + '</a></dd></dl></aside>')
    main = ('<main id="main"><section class="page-heading news-heading"><p class="eyebrow dark">'
            + escape(copy['category'].upper()) + ' · <time datetime="2026-10-22">2026-10-22</time> · Aurora Studio</p>'
            + '<h1 class="article-title">' + escape(title) + '</h1><p>' + escape(summary) + '</p></section>'
            + '<article class="section article news-article">' + quick
            + '<img class="article-visual" src="/assets/revenant-cover-v2.jpg" alt="' + escape(copy['art']) + '" loading="lazy">'
            + body + '<div class="article-links"><a href="' + DEMO + '">' + escape(copy['demo']) + ' ↗</a>'
            + '<a href="mailto:' + EMAIL + '">' + escape(copy['contact']) + ' ↗</a>'
            + '<a href="/project/revenant-of-tsushima/">' + escape(copy['project'])
            + ('' if code == 'en' else ' (' + escape(copy['english']) + ')') + ' ↗</a>'
            + '<a href="' + route(code) + '">← ' + escape(copy['back']) + '</a></div></article></main>')
    return main, title, summary


def metadata(shell, main, code, title, description, article, copy):
    canonical = BASE + route(code, article)
    lang = LANGS[code]
    shell = re.sub(r'<html lang="[^"]+">', '<html lang="' + lang + '">', shell, count=1)
    shell = replace_inner(shell, 'title', escape(title) + ' | Aurora Studio')
    shell = re.sub(r'<meta name="description"[^>]*>', '<meta name="description" content="' + escape(description, quote=True) + '">', shell)
    shell = re.sub(r'<link rel="(?:canonical|alternate)"[^>]*>', '', shell)
    shell = re.sub(r'<meta (?:property="(?:og:|article:)[^"]+"|name="twitter:[^"]+")[^>]*>', '', shell)
    shell = re.sub(r'<link rel="stylesheet" href="/news.css[^>]*>', '', shell)
    old_graph = re.search(r'<script type="application/ld\+json">(.*?)</script>', shell, re.S)
    graph = [x for x in json.loads(old_graph[1])['@graph'] if x.get('@type') in ('Organization', 'Brand', 'WebSite')]
    page = {'@type': 'WebPage' if article else 'CollectionPage', '@id': canonical + '#webpage',
            'url': canonical, 'name': title, 'description': description, 'inLanguage': lang,
            'isPartOf': {'@id': BASE + '/#website'}, 'breadcrumb': {'@id': canonical + '#breadcrumb'}}
    graph.append(page)
    breadcrumb = [{'@type': 'ListItem', 'position': 1, 'name': copy['home'], 'item': BASE + (('/' + code) if code != 'en' else '') + '/'},
                  {'@type': 'ListItem', 'position': 2, 'name': copy['news'], 'item': BASE + route(code)}]
    if article:
        breadcrumb.append({'@type': 'ListItem', 'position': 3, 'name': title, 'item': canonical})
        page['mainEntity'] = {'@id': canonical + '#article'}
        graph.append({'@type': 'NewsArticle', '@id': canonical + '#article', 'url': canonical,
                      'headline': title, 'description': description, 'inLanguage': lang,
                      'datePublished': '2026-10-22', 'dateModified': '2026-10-22',
                      'author': {'@type': 'Organization', 'name': 'Aurora Studio', 'url': BASE + '/'},
                      'publisher': {'@id': BASE + '/#organization'},
                      'image': BASE + '/assets/revenant-cover-v2.jpg',
                      'mainEntityOfPage': {'@id': canonical + '#webpage'},
                      'about': {'@type': 'VideoGame', 'name': 'Revenant of Tsushima', 'url': BASE + '/project/revenant-of-tsushima/'}})
    else:
        items = []
        for position, row in enumerate(re.findall(r'<article>.*?</article>', main, re.S), 1):
            url = re.search(r'<a href="([^"]+)"', row)[1]
            name = plain(re.search(r'<h2>(.*?)</h2>', row)[1])
            items.append({'@type': 'ListItem', 'position': position, 'name': name, 'url': BASE + url})
        page['mainEntity'] = {'@id': canonical + '#stories'}
        graph.append({'@type': 'ItemList', '@id': canonical + '#stories', 'numberOfItems': len(items), 'itemListElement': items})
    graph.append({'@type': 'BreadcrumbList', '@id': canonical + '#breadcrumb', 'itemListElement': breadcrumb})
    schema = json.dumps({'@context': 'https://schema.org', '@graph': graph}, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
    shell = re.sub(r'<script type="application/ld\+json">.*?</script>', lambda m: '<script type="application/ld+json">' + schema + '</script>', shell, count=1, flags=re.S)
    tags = '<link rel="canonical" href="' + canonical + '">'
    tags += ''.join('<link rel="alternate" hreflang="' + language + '" href="' + BASE + route(other, article) + '">' for other, language in LANGS.items())
    tags += '<link rel="alternate" hreflang="x-default" href="' + BASE + route('en', article) + '">'
    tags += '<link rel="stylesheet" href="/news.css?v=20261022">'
    properties = {'og:type': 'article' if article else 'website', 'og:site_name': 'Aurora Studio',
                  'og:title': title, 'og:description': description, 'og:url': canonical,
                  'og:locale': OG_LOCALES[code], 'og:image': BASE + '/assets/revenant-cover-v2.jpg', 'og:image:alt': copy['art']}
    if article:
        properties['article:published_time'] = '2026-10-22'
    tags += ''.join('<meta property="' + key + '" content="' + escape(value, quote=True) + '">' for key, value in properties.items())
    tags += ''.join('<meta property="og:locale:alternate" content="' + value + '">' for other, value in OG_LOCALES.items() if other != code)
    tags += '<meta name="twitter:card" content="summary_large_image">'
    for key in ('title', 'description', 'image', 'image:alt'):
        tags += '<meta name="twitter:' + key + '" content="' + escape(properties['og:' + key], quote=True) + '">'
    shell = shell.replace('</head>', tags + '</head>', 1)
    return re.sub(r'<main id="main">.*?</main>', lambda m: main, shell, count=1, flags=re.S)


def generate():
    copies = json.loads((ROOT / 'news/i18n.json').read_text(encoding='utf-8'))
    source = source_article()
    index_shell = (ROOT / 'news/index.html').read_text(encoding='utf-8')
    article_shell = (ROOT / 'news' / SLUG / 'index.html').read_text(encoding='utf-8')
    index_main = re.search(r'<main id="main">.*?</main>', index_shell, re.S)[0]
    index_main = re.sub(r'<section class="section rot-membership-news">.*?</section>', '', index_main, flags=re.S)
    index_main = re.sub(r'<article class="rot-membership-news">.*?</article>', '', index_main, flags=re.S)
    paths = []
    for code, copy in copies.items():
        listing = translated_listing(index_main, code, copy)
        article, title, summary = article_main(code, copy, source)
        for is_article, main, heading, description, shell in (
            (False, listing, copy['title'], copy['description'], index_shell),
            (True, article, title, summary, article_shell),
        ):
            path = ROOT / route(code, is_article).strip('/') / 'index.html'
            path.parent.mkdir(parents=True, exist_ok=True)
            text = normalize_dates(metadata(shell, main, code, heading, description, is_article, copy))
            paths.append((path, code, is_article))
            path.write_text(text, encoding='utf-8')

    # All language destinations exist before navigation checks for local routes.
    from navigation import header, LABELS as NAV_LABELS
    for path, code, is_article in paths:
        text = path.read_text(encoding='utf-8')
        language_links = ''.join('<a href="' + route(other, is_article) + '" lang="' + lang + '"'
                                 + (' aria-current="page"' if code == other else '') + '>' + LABELS[other] + '</a>' for other, lang in LANGS.items())
        old_header = '<div class="lang">' + language_links + '</div>'
        text = re.sub(r'<header class="site-header[^"]*">.*?</header>', lambda m: header(path, old_header), text, count=1, flags=re.S)
        if code != 'en':
            labels = NAV_LABELS[code]
            translations = dict(zip(['Projects', 'Services', 'ACG Partnerships', 'Publishing', 'Talents', 'News', 'Media', 'Contact', 'Careers'],
                                    [labels[1], labels[6], labels[7], labels[2], labels[11], labels[9], labels[10], labels[5], labels[12]]))
            footer = re.search(r'<footer>.*?</footer>', text, re.S)[0]
            for en, translated in translations.items():
                footer = footer.replace('>' + en + '<', '>' + escape(translated) + '<')
            other_labels = {
                'zh-hant': ['支持工作室', '工作原則'], 'zh-hans': ['支持工作室', '工作原则'],
                'ja': ['スタジオを支援', '運営方針'], 'ko': ['스튜디오 후원', '운영 원칙'],
            }
            for en, translated in zip(['Support', 'Governance'], other_labels[code]):
                footer = footer.replace('>' + en + '<', '>' + translated + '<')
            footer = footer.replace('href="/news/"', 'href="' + route(code) + '"')
            footnotes = {'zh-hant': '香港・獨立遊戲開發', 'zh-hans': '香港・独立游戏开发', 'ja': '香港のインディーゲーム開発', 'ko': '홍콩 인디 게임 개발'}
            footer = footer.replace('Independent game development · Hong Kong', footnotes[code])
            text = re.sub(r'<footer>.*?</footer>', lambda m: footer, text, count=1, flags=re.S)
            skips = {'zh-hant': '跳至主要內容', 'zh-hans': '跳至主要内容', 'ja': '本文へスキップ', 'ko': '본문으로 이동'}
            text = text.replace('>Skip to content<', '>' + skips[code] + '<')
        path.write_text(text, encoding='utf-8')

    # Existing localized homepages expose their local news archive.
    for code in LANGS:
        if code == 'en':
            continue
        path = ROOT / code / 'index.html'
        text = path.read_text(encoding='utf-8')
        text = text.replace('href="/news/"', 'href="' + route(code) + '"')
        path.write_text(text, encoding='utf-8')
    sitemap = ROOT / 'sitemap.xml'
    text = sitemap.read_text(encoding='utf-8')
    for path, code, is_article in paths:
        url = BASE + route(code, is_article)
        if '<loc>' + url + '</loc>' not in text:
            text = text.replace('</urlset>', '<url><loc>' + url + '</loc></url>\n</urlset>')
    sitemap.write_text(text, encoding='utf-8')
    from membership_news import generate as generate_membership_news
    generate_membership_news()


if __name__ == '__main__':
    generate()
