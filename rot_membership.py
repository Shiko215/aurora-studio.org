"""Optional RoT membership CTAs for studio pages. No tier benefits are assumed."""
from html import escape
COPY = {'en': {'eyebrow': 'SUPPORT INDEPENDENT DEVELOPMENT',
        'title': 'Help the pilgrimage continue.',
        'body': 'Help fund the continued development of Revenant of Tsushima, a Japanese folk '
                'horror journey through forgotten shrines and restless spirits. Become a supporter '
                'on Patreon or pixivFANBOX and help Aurora Studio keep creating.',
        'note': 'Membership is optional. Check each platform for current prices, billing terms and '
                'tier benefits before joining. Game purchases, Steam keys and access to builds are '
                'included only when explicitly listed in your chosen tier.',
        'patreon': 'Become a Patreon supporter',
        'fanbox': 'Become a FANBOX supporter',
        'nav': 'Support',
        'steam': 'Add Revenant of Tsushima to your Steam wishlist and follow the game for '
                 'development updates.'},
 'ja': {'eyebrow': 'インディーゲーム開発を応援',
        'title': 'この巡礼の続きを、ともに。',
        'body': '忘れられた神社と彷徨う魂を巡る和風民俗ホラー『津島・魂鬼 Revenant of '
                'Tsushima』。PatreonまたはpixivFANBOXの支援者となり、Aurora '
                'Studioが制作を続けるための開発資金を支えていただけませんか。作品が形になる旅路を、ともに歩んでください。',
        'note': 'メンバーシップへの参加は任意です。料金・請求条件・特典は、各サービスの最新のプランをご確認ください。ゲーム本編、Steamキー、開発ビルドへのアクセスは、選択したプランに明記されている場合に限り含まれます。',
        'patreon': 'Patreonで支援する',
        'fanbox': 'FANBOXで支援する',
        'nav': '開発を応援',
        'steam': '『津島・魂鬼 Revenant of Tsushima』をSteamのウィッシュリストに追加し、フォローして開発情報をチェックしてください。'},
 'zh-Hant': {'eyebrow': '支持獨立遊戲開發',
             'title': '讓這段巡禮繼續走下去。',
             'body': '與 Aurora Studio 一起，讓《津島・魂鬼 Revenant of '
                     'Tsushima》的民俗恐怖世界逐步成形，走進被遺忘的神社與徘徊的魂靈。歡迎透過 Patreon 或 pixivFANBOX '
                     '成為支持者，為後續製作提供開發資金，陪伴我們繼續創作。',
             'note': '加入會員完全自願。訂閱前請查看各平台最新的價格、扣款條款及方案福利。只有所選方案明確列出時，才包含遊戲本體、Steam 序號或開發版本存取權。',
             'patreon': '成為 Patreon 支持者',
             'fanbox': '成為 FANBOX 支持者',
             'nav': '支持開發',
             'steam': '將《津島・魂鬼 Revenant of Tsushima》加入 Steam 願望清單，並追蹤遊戲以獲取開發消息。'},
 'zh-Hans': {'eyebrow': '支持独立游戏开发',
             'title': '让这段巡礼继续走下去。',
             'body': '与 Aurora Studio 一起，让《津岛・魂鬼 Revenant of '
                     'Tsushima》的民俗恐怖世界逐步成形，走进被遗忘的神社与徘徊的魂灵。欢迎通过 Patreon 或 pixivFANBOX '
                     '成为支持者，为后续制作提供开发资金，陪伴我们继续创作。',
             'note': '加入会员完全自愿。订阅前请查看各平台最新的价格、扣款条款及方案福利。只有所选方案明确列出时，才包含游戏本体、Steam 序号或开发版本访问权。',
             'patreon': '成为 Patreon 支持者',
             'fanbox': '成为 FANBOX 支持者',
             'nav': '支持开发'},
 'ko': {'eyebrow': '인디 게임 개발 후원',
        'title': '이 순례가 계속될 수 있도록.',
        'body': '잊힌 신사와 떠도는 영혼을 만나는 일본 민속 공포 게임 Revenant of Tsushima. Patreon 또는 pixivFANBOX에서 '
                '후원자가 되어 Aurora Studio의 지속적인 게임 제작에 필요한 개발 자금을 지원하고, 작품이 완성되어 가는 여정을 함께해 주세요.',
        'note': '멤버십 가입은 선택 사항입니다. 가입 전 각 플랫폼의 최신 요금, 결제 조건 및 플랜별 혜택을 확인해 주세요. 게임 본편, Steam 키 및 개발 '
                '빌드 이용 권한은 선택한 플랜에 명시된 경우에만 포함됩니다.',
        'patreon': 'Patreon 후원자 되기',
        'fanbox': 'FANBOX 후원자 되기',
        'nav': '개발 후원'}}
P = 'https://www.patreon.com/c/revenant_tsushima'
F = 'https://shikosama.fanbox.cc/'
def section(lang, game=False, ident='support-rot'):
 c = COPY[lang]
 wrapper = 'wrap' if game else 'rot-membership-inner'
 return f'''<section class="section rot-membership" id="{ident}" lang="{lang}" aria-labelledby="{ident}-heading"><div class="{wrapper}"><p class="eyebrow">{escape(c['eyebrow'])}</p><h2 id="{ident}-heading">{escape(c['title'])}</h2><p class="rot-membership-copy">{escape(c['body'])}</p><div class="actions"><a class="button" href="{P}" target="_blank" rel="noopener noreferrer">{escape(c['patreon'])} ↗</a><a class="button" href="{F}" target="_blank" rel="noopener noreferrer">{escape(c['fanbox'])} ↗</a></div><p class="rot-membership-note">{escape(c['note'])}</p></div></section>'''
