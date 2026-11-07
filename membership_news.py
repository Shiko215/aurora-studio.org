"""Generate the Steam-page / optional development-support announcement."""
from pathlib import Path
from html import escape
import json
import re
from rot_membership import section

ROOT = Path(__file__).parent
BASE = 'https://www.aurora-studio.org'
SLUG = 'revenant-of-tsushima-steam-page-development-support'
STEAM = 'https://store.steampowered.com/app/5529920/Revenant_of_Tsushima/'
COPY = {
 'en': ('en', 'Revenant of Tsushima is on Steam — help us build the next chapter',
  'Wishlist the game on Steam, or support ongoing development through Patreon or pixivFANBOX.',
  'Our Steam store page is live. Thank you to everyone discovering Revenant of Tsushima, our first-person Japanese folk horror project. Add the game to your wishlist and follow it on Steam to keep up with development.',
  'A Steam page is a milestone in sharing the project with players; development continues. We are inviting optional membership support through Patreon and pixivFANBOX to help fund continued work on the game. Explore the current plans on either platform and choose the one that suits you.',
  'You can also help by sharing the Steam page and telling us what interests you about the game. Thank you for walking this road with Aurora Studio.',
  'Wishlist on Steam', 'All news', 'Read the announcement'),
 'ja': ('ja', '『津島・魂鬼』Steamストアページ公開 — 次の一歩を応援してください',
  'Steamでウィッシュリスト登録。Patreon・pixivFANBOXで継続開発へのご支援も受け付けています。',
  '一人称視点の和風民俗ホラー『津島・魂鬼 Revenant of Tsushima』のSteamストアページを公開しました。作品を見つけてくださった皆様、ありがとうございます。ぜひウィッシュリストに追加し、Steamでフォローして開発情報をご覧ください。',
  'ストアページの公開は、作品を世界のプレイヤーに届けるための一歩です。開発は引き続き進めており、その制作資金を支えてくださる方をPatreonとpixivFANBOXで募集しています。ご支援は任意です。各サービスの最新プランから、ご自身に合う応援方法をご検討ください。',
  'Steamページのシェアや、作品への感想も大きな励みになります。Aurora Studioとともに、この道を歩んでくださりありがとうございます。',
  'Steamでウィッシュリストに追加', 'すべてのニュース', 'お知らせを読む'),
 'zh-hant': ('zh-Hant', '《津島・魂鬼》Steam 頁面公開：邀請你支持下一段開發旅程',
  '加入 Steam 願望清單，或透過 Patreon／pixivFANBOX 支持持續開發。',
  '我們的第一人稱和風民俗恐怖遊戲《津島・魂鬼 Revenant of Tsushima》已公開 Steam 商店頁面！感謝每一位發現這款作品的玩家，歡迎加入願望清單並在 Steam 追蹤遊戲，接收後續開發消息。',
  'Steam 頁面公開，是讓全球玩家認識作品的一步；遊戲仍在開發中。我們正透過 Patreon 與 pixivFANBOX 邀請自願會員支持，為後續製作籌集開發資金。歡迎到兩個平台查看最新方案，選擇適合自己的支持方式。',
  '分享 Steam 頁面、告訴我們你對作品的期待，同樣能幫助這段旅程。謝謝你與 Aurora Studio 一起走下去。',
  '加入 Steam 願望清單', '所有消息', '閱讀公告'),
 'zh-hans': ('zh-Hans', '《津岛・魂鬼》Steam 页面公开：邀请你支持下一段开发旅程',
  '加入 Steam 愿望单，或通过 Patreon／pixivFANBOX 支持持续开发。',
  '我们的第一人称和风民俗恐怖游戏《津岛・魂鬼 Revenant of Tsushima》已公开 Steam 商店页面！感谢每一位发现这款作品的玩家，欢迎加入愿望单并在 Steam 关注游戏，接收后续开发消息。',
  'Steam 页面公开，是让全球玩家认识作品的一步；游戏仍在开发中。我们正通过 Patreon 与 pixivFANBOX 邀请自愿会员支持，为后续制作筹集开发资金。欢迎到两个平台查看最新方案，选择适合自己的支持方式。',
  '分享 Steam 页面、告诉我们你对作品的期待，同样能帮助这段旅程。谢谢你与 Aurora Studio 一起走下去。',
  '加入 Steam 愿望单', '所有消息', '阅读公告'),
 'ko': ('ko', 'Revenant of Tsushima Steam 페이지 공개 — 다음 개발 여정을 함께해 주세요',
  'Steam 찜 목록에 추가하거나 Patreon·pixivFANBOX를 통해 지속적인 개발을 후원해 주세요.',
  '1인칭 일본 민속 공포 게임 Revenant of Tsushima의 Steam 상점 페이지를 공개했습니다! 게임을 발견해 주신 모든 분께 감사드립니다. Steam에서 찜 목록에 추가하고 팔로우하여 앞으로의 개발 소식을 받아 보세요.',
  'Steam 페이지 공개는 전 세계 플레이어에게 작품을 알리는 첫걸음이며, 게임 개발은 계속되고 있습니다. Aurora Studio는 Patreon과 pixivFANBOX에서 자발적인 멤버십 후원을 받아 앞으로의 게임 제작에 필요한 개발 자금을 마련하고자 합니다. 각 플랫폼의 최신 후원 플랜을 살펴보고 자신에게 맞는 방법을 선택해 주세요.',
  'Steam 페이지를 공유하거나 게임에 대한 기대와 의견을 전해 주시는 것도 큰 힘이 됩니다. Aurora Studio와 함께 이 여정을 걸어 주셔서 감사합니다.',
  'Steam 찜 목록에 추가', '모든 소식', '공지 읽기'),
}

def route(code):
 return ('' if code == 'en' else '/'+code)+'/news/'+SLUG+'/'

def generate():
 for code, (lang,title,summary,intro,funding,thanks,steam,back,read) in COPY.items():
  shell=(ROOT/('' if code=='en' else code)/'news/revenant-of-tsushima-demo-creator-outreach/index.html').read_text(encoding='utf-8')
  url=BASE+route(code)
  index=('' if code=='en' else '/'+code)+'/news/'
  main='<main id="main"><section class="page-heading"><p class="eyebrow dark">Aurora Studio · <time datetime="2026-11-07">2026-11-07</time></p><h1 class="article-title">'+escape(title)+'</h1><p>'+escape(summary)+'</p></section><article class="section article"><p>'+escape(intro)+'</p><p><a class="button light" href="'+STEAM+'">'+escape(steam)+' ↗</a></p><p>'+escape(funding)+'</p><p>'+escape(thanks)+'</p></article>'+section(lang)+'<section class="section"><a href="'+index+'">← '+escape(back)+'</a></section></main>'
  text=re.sub(r'<html lang="[^"]+">','<html lang="'+lang+'">',shell,count=1)
  text=re.sub(r'<title>.*?</title>','<title>'+escape(title)+' | Aurora Studio</title>',text,count=1)
  text=re.sub(r'<meta name="description"[^>]*>','<meta name="description" content="'+escape(summary,quote=True)+'">',text)
  text=re.sub(r'<link rel="(?:canonical|alternate)"[^>]*>','',text)
  text=re.sub(r'<meta (?:property="(?:og:|article:)[^"]+"|name="twitter:[^"]+")[^>]*>','',text)
  graph=json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>',text,re.S)[1])['@graph']
  graph=[node for node in graph if node.get('@type') in ('Organization','Brand','WebSite')]
  graph.append({'@type':'NewsArticle','headline':title,'description':summary,'datePublished':'2026-11-07','inLanguage':lang,'url':url,'mainEntityOfPage':url,'author':{'@id':BASE+'/#organization'},'publisher':{'@id':BASE+'/#organization'},'image':BASE+'/assets/revenant-cover-v2.jpg'})
  text=re.sub(r'<script type="application/ld\+json">.*?</script>',lambda m:'<script type="application/ld+json">'+json.dumps({'@context':'https://schema.org','@graph':graph},ensure_ascii=False).replace('</','<\\/')+'</script>',text,count=1,flags=re.S)
  tags='<link rel="canonical" href="'+url+'">'+''.join('<link rel="alternate" hreflang="'+data[0]+'" href="'+BASE+route(other)+'">' for other,data in COPY.items())+'<link rel="alternate" hreflang="x-default" href="'+BASE+route('en')+'">'
  for key,value in {'og:type':'article','og:title':title,'og:description':summary,'og:url':url,'og:locale':{'en':'en_US','ja':'ja_JP','zh-hant':'zh_TW','zh-hans':'zh_CN','ko':'ko_KR'}[code],'og:image':BASE+'/assets/revenant-cover-v2.jpg','article:published_time':'2026-11-07'}.items():
   tags+='<meta property="'+key+'" content="'+escape(value,quote=True)+'">'
  tags+='<meta name="twitter:card" content="summary_large_image">'
  for key,value in {'twitter:title':title,'twitter:description':summary,'twitter:image':BASE+'/assets/revenant-cover-v2.jpg'}.items():
   tags+='<meta name="'+key+'" content="'+escape(value,quote=True)+'">'
  text=text.replace('</head>',tags+'</head>',1)
  text=re.sub(r'<main id="main">.*?</main>',lambda m:main,text,count=1,flags=re.S)
  from navigation import header
  langs='<div class="lang">'+''.join('<a href="'+route(other)+'" lang="'+data[0]+'"'+(' aria-current="page"' if other==code else '')+'>'+{'en':'EN','ja':'日本語','zh-hant':'繁體中文','zh-hans':'简体中文','ko':'한국어'}[other]+'</a>' for other,data in COPY.items())+'</div>'
  path=ROOT/route(code).strip('/')/'index.html'
  path.parent.mkdir(parents=True,exist_ok=True)
  text=re.sub(r'<header class="site-header[^"]*">.*?</header>',lambda m:header(path,langs),text,count=1,flags=re.S)
  path.write_text(text,encoding='utf-8')
  listing=ROOT/index.strip('/')/'index.html'
  text=listing.read_text(encoding='utf-8')
  text=re.sub(r'<section class="section rot-membership-news">.*?</section>','',text,flags=re.S)
  card='<section class="section rot-membership-news"><time datetime="2026-11-07">2026-11-07</time><h2>'+escape(title)+'</h2><p>'+escape(summary)+'</p><a href="'+route(code)+'">'+escape(read)+' ↗</a></section>'
  # Separate feature section preserves existing archive card translations and counts.
  text=text.replace('<section class="section news-list">',card+'<section class="section news-list">',1)
  assert card in text
  listing.write_text(text,encoding='utf-8')
  home=ROOT/('index.html' if code=='en' else code+'/index.html')
  text=home.read_text(encoding='utf-8')
  text=re.sub(r'<section class="section rot-membership-news">.*?</section>','',text,flags=re.S)
  text=text.replace('</main>',card+'</main>',1)
  home.write_text(text,encoding='utf-8')
  sitemap=ROOT/'sitemap.xml';text=sitemap.read_text(encoding='utf-8')
  if '<loc>'+url+'</loc>' not in text:
   text=text.replace('</urlset>','<url><loc>'+url+'</loc></url>\n</urlset>')
  sitemap.write_text(text,encoding='utf-8')

if __name__=='__main__':
 generate()
