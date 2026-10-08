"""Generate public English and Traditional Chinese talent network pages and entrances."""
from pathlib import Path
from html import escape
import re
ROOT=Path(__file__).parent

def generate():
 for code in ('en','zh-Hant'):
  zh=code=='zh-Hant'
  def t(en,tc): return tc if zh else en
  route='/zh-hant/careers/' if zh else '/careers/'
  roles=[
   ('Production & Operations','製作與發行營運','Publishing producer, project coordination, Steam release operations, finance and business development.','Publishing Producer、項目協調、Steam 發售營運、財務及 Business Development。'),
   ('Scout & Acquisition','Scout 與作品評估','Gameplay evaluation, market research, developer outreach and evidence-based due diligence.','玩法評估、市場研究、開發者接洽及有證據支持的 Due Diligence。'),
   ('QA & Localization','QA 與在地化','Functional and compatibility testing, translation, editing, LQA and accessibility review.','功能與兼容性測試、翻譯、編輯、LQA 及無障礙體驗評估。'),
   ('Regional Marketing & Community','區域行銷與社群','Japan, Hong Kong and Taiwan PR, community management and creator / VTuber campaign coordination.','日本、香港及台灣 PR、社群營運、Creator／VTuber 宣傳項目協調。'),
   ('Creative & Platform Specialists','創意與平台專業人才','Trailers, graphic design, marketing art, console porting and certification coordination.','預告片、平面設計、行銷美術、主機移植及 Certification 協調。'),
   ('Open Application','開放式申請','Tell us what you do best and how you could help independent developers reach new audiences.','介紹你最擅長的工作，以及如何協助獨立開發者接觸新玩家。')]
  cards=''.join(f'<article class="career-card"><p class="eyebrow dark">0{i+1} / TALENT NETWORK</p><h3>{t(a,b)}</h3><p>{t(c,d)}</p></article>' for i,(a,b,c,d) in enumerate(roles))
  def field(name,en,tc,typ='text',required=False):
   req=' required' if required else ''
   return f'<label for="{name}">{t(en,tc)}{t(" (required)","（必填）") if required else ""}<input id="{name}" name="{name}" type="{typ}" maxlength="500"{req}></label>'
  fields=field('name','Name','姓名',required=True)+field('email','Email','電郵','email',True)
  fields+=f'<label for="discipline">{t("Primary discipline (required)","主要專業領域（必填）")}<select id="discipline" name="discipline" required><option value="">{t("Choose a discipline","選擇專業領域")}</option>'+''.join(f'<option value="{escape(a)}">{t(a,b)}</option>' for a,b,_,_ in roles)+'</select></label>'
  fields+=field('location','Location / time zone','所在地／時區')+field('languages','Working languages','工作語言')+field('portfolio','Portfolio / LinkedIn URL','作品集／LinkedIn 網址','url')+field('availability','Availability / preferred engagement','可工作時間／偏好合作形式')+field('rate','Expected fee / salary and currency (optional)','期望酬金／薪酬及貨幣（選填）')
  title=t('Careers & Talent Network','職涯與人才網絡')
  description=t('Join Aurora Publishing’s talent network for future and project-based opportunities across production, QA, localization and marketing.','加入 Aurora Publishing 人才網絡，登記未來及按項目的製作、QA、在地化與行銷合作機會。')
  html=f'''<!doctype html><html lang="{code}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{title} | Aurora Publishing</title><meta name="description" content="{description}"><link rel="canonical" href="https://www.aurora-studio.org{route}"><link rel="alternate" hreflang="en" href="https://www.aurora-studio.org/careers/"><link rel="alternate" hreflang="zh-Hant" href="https://www.aurora-studio.org/zh-hant/careers/"><link rel="alternate" hreflang="x-default" href="https://www.aurora-studio.org/careers/"><meta property="og:title" content="{title} | Aurora Publishing"><meta property="og:description" content="{description}"><meta property="og:url" content="https://www.aurora-studio.org{route}"><meta property="og:type" content="website"><link rel="icon" href="/assets/aurora-studio-icon.png"><link rel="stylesheet" href="/style.css?v=20261001a"><link rel="stylesheet" href="/careers.css"><script src="/careers.js" defer></script></head><body><a class="skip" href="#main">{t('Skip to content','跳至內容')}</a><header class="site-header"><a class="brand" href="/"><span class="brand-name">Aurora Studio</span></a><nav aria-label="{t('Main navigation','主要導覽')}"><a href="/">{t('Home','首頁')}</a><a href="{'/zh-hant/publishing/' if zh else '/publishing/'}">{t('Publishing','遊戲發行')}</a><a href="{route}" aria-current="page">{t('Careers','人才招募')}</a><a href="/project/">{t('Projects','作品 (EN)')}</a><a href="/contact/">{t('Contact','聯絡 (EN)')}</a></nav><div class="lang"><a href="/careers/" lang="en">EN</a><a href="/zh-hant/careers/" lang="zh-Hant">繁</a></div></header><main id="main">
<section class="section career-hero"><p class="eyebrow">AURORA PUBLISHING / CAREERS & TALENT NETWORK</p><h1>{t('Help indie games<br><em>cross borders.</em>','讓獨立遊戲<br><em>跨越地域。</em>')}</h1><p>{description}</p><div class="actions"><a class="button light" href="#apply">{t('Join our talent network ↗','登記加入人才網絡 ↗')}</a><a class="text-link" href="#disciplines">{t('Explore disciplines ↓','探索專業領域 ↓')}</a></div></section>
<section class="career-wrap"><h2>{t('Build with purpose.','按項目需要，組建團隊。')}</h2><p>{t('Aurora Publishing is the publishing division of Hong Kong-based Aurora Studio, working to connect independent games with audiences across Asia and the world. We are building a network of people who care about developer independence, clear communication and thoughtful execution.','Aurora Publishing 是香港 Aurora Studio 的發行部門，致力連繫獨立遊戲與亞洲及全球玩家。我們正建立重視開發者自主、清晰溝通及執行品質的人才網絡。')}</p><div class="career-note"><strong>{t('Expression of interest — future / project-based opportunities','人才意向登記 — 未來／按項目合作機會')}</strong><p>{t('This page collects expressions of interest; it does not advertise confirmed funded vacancies. Opportunities depend on project needs, approved budgets and agreed terms. Submitting does not guarantee an interview, employment or paid work.','本頁收集合作意向，目前並非已確認有預算的職位招聘。機會視乎項目需要、已批准預算及雙方商定條件；登記並不保證面試、聘用或付費工作。')}</p></div><div class="career-grid"><article class="career-card"><h3>{t('Future core team opportunities','未來核心團隊機會')}</h3><p>{t('Register interest in longer-term publishing roles. A specific vacancy, scope, compensation and working arrangement will be confirmed before any offer.','登記長期發行職務的意向。具體職缺、工作範圍、薪酬及工作安排會於聘用前確認。')}</p></article><article class="career-card"><h3>{t('Project-based specialist network','按項目合作專業人才網絡')}</h3><p>{t('Freelancers and contractors can share expertise, availability and rates. Scope, fees, milestones and payment terms will be agreed before work starts.','自由工作者及承包人可提交專長、可工作時間及報價。工作開始前會商定範圍、酬金、里程碑及付款條件。')}</p></article></div></section>
<section class="career-wrap" id="disciplines"><p class="eyebrow dark">PUBLISHING WORKSTREAMS</p><h2>{t('Where you could contribute.','你可以參與的領域。')}</h2>{cards}</section>
<section class="career-apply" id="apply"><div class="career-wrap"><h2>{t('Tell us what you bring.','介紹你的專長。')}</h2><p>{t('Prepare an email introduction below, then attach your CV in your email app. Include public portfolio links and relevant experience. English or Traditional Chinese applications are welcome.','以下表格可準備申請電郵，然後於電郵程式附上 CV。請提供公開作品集連結及相關經驗，歡迎英文或繁體中文申請。')}</p><p class="career-note">{t('This form opens your email app. It does not upload files or send an application automatically; you must send the email yourself.','表格會開啟你的電郵程式，不會上傳檔案或自動遞交申請；你需要自行寄出電郵。')}</p><form id="talent-application" class="career-form">{fields}<label class="wide" for="notes">{t('Relevant experience / introduction','相關經驗／自我介紹')}<textarea id="notes" name="notes" rows="5" maxlength="1500"></textarea></label><label class="wide consent"><input type="checkbox" name="consent" required><span>{t('I agree to Aurora reviewing the information I email and contacting me about relevant talent opportunities.','我同意 Aurora 審閱我透過電郵提供的資料，並就相關人才合作機會聯絡我。')}</span></label><button class="button dark wide" type="submit">{t('Prepare application email ↗','準備申請電郵 ↗')}</button></form><p id="application-status" class="career-status" role="status" hidden>{t('Your email app was requested. Attach your CV and send the message to complete your application. If it did not open, email the address below directly.','已嘗試開啟電郵程式。請附上 CV 並寄出電郵以完成申請；如未能開啟，請直接寄往下方地址。')}</p><p>{t('Prefer to apply directly?','想直接申請？')} <a href="mailto:publishing@aurora-studio.org?subject=Aurora%20Talent%20Network%20-%20Expression%20of%20Interest">publishing@aurora-studio.org</a></p><noscript><p>{t('Please email your CV and introduction directly to the address above.','請直接將 CV 及自我介紹寄往以上電郵。')}</p></noscript><p class="career-privacy">{t('Applicant information is requested for talent review and related contact. Please do not include identity documents, bank details, medical information or confidential client material. To ask about your information, withdraw your interest or request deletion, contact publishing@aurora-studio.org.','申請資料用於人才審閱及相關聯絡。請勿提交身分證明、銀行資料、醫療資料或客戶機密。查詢個人資料、撤回合作意向或要求刪除，請聯絡 publishing@aurora-studio.org。')}</p></div></section></main><footer><strong>AURORA STUDIO</strong><div><a href="/publishing/">Publishing</a><a href="{route}">{title}</a><a href="/governance/">Governance (EN)</a></div><small>© 2026 Aurora Studio</small></footer></body></html>'''
  p=ROOT/route.strip('/')/'index.html';p.parent.mkdir(parents=True,exist_ok=True);p.write_text(html)
 # Keep generated pages discoverable across rebuilds without changing their content.
 for p in ROOT.rglob('*.html'):
  text=p.read_text()
  if '/careers/' in text: continue
  zh='zh-hant' in p.parts
  href='/zh-hant/careers/' if zh else '/careers/'
  label='人才招募' if zh else ('Careers' if 'lang="en"' in text else 'Careers (EN)')
  link=f'<a href="{href}">{label}</a>'
  text=re.sub(r'(<nav aria-label="(?:Main navigation|Navigation)">)(.*?)(</nav>)',lambda m:m[1]+m[2]+link+m[3],text,count=1,flags=re.S)
  if '<footer>' in text:text=text.replace('<small>©',link+'<small>©',1)
  p.write_text(text)
 for path in ('index.html','zh-hant/index.html','publishing/index.html','zh-hant/publishing/index.html'):
  p=ROOT/path; text=p.read_text(); zh=path.startswith('zh-hant/')
  if 'id="publishing-talent-network"' in text: continue
  title='加入 Aurora Publishing 人才網絡' if zh else 'Bring your expertise to Aurora Publishing.'
  copy='我們正收集製作、Scout、QA、在地化及行銷專業人才的合作意向。未來機會按項目需要及預算安排。' if zh else 'Share your expertise in production, scouting, QA, localization or marketing. Register interest in future and project-based opportunities.'
  href='/zh-hant/careers/' if zh else '/careers/'
  section=f'<section class="section home-extras" id="publishing-talent-network"><div class="info-panel"><p class="eyebrow dark">CAREERS &amp; TALENT NETWORK</p><h2>{title}</h2><p>{copy}</p><a href="{href}">{"探索人才合作機會" if zh else "Explore talent opportunities"} ↗</a></div></section>'
  text=text.replace('</main>',section+'</main>',1);p.write_text(text)
 sitemap=ROOT/'sitemap.xml'
 text=sitemap.read_text()
 for route in ('careers','zh-hant/careers'):
  url=f'https://www.aurora-studio.org/{route}/'
  if url not in text:text=text.replace('</urlset>',f'<url><loc>{url}</loc></url>\n</urlset>')
 sitemap.write_text(text)

if __name__=='__main__':generate()
