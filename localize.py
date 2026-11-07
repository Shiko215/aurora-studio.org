from rot_membership import section as membership_section
from pathlib import Path
from html import escape as e
root=Path(__file__).parent
translations={
'zh-hant':('zh-Hant','來自香港的獨立遊戲','我們以東亞的街道、文化與故事，創作模擬與敘事世界。','作品','在 OMSI 2 駕駛巴士，探索以真實比例重現的日本靜岡縣沼津市。','一場穿越江戶時代日本的第一人稱民俗恐怖旅程。','關於我們','Aurora Studio 是香港的獨立遊戲開發團隊，由 Shiko Leung 創立。我們結合文化細節與技術製作，與各地創作者合作。','最新消息','《Project Numazu》已在 Steam 推出；《Railway Depot》已有搶先開發版本。','聯絡我們','媒體及合作','玩家支援'),
'zh-hans':('zh-Hans','来自香港的独立游戏','我们以东亚的街道、文化与故事，创作模拟与叙事世界。','作品','在 OMSI 2 驾驶巴士，探索以真实比例重现的日本静冈县沼津市。','一场穿越江户时代日本的第一人称民俗恐怖旅程。','关于我们','Aurora Studio 是香港的独立游戏开发团队，由 Shiko Leung 创立。我们结合文化细节与技术制作，与各地创作者合作。','最新消息','《Project Numazu》已在 Steam 推出；《Railway Depot》已有抢先开发版本。','联系我们','媒体与合作','玩家支持'),
'ja':('ja','香港発のインディーゲーム','東アジアの街並み、文化、物語から着想を得て、シミュレーションと物語体験を制作しています。','作品','静岡県沼津市の街並みを実寸大で再現した、OMSI 2向けのバスシミュレーション追加コンテンツ。','江戸時代の日本を巡る一人称視点の民俗ホラー。','スタジオについて','Aurora Studioは香港を拠点とするインディーゲーム開発チームです。Shiko Leungが設立し、文化的な細部と技術的な表現を大切に、各地のクリエイターと制作しています。','最新情報','『Project Numazu』はSteamで発売中。『Railway Depot』のプレアルファ版も公開しています。','お問い合わせ','取材・事業提携','プレイヤーサポート'),
'ko':('ko','홍콩에서 만드는 인디 게임','동아시아의 거리와 문화, 이야기에서 영감을 받은 시뮬레이션과 서사 게임을 만듭니다.','프로젝트','일본 시즈오카현 누마즈시의 거리를 실제 크기로 재현한 OMSI 2 버스 시뮬레이션 콘텐츠입니다.','에도 시대 일본을 여행하는 1인칭 민속 공포 게임입니다.','스튜디오 소개','Aurora Studio는 홍콩의 독립 게임 개발팀입니다. Shiko Leung이 설립했으며, 문화적 디테일과 기술적 완성도를 바탕으로 여러 창작자와 협업합니다.','소식','Project Numazu는 Steam에서 출시되었으며 Railway Depot의 프리알파 버전도 공개되었습니다.','문의','언론 및 협업','플레이어 지원')}
langs='<div class="lang"><a href="/">EN</a><a href="/zh-hant/">繁</a><a href="/zh-hans/">简</a><a href="/ja/">日</a><a href="/ko/">한</a></div>'
extra={
'zh-hant':('合作服務','遊戲場景、模擬設計及原型製作。','支持曙光工房','透過會員計劃支持獨立開發，或洽談項目贊助與融資。','工作原則'),
'zh-hans':('合作服务','游戏场景、模拟设计及原型制作。','支持曙光工房','通过会员计划支持独立开发，或洽谈项目赞助与融资。','工作原则'),
'ja':('制作協力','ゲーム環境、シミュレーション設計、プロトタイプ制作。','スタジオを応援','メンバーシップによる支援、またはプロジェクト協賛・資金提供に関するご相談。','運営方針'),
'ko':('제작 협업','게임 환경, 시뮬레이션 설계 및 프로토타입 제작.','스튜디오 후원','멤버십으로 독립 개발을 지원하거나 프로젝트 후원 및 자금 협력을 문의하세요.','운영 원칙')}
media_titles={'zh-hant':'預告片・媒體報道・遊玩紀錄','zh-hans':'预告片・媒体报道・游玩视频','ja':'予告編・メディア掲載・実況動画','ko':'트레일러・언론 보도・플레이 영상'}
publishing_links={'zh-hant':'投稿遊戲','zh-hans':'提交游戏','ja':'ゲームのご提案','ko':'게임 제안하기'}
acg_links={'zh-hant':'ACG 跨境合作','zh-hans':'ACG 跨境合作','ja':'ACG事業提携'}

for code,(lang,title,lead,work,numazu,rot,about,abouttext,news,newstext,contact,press,support) in translations.items():
 media_href={'zh-hant':'/zh-hant/media/','zh-hans':'/zh-hans/media/','ja':'/ja/media/'}.get(code,'/media/')
 media_label=e(media_titles[code]) if code in ('zh-hant','zh-hans','ja') else 'Media'
 media_suffix='' if code in ('zh-hant','zh-hans','ja') else ' (EN)'
 nav=f'<a href="#work">{e(work)}</a><a href="/{code}/publishing/">{e({"zh-hant":"遊戲發行","zh-hans":"游戏发行","ja":"パブリッシング","ko":"퍼블리싱"}[code])}</a><a href="#about">{e(about)}</a><a href="#news">{e(news)}</a><a href="{media_href}">{media_label}</a><a href="/talents/">Talents (EN)</a><a href="#contact">{e(contact)}</a>'
 if code == 'zh-hans':
  nav=nav.replace(f'<a href="{media_href}">{media_label}</a>', '')
  nav=nav.replace('<a href="/zh-hans/publishing/">游戏发行</a>', '<a href="/zh-hans/publishing/">游戏发行</a><a href="/zh-hans/media/">媒体</a>')
 hero_cta=f'<a class="button light" href="#work">{e(work)} ↗</a>'
 if code == 'zh-hans':
  hero_cta='<div class="actions">'+hero_cta+'<a class="button light" href="/zh-hans/media/">媒体室 ↗</a></div>'
 footer_media_label = '媒体室' if code == 'zh-hans' else e(media_titles[code])+media_suffix
 service,servicecopy,back,backcopy,governance=extra[code]
 acg_link=f'<a href="/{code}/acg-partnerships/">{e(acg_links[code])} ↗</a>' if code in acg_links else '<a href="/acg-partnerships/">ACG Partnerships (EN) ↗</a>'
 extra_sections=f'<section class="section home-extras"><div class="info-panel"><h2>{e(service)}</h2><p>{e(servicecopy)}</p><a href="/services/">{e(service)} (EN) ↗</a>{acg_link}<a href="/{code}/publishing/">{e(publishing_links[code])} ↗</a></div><div class="info-panel"><h2>{e(back)}</h2><p>{e(backcopy)}</p><a href="/support/">{e(back)} (EN) ↗</a></div></section>'
 html=f'''<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{e(title)} | Aurora Studio</title><meta name="description" content="{e(lead)}"><link rel="canonical" href="https://www.aurora-studio.org/{code}/"><link rel="alternate" hreflang="en" href="https://www.aurora-studio.org/"><link rel="alternate" hreflang="zh-Hant" href="https://www.aurora-studio.org/zh-hant/"><link rel="alternate" hreflang="zh-Hans" href="https://www.aurora-studio.org/zh-hans/"><link rel="alternate" hreflang="ja" href="https://www.aurora-studio.org/ja/"><link rel="alternate" hreflang="ko" href="https://www.aurora-studio.org/ko/"><link rel="icon" href="/assets/aurora-studio-icon.png?v=20260925" type="image/png"><link rel="apple-touch-icon" href="/assets/aurora-studio-icon.png"><link rel="stylesheet" href="/style.css?v=20260926e"></head><body><a class="skip" href="#main">Skip to content</a><header class="site-header"><a class="brand" href="/" aria-label="Aurora Studio"><span class="brand-mark" aria-hidden="true"><img src="/assets/aurora-studio-logo.jpeg" alt="" width="1500" height="1000"></span><span class="brand-name">Aurora Studio</span></a><nav aria-label="Navigation">{nav}</nav>{langs}</header><main id="main"><section class="hero"><img class="hero-image" src="/assets/numazu-buses.jpg" alt="Project Numazu buses in game" fetchpriority="high"><div class="hero-shade"></div><div class="hero-content"><p class="eyebrow">AURORA STUDIO · HONG KONG</p><h1>{e(title)}.</h1><p>{e(lead)}</p>{hero_cta}</div></section><section class="section" id="work"><p class="eyebrow dark">PROJECTS</p><h2 class="local-head">{e(work)}</h2><div class="project-grid"><a class="feature-card" href="https://store.steampowered.com/app/3880120/"><img src="/assets/numazu-route.jpg" alt="Project Numazu" loading="lazy"><div><span>SIMULATION · RELEASED</span><h3>OMSI 2: Project Numazu</h3><p>{e(numazu)}</p><b>↗</b></div></a><a class="type-card" href="https://revenant-tsushima.aurora-studio.org/"><img class="rot-card-image" src="/assets/revenant-cover-clean.jpg" alt="Revenant of Tsushima poster" loading="lazy"><span>FOLK HORROR</span><h3>Revenant of Tsushima</h3><p>{e(rot)}</p><b>↗</b></a></div><article class="mini-list"><h2>Railway Depot: Operations &amp; Empire</h2><a href="https://shikosama.itch.io/railway-depot">itch.io ↗</a></article></section><section class="section two-column" id="about"><h2>{e(about)}</h2><p>{e(abouttext)}</p></section><section class="section two-column local-news" id="news"><h2>{e(news)}</h2><div><p>{e(newstext)}</p><a class="inline-media-link" href="{media_href}">{e(media_titles[code])}{media_suffix} ↗</a></div></section>{extra_sections}<section class="callout" id="contact"><p class="eyebrow">CONTACT</p><h2>{e(contact)}</h2><p>{e(press)}: <a href="mailto:press@aurora-studio.org">press@aurora-studio.org</a></p><p>{e(support)}: <a href="mailto:support@aurora-studio.org">support@aurora-studio.org</a></p></section></main><footer><strong>AURORA STUDIO</strong><div><a href="{media_href}">{footer_media_label}</a><a href="/services/">{e(service)} (EN)</a><a href="/support/">{e(back)} (EN)</a><a href="/governance/">{e(governance)} (EN)</a></div><small>© 2026 Aurora Studio</small></footer></body></html>'''
 html=html.replace('</main>', membership_section({'ja':'ja', 'zh-hant':'zh-Hant', 'zh-hans':'zh-Hans', 'ko':'ko'}[code])+'</main>')
 target=root/code/'index.html';target.parent.mkdir(exist_ok=True);target.write_text(html)
from careers_pages import generate as generate_careers_pages
generate_careers_pages()

from news_i18n import generate as generate_news_pages
generate_news_pages()
