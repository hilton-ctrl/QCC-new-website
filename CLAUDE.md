# Quick Carpet Cleaners — Website Project

## Project Overview

This is the website build for **Quick Carpet Cleaners (QCC)**, a Gold Coast-based residential carpet and upholstery cleaning business. Owners: **Michael & Jack**. The website is a conversion-focused local service site with an AI receptionist widget and a structured SEO content network.

The build uses **HTML/CSS/JS** (no framework assumed). All design decisions are governed by `Design.md`.

---

## Business Context

- **Business name:** Quick Carpet Cleaners
- **Owners:** Michael & Jack
- **Location:** Gold Coast, Queensland, Australia
- **Primary phone CTA:** "Call Michael & Jack Now"
- **Services:** Carpet cleaning, couch/upholstery cleaning, pet stain & odour removal, vacate/exit/bond cleaning, carpet + pest control, advanced spot & stain treatment
- **Brand narrative:** "The Professional Neighbor" — tradie-business aesthetic, not a corporate franchise
- **AI receptionist:** Widget branded as "Michael's AI assistant" — Deep Navy bubble, bottom-right, high z-index

---

## Design System

All visual decisions live in `Design.md`. Key facts:

- **Design system name:** Confidence & Care
- **Primary colour:** Deep Navy `#051125` / `#1b263b`
- **Accent/CTA colour:** Warm Orange `#fe7a34` / `#a14000`
- **Background:** Warm Cream `#fbf9f8` (not pure white)
- **Surface/cards:** Pure White `#ffffff`
- **Headline font:** Outfit (600–700 weight)
- **Body/UI font:** Inter (400–600 weight)
- **Border radius:** 8px small elements, 16px cards, 24px+ AI widget
- **Container max-width:** 1200px
- **Section padding desktop:** 120px vertical
- **Card internal padding:** 32px
- **Card shadow:** `0 4px 20px rgba(0,0,0,0.05)`

---

## Assets

### Images (`/images/fin-images/`, `/full/`, `/mobile/`)
- `owner-portrait-hero.webp` — hero section (full + mobile variants)
- `owner-with-van-hero.webp` — van + branding shot
- `team-mike-and-jack-equipment.webp` — team photo with equipment
- `owner-cleaning-yacht-deck.webp` — premium job proof
- `before-after-carpet-extraction-1.webp` — before/after proof
- `before-after-couch-cushions-1.webp` — upholstery before/after
- `carpet-extraction-wand-2.webp`, `carpet-extraction-wand-3.webp` — process shots
- `carpet-clean-after-stairway.webp`, `carpet-cleaning-lounge-room.webp`
- `couch-cleaning-outdoor-patio.webp`, `couch-cleaning-action-sectional.webp`
- `couch-cushions-clean-detail.webp`, `couch-cushions-dirty-detail.webp`
- `upholstery-chair-cushion-detail.webp`
- `logo-quick-carpet-cleaners.webp` (full + mobile)
- `helper.png` — supporting graphic

### Videos (`/vids/`)
- `vid-stairs.mp4` — stairway carpet clean
- `carpet.mp4` — carpet cleaning process
- `tune-tt.mp4` — (check usage with client)

Use `/full/` images for desktop and `/mobile/` for mobile breakpoints where both exist.

---

## SEO Content Architecture (SRO Plan)

The site uses a **Root → Seed → Node** semantic content network. Do not flatten this into a single-page site.

### Central entity
Professional carpet cleaning for Queensland homes, rentals, and pet-affected properties.

### Page hierarchy

| Level | URL | Purpose |
|-------|-----|---------|
| Root | `/carpet-cleaning-queensland/` | Central commercial hub, links to all seeds |
| Seed 1 | `/pet-stain-odour-carpet-cleaning/` | Pet urine, odour, staining |
| Seed 2 | `/vacate-exit-carpet-cleaning/` | Bond/end-of-lease/exit cleaning |
| Seed 3 | `/carpet-cleaning-pest-control/` | Combined service — highest QLD demand |
| Seed 4 | `/advanced-spot-stain-treatment/` | Tough stains: red wine, blood, coffee, rust |
| Seed 5 | `/couch-upholstery-cleaning/` | Sofas, lounges, upholstery |
| Local | `/carpet-cleaning-gold-coast/` + suburb pages | Real service areas only |

### Priority keyword targets (QLD-specific)

| Keyword | QLD Vol/mo | Notes |
|---------|-----------|-------|
| carpet cleaning and pest control | 320 | 82% of AU volume is QLD — top priority |
| bond carpet cleaning | 40 | 57% QLD-skewed, highest CPC ($9.53) |
| end of lease carpet cleaning | 50 | KD 9, best all-round commercial target |
| couch cleaning | 1,600 | Highest absolute volume |
| upholstery cleaning | 260 | KD 5 nationally — easiest win |
| carpet cleaning near me | high | KD 3 — anchor the root page around this |

### Phrasing rules
- Prefer "bond carpet cleaning" over "vacate" in QLD-targeted content
- Use "end of lease" not "exit" for the rental seed page
- "carpet cleaning and pest control" is a QLD-dominant term — lead with it in Seed 3
- Node pages (pet odour combos, specific stains) have near-zero search volume — they exist for topical depth and internal linking, not direct traffic

### Internal linking
- Homepage → Root page + all 5 seeds
- Every seed → root + 2–4 related seeds + 3–6 nodes + CTA
- Every node → its parent seed → related seeds → CTA

---

## Components

### Mobile Sticky Call Bar
- Pinned bottom, z-index 1000
- Solid Warm Orange background
- "Call Michael & Jack Now" — bold white text + phone icon

### AI Receptionist Widget
- Deep Navy bubble, bottom-right, z-index above sticky bar
- Tooltip on load: "Hi, I'm Michael's AI assistant!"
- Pill/high-roundedness shape (24px+)

### Trust Signals row
- Navy or Orange single-colour icons
- "Google 5-Star", "Fully Insured", "Local Family Business"
- No heavy backgrounds — icons breathe

### FAQs Accordion
- One item open at a time
- Chevron or +/- toggle
- Navy H3 text for question headers

### Schema (add to every relevant page)
- `LocalBusiness`
- `Service` (per service page)
- `FAQPage` (where FAQs appear)
- `BreadcrumbList`
- `Organization`
- `ImageObject` for before/after images

---

## Build Order

1. Homepage (with pet + exit + stain + couch context, links to all seeds)
2. Carpet Cleaning Queensland — root page
3. Pet Stain & Odour seed
4. Vacate/Exit/Bond Cleaning seed
5. Carpet Cleaning + Pest Control seed
6. Advanced Spot & Stain Treatment seed
7. Couch & Upholstery Cleaning seed
8. Top 10 supporting node pages
9. Service-area / local suburb pages (Gold Coast + high-value suburbs only)
10. FAQs, before/after galleries, reviews, case studies

---

## Rules & Constraints

- Do not make "bond guaranteed" or "100% stain removal" claims unless client confirms
- Do not mass-generate thin suburb pages — only create local pages for real service areas with unique local proof
- Pest control licensing/chemical claims require client verification before publishing
- Keep AI widget z-index strictly above the mobile sticky call bar
- All copy must use the site-wide n-gram phrases consistently in titles, intros, headings, and anchor text

### Counted claims must stay in sync with the page

Some headings assert a number that the page itself has to satisfy. If the
underlying content changes, the heading is no longer true — on a site whose
entire positioning is now honesty, that matters more than usual.

| Claim | Location | Must match |
|---|---|---|
| "The six things people ask before they book." | Homepage, Quick Questions H2 | the number of `.faq-item` blocks in `section.faq-quick` (currently 6) |
| "97 five-star reviews" | Homepage hero badge, hero stat, trust H2, trust card, form proof strip | the real Google review count — update everywhere at once |
| "4,000+ cleans" / "nine years" | Homepage hero stat, mechanism close, About, form proof strip; bond, faqs, pet-stain-rental pages | client-confirmed figures (see below) |

### Client-verified facts (`qcc=questions.rtf`, Aug 2026 — supersedes earlier drafts)

- **Nine years** of operation (since 2017) — *not* 8 years / 2018
- **4,000+ cleans** — *not* the 1,465 figure in the older drafts
- **Zero carpets ever flagged by a property manager** — the substitute proof that replaced the guarantees
- **97 five-star Google reviews**
- Fresh Home Reset offer: **$330** (VSL/landing copy only — not yet reconciled with the live pricing page)

### No return-visit guarantees — ever

The client explicitly declined all of these. Do not reintroduce them in any
page, draft, or schema block:

- ❌ free re-clean of property-manager-flagged areas
- ❌ 14-day stain re-treat
- ❌ "we'll come back at no extra charge"

His reasoning: if a carpet doesn't come up the first time it is damaged rather
than dirty, so a return visit cannot fix it. Use the zero-flagged record as the
risk-reversal substitute instead.

**Pet-odour copy** must keep the backing/underlay caveat — cleaning cannot reach
urine below the carpet without lifting it. Never claim odour removal that
requires reaching the underlay.

### The mechanism

Every job runs as **The Walk-Through Guarantee Clean** (name client-approved):
Locked Quote → Stain-Matched Clean → Walk-Through Sign-Off. The **Four Named
Methods are Step Two up close**, not a competing mechanism — keep them nested.
The sign-off is same-visit only; it is not a promise to return.

Superseded drafts in `qcc-sales-letter/drafts/` (`*-v2.md`,
`carpet-cleaning-VSL-script.md`) and `qcc=questions.md` still carry the old
figures and guarantees. They are dated archives — do not copy from them.
