# Revenant of Tsushima supporter campaign

The campaign invites voluntary Patreon / pixivFANBOX membership to fund continued
game development. Copy is provided in English, Traditional Chinese, Simplified
Chinese, Japanese and Korean. No prices, reward schedules, Steam keys, build access
or delivery dates are promised without verification of the chosen platform tier.

## Pages and maintenance

- Five localized homepages: RoT supporter section and news feature.
- Five localized news indexes: feature linking to the matching translated article.
- Five articles at `[locale]/news/revenant-of-tsushima-steam-page-development-support/`
  (no locale prefix for English), with reciprocal language links, canonical URLs,
  localized social metadata and NewsArticle data. Articles are dated November 7, 2026;
  adjust the visible and metadata dates together if publication is delayed.
- English `/support/` and `/project/revenant-of-tsushima/`: RoT membership CTAs.
- All five article routes are included in the sitemap.

Edit `rot_membership.py` for supporter section copy and `membership_news.py` for the
announcement. Run `python membership_news.py` to refresh only the news articles,
feature links and sitemap; it is also called by the existing `news_i18n.py` workflow.
The existing `build.py` and `localize.py` include the membership sections when
regenerating the site. Legacy full-site generators can change unrelated checked-in
content: review their complete diff before publishing.

## Scope and policy review

This change is for the studio website. Steam app 5529920 already has a dedicated
official-website link. No Steam description, artwork, announcement or website-link
destination is changed. Website membership promotion is not represented as Valve
approval or an exemption for paid promotions on Steam.

- [Steam description rules](https://partner.steamgames.com/doc/store/page/description)
  prohibit promoting or linking to external sites in descriptions or artwork and
  direct developers to the dedicated Basic Info website/social fields.
- [itch.io Patreon integration](https://itch.io/docs/creators/patreon) is available
  separately; no access entitlements or storefront settings are changed here.

The supplied Patreon and FANBOX URLs are used exactly as requested. Automated
reading of their current membership tiers was unavailable; verify the public
campaign destinations and benefits before publishing any specific rewards.

## Validation

- 34 Chrome desktop/mobile checks across 17 studio pages: visible CTAs and news
  features, exact destination URLs, no horizontal overflow, unique IDs, valid
  article JSON data, all five language alternates, no JavaScript errors.
- Screenshot review at 390px and 1280px.
- Scoped announcement generation is repeatable without duplicate features.
- Existing repository tests: 6 passed, 2 failed. Both failures also occur at the
  unchanged upstream commit: Windows case-insensitive `Ads.txt` checking and an
  archive test fixed at 15 stories (upstream now has 16). The new announcement is
  a separate feature above the existing archive.

Publishing remains separate from this review branch. After deployment, open all
five public articles and check both membership destinations manually.
