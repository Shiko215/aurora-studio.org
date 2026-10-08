"""Apply a shared, grouped header to every generated language page."""
from pathlib import Path
from html import escape
import re
ROOT = Path(__file__).parent
LABELS = {
 'en': ['Home','Projects','Publishing','Business','Studio','Contact','Services','ACG Partnerships','About','News','Media','Talents','Careers & Talent Network','Language'],
 'zh-hant': ['首頁','作品','遊戲發行','業務合作','工作室','聯絡','服務','ACG 合作','關於我們','最新消息','媒體室','藝人','職涯與人才網絡','語言'],
 'zh-hans': ['首页','作品','游戏发行','业务合作','工作室','联系','服务','ACG 合作','关于我们','最新消息','媒体室','艺人','职业与人才网络','语言'],
 'ja': ['ホーム','作品','パブリッシング','事業','スタジオ','お問い合わせ','サービス','ACG パートナーシップ','私たちについて','ニュース','メディア','タレント','採用・人材ネットワーク','言語'],
 'ko': ['홈','프로젝트','퍼블리싱','비즈니스','스튜디오','문의','서비스','ACG 파트너십','소개','뉴스','미디어','탤런트','채용 및 인재 네트워크','언어'],
}

def header(path, old):
 rel=path.relative_to(ROOT).as_posix()
 code=rel.split('/')[0] if rel.split('/')[0] in LABELS else 'en'
 labels=LABELS[code]
 prefix='' if code=='en' else '/'+code
 route='/'+rel.removesuffix('index.html')
 def target(s, localized=False):
  candidate=(prefix+s if localized else s)
  return candidate if (ROOT/candidate.strip('/')/'index.html').exists() else s
 def link(url, label):
  current=' aria-current="page"' if route==url else ''
  return f'<a href="{url}"{current}>{escape(label)}</a>'
 def group(title, items):
  active=' class="nav-group nav-active"' if any(route==u for u,_ in items) else ' class="nav-group"'
  return f'<details{active}><summary>{escape(title)}</summary><div class="nav-panel">'+''.join(link(u,t) for u,t in items)+'</div></details>'
 nav=link(prefix+'/',labels[0])+link('/project/',labels[1])+link(target('/publishing/',True),labels[2])
 nav+=group(labels[3],[( '/services/',labels[6]),(target('/acg-partnerships/',True),labels[7])])
 nav+=group(labels[4],[( '/about/',labels[8]),('/news/',labels[9]),(target('/media/',True),labels[10]),('/talents/',labels[11]),(target('/careers/',True),labels[12])])
 nav+=link('/contact/',labels[5])
 brand='<a href="'+prefix+'/" class="brand" aria-label="Aurora Studio"><span class="brand-mark" aria-hidden="true"><img src="/assets/aurora-studio-logo.jpeg" alt="" width="1500" height="1000"></span><span class="brand-name">Aurora Studio</span></a>'
 lang=re.search(r'<div class="lang"[^>]*>(.*?)</div>',old,re.S)
 if not lang: lang=re.search(r'<details class="nav-group nav-language">.*?<div class="nav-panel">(.*?)</div>',old,re.S)
 languages=lang.group(1) if lang else '<a href="/" lang="en">EN</a><a href="/zh-hant/" lang="zh-Hant">繁</a>'
 current={'en':'EN','zh-hant':'繁','zh-hans':'简','ja':'日','ko':'한'}[code]
 language=f'<details class="nav-group nav-language"><summary aria-label="{labels[13]}">{current}</summary><div class="nav-panel">{languages}</div></details>'
 return f'<header class="site-header organized-header">{brand}<nav aria-label="Main navigation">{nav}</nav>{language}</header>'

def generate():
 for path in ROOT.rglob('*.html'):
  text=path.read_text()
  match=re.search(r'<header class="site-header[^\"]*">.*?</header>',text,re.S)
  if not match: continue
  text=text[:match.start()]+header(path,match.group())+text[match.end():]
  if '/navigation.css' not in text:
   text=text.replace('</head>','<link rel="stylesheet" href="/navigation.css?v=20261008"><script src="/navigation.js?v=20261008" defer></script></head>',1)
  path.write_text(text)

if __name__=='__main__':generate()
