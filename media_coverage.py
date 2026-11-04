"""Latest RoT coverage shared by the four media-room editions."""
import json
import re
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent
START = "<!-- latest-rot-coverage:start -->"
END = "<!-- latest-rot-coverage:end -->"
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
        cards = ""
        for i, (source, date, title, description, url) in enumerate(rows):
            cards += f'<a class="press-item" href="{url}" target="_blank" rel="noopener noreferrer"><div class="press-line"><span class="press-source">{escape(source)}</span><span class="press-meta">{escape(c["labels"][i])} · <time datetime="{date}">{date.replace("-", ".")}</time></span></div><h3>{escape(title)}</h3><p>{escape(description)}</p><b>{escape(c["read"][i])} ↗</b></a>'
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

