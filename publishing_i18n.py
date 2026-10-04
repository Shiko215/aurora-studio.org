"""Generate translated Aurora Publishing pages from English page and JSON strings.

build.py invokes this after its other page generators. Do not edit generated
pages directly; change publishing/index.html or publishing/i18n.json.
"""
from pathlib import Path
import json
import re

ROOT=Path(__file__).parent
LANGS={
 "zh-hant":"zh-Hant", "zh-hans":"zh-Hans", "ja":"ja", "ko":"ko"
}
MENU=[("en","EN","/publishing/"),("zh-Hant","繁","/zh-hant/publishing/"),("zh-Hans","简","/zh-hans/publishing/"),("ja","日","/ja/publishing/"),("ko","한","/ko/publishing/")]

def generate():
 template=(ROOT/"publishing"/"index.html").read_text(encoding="utf-8")
 translations=json.loads((ROOT/"publishing"/"i18n.json").read_text(encoding="utf-8"))
 keys=translations["keys"]
 for code,lang in LANGS.items():
  locale=translations["locales"][code]
  values=locale["texts"]
  if len(keys)!=len(values):
   raise ValueError(f"Missing translations for {code}: {len(keys)} keys and {len(values)} values")
  html=template.replace('<html lang="en">',f'<html lang="{lang}">')
  html=html.replace('<link rel="canonical" href="https://www.aurora-studio.org/publishing/">',f'<link rel="canonical" href="https://www.aurora-studio.org/{code}/publishing/">')
  html=html.replace('<meta property="og:url" content="https://www.aurora-studio.org/publishing/">',f'<meta property="og:url" content="https://www.aurora-studio.org/{code}/publishing/">')
  for original,translated in sorted(zip(keys,values),key=lambda x:-len(x[0])):
   if original not in html:
    raise ValueError(f"Missing template source text {code}: {original}")
   html=html.replace(original,translated)
  menu='<div class="lang" aria-label="Page language">'+''.join(f'<a href="{href}" lang="{language}"'+(' aria-current="page"' if lang==language else '')+f'>{label}</a>' for language,label,href in MENU)+'</div>'
  html=re.sub(r'<div class="lang" aria-label="Page language">.*?</div>',lambda _:menu,html,count=1,flags=re.S)
  acg=f"/{code}/acg-partnerships/" if code!="ko" else "/acg-partnerships/"
  nav_urls=[f"/{code}/","/project/","/services/",acg,f"/{code}/publishing/","/media/","/about/","/contact/"]
  nav_items=list(zip(nav_urls,locale["nav"]))
  nav_items.insert(1,nav_items.pop(4))
  nav='<nav aria-label="Main navigation">'+''.join(f'<a href="{href}"'+(' aria-current="page"' if i==1 else '')+f'>{label}</a>' for i,(href,label) in enumerate(nav_items))+'</nav>'
  html=re.sub(r'<nav aria-label="Main navigation">.*?</nav>',lambda _:nav,html,count=1,flags=re.S)
  foot_urls=["/project/","/services/",acg,f"/{code}/publishing/","/media/","/governance/","/contact/"]
  foot='<footer><div><strong>AURORA STUDIO</strong><p>'+values[keys.index("Independent game development · Hong Kong")]+ '</p></div><div>'+''.join(f'<a href="{href}">{label}</a>' for href,label in zip(foot_urls,locale["foot"]))+'</div><small>© 2026 Aurora Studio</small></footer>'
  html=re.sub(r'<footer>.*?</footer>',lambda _:foot,html,count=1,flags=re.S)
  output=ROOT/code/"publishing"/"index.html"
  output.parent.mkdir(parents=True,exist_ok=True)
  output.write_text(html,encoding="utf-8")

if __name__=="__main__": generate()
