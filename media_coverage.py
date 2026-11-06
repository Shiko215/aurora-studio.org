"""Latest RoT coverage shared by the four media-room editions."""
import json
import re
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent
START = "<!-- latest-rot-coverage:start -->"
END = "<!-- latest-rot-coverage:end -->"

# Verified additional regional coverage (2026-11-02). Keep editorial origin distinct.
ADDITIONAL_COVERAGE = {
    "en": [
        ("3DMGAME · China", "3DM translated/adapted report", "3DM translated the Steam store-page announcement, crediting Bahamut as the source.", "3DM EDITORIAL TRANSLATION", "Read at 3DMGAME"),
        ("3DM International · English", "English edition of the 3DM report", "English-language version of 3DM's coverage; not a separate independent interview.", "TRANSLATED EDITION", "Read the English report"),
        ("游数社 · China", "Steam page and new trailer coverage", "An editorial article covering the Steam page, gameplay loop and current development status.", "EDITORIAL REPORT", "Read at 游数社"),
    ],
    "zh-hant": [
        ("3DMGAME · 中國大陸", "3DM 編譯 Steam 頁上線消息", "文章標示來源為巴哈姆特，由 3DM 編譯，並非獨立採訪。", "編譯報導", "閱讀 3DM 中文版"),
        ("3DM International · 英文", "3DM 報導的英文版本", "同一報導的英文版本，不另計為獨立原創採訪。", "英文翻譯版", "閱讀 3DM 英文版"),
        ("游數社 · 中國大陸", "Steam 頁公開及新預告報導", "文章介紹 Steam 商店頁、玩法循環及作品現階段開發狀態。", "編輯報導", "閱讀游數社"),
    ],
    "zh-hans": [
        ("3DMGAME · 中国大陆", "3DM 编译 Steam 页面上线消息", "文章注明来源为巴哈姆特，由 3DM 编译，不属于独立采访。", "编译报道", "阅读 3DM 中文版"),
        ("3DM International · 英文", "3DM 报道的英文版本", "同篇报道的英文版本，不单独计算为原创采访。", "英文翻译版", "阅读 3DM 英文版"),
        ("游数社 · 中国大陆", "Steam 页面与新预告报道", "文章介绍 Steam 商店页面、核心玩法及当前开发状态。", "编辑报道", "阅读游数社"),
    ],
    "ja": [
        ("3DMGAME · 中国", "3DMによるSteam公開ニュースの翻訳・編集記事", "巴哈姆特を出典と明記した翻訳・編集記事です。独自取材とは区別しています。", "翻訳・編集記事", "3DM中国語版を読む"),
        ("3DM International · 英語", "3DM記事の英語版", "3DMの記事を英語で紹介したもので、別の独自取材としては数えません。", "英語版", "3DM英語版を読む"),
        ("游数社 · 中国", "Steamページと新トレーラーの紹介", "Steam公開、ゲームシステム、開発状況を取り上げた記事です。", "編集記事", "游数社の記事を読む"),
    ],
}
ADDITIONAL_URLS = (
    "https://www.3dmgame.com/news/202611/3958659.html",
    "https://en.3dmgame.com/news/8965",
    "https://monv.net/news/4807",
)

def generate():
    data = json.loads((ROOT / "media/coverage.json").read_text(encoding="utf-8"))
    for locale, c in data.items():
        path = ROOT / ("" if locale == "en" else locale) / "media/index.html"
        if not path.exists():
            continue
        html = path.read_text(encoding="utf-8")
        rows = [
            ("Bahamut GNN · Taiwan", "2026-11-02", c["gnn"], c["gdesc"], "https://gnn.gamer.com.tw/detail.php?sn=314345"),
            ("PChome Online News · Taiwan", "2026-11-02", c["p"], c["pd"], "https://news.pchome.com.tw/game/gamer/20261102/index-79361195876455203104.html"),
            ("3Days Steam · Japan", "2026-11-01", c["list"], c["ld"], "https://3days-steam.blog/"),
        ]
        rows.extend((source, "2026-11-02", title, description, ADDITIONAL_URLS[i])
                    for i, (source, title, description, label, read) in enumerate(ADDITIONAL_COVERAGE[locale]))
        cards = ""
        for i, (source, date, title, description, url) in enumerate(rows):
            cards += f'<a class="press-item" href="{url}" target="_blank" rel="noopener noreferrer"><div class="press-line"><span class="press-source">{escape(source)}</span><span class="press-meta">{escape(c["labels"][i] if i < 3 else ADDITIONAL_COVERAGE[locale][i - 3][3])} · <time datetime="{date}">{date.replace("-", ".")}</time></span></div><h3>{escape(title)}</h3><p>{escape(description)}</p><b>{escape(c["read"][i] if i < 3 else ADDITIONAL_COVERAGE[locale][i - 3][4])} ↗</b></a>'
        section = START + f'''
<section class="section media-section" id="latest-coverage" aria-labelledby="latest-coverage-title">
<div class="media-section-head"><div><p class="eyebrow dark">REVENANT OF TSUSHIMA · NOV 2026</p><h2 id="latest-coverage-title">{escape(c["title"])}</h2></div><div><p>{escape(c["intro"])}</p></div></div>
<div class="press-list">{cards}</div>
<p class="actions"><a class="inline-media-link" href="https://store.steampowered.com/app/5529920/Revenant_of_Tsushima/?utm_source=aurora_studio&amp;utm_medium=website&amp;utm_campaign=rot_steam_launch&amp;utm_content=media_{locale}" target="_blank" rel="noopener noreferrer">{escape(c["steam"])} ↗</a><a class="inline-media-link" href="https://revenant-tsushima.aurora-studio.org/press-kit/" target="_blank" rel="noopener noreferrer">{escape(c["kit"])} ↗</a></p>
</section>
''' + END
        if START in html:
            html = re.sub(re.escape(START) + r".*?" + re.escape(END), lambda _: section, html, flags=re.S)
        else:
            marker = '<section class="media-showcase"'
            if marker not in html:
                raise ValueError(f"Missing media showcase in {path}")
            html = html.replace(marker, section + "\n" + marker, 1)
        if 'href="#latest-coverage"' not in html:
            html = html.replace('<a href="#highlights">', f'<a href="#latest-coverage">{escape(c["nav"])}</a><a href="#highlights">', 1)
        path.write_text(html, encoding="utf-8")

if __name__ == "__main__":
    generate()

