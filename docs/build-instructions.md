# Build Instructions - QCC Location Pages

This document is the authoritative reference for building the parent hub page and 9 suburb pages. It overrides any conflicting information in `location_pages_blueprint.md`.

---

## Business Data (use throughout all pages)

- Business name: Quick Carpet Cleaners
- Owners: Michael and Jack
- Phone: 0484 312 966
- Email: office@quick-carpet-cleaners.com.au
- Base location: Upper Coomera, QLD
- ABN: 92 887 853 691
- Domain: qccgoldcoast.com.au
- Review claim: "97+ Five-Star Reviews" (never use "4.9 stars" - not substantiated)
- Hours: Mon-Sat 7am-6pm

---

## URL Convention

- Parent hub: `/carpet-cleaning-gold-coast/index.html`
- Suburb pages: `/carpet-cleaning-{suburb-slug}/index.html`
  - `/carpet-cleaning-helensvale/`
  - `/carpet-cleaning-coomera/`
  - `/carpet-cleaning-pimpama/`
  - `/carpet-cleaning-upper-coomera/`
  - `/carpet-cleaning-ormeau/`
  - `/carpet-cleaning-oxenford/`
  - `/carpet-cleaning-pacific-pines/`
  - `/carpet-cleaning-hope-island/`
  - `/carpet-cleaning-sanctuary-cove/`

No nested `/locations/` folder. Match the existing convention used by service pages (`/vacate-exit-carpet-cleaning/`, etc.).

---

## Design System

Reuse the existing design system from the homepage. Do NOT introduce new styles.

- Copy the homepage's full `<style>` block verbatim into each new page
- Fonts: Outfit (display) and Inter (body) - loaded via Google Fonts
- Primary orange: `--secondary-container: #fe7a34`
- Primary dark: `--primary: #051125`
- Component classes to reuse: `.nav`, `.hero`, `.trust-bar`, `.services-grid`, `.svc-card`, `.about-inner`, `.proof-grid`, `.testi-grid`, `.faq-item`, `.cta-contact`, `.footer`, `.sticky-call`, `.ai-widget`

---

## Schema (per suburb page)

```json
{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "name": "Quick Carpet Cleaners - {{ SUBURB }}",
  "description": "Professional carpet cleaning, couch and upholstery cleaning, pet stain and odour removal, and bond carpet cleaning serving {{ SUBURB }} and surrounding Gold Coast suburbs.",
  "url": "https://qccgoldcoast.com.au/carpet-cleaning-{{ slug }}/",
  "telephone": "0484312966",
  "email": "office@quick-carpet-cleaners.com.au",
  "address": {
    "@type": "PostalAddress",
    "addressLocality": "{{ SUBURB }}",
    "addressRegion": "QLD",
    "addressCountry": "AU"
  },
  "geo": {
    "@type": "GeoCoordinates",
    "latitude": "{{ LAT }}",
    "longitude": "{{ LNG }}"
  },
  "areaServed": [
    { "@type": "AdministrativeArea", "name": "{{ SUBURB }}" },
    { "@type": "AdministrativeArea", "name": "{{ NEIGHBOUR_1 }}" },
    { "@type": "AdministrativeArea", "name": "{{ NEIGHBOUR_2 }}" }
  ],
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "5",
    "reviewCount": "97"
  },
  "openingHours": "Mo-Sa 07:00-18:00",
  "hasOfferCatalog": {
    "@type": "OfferCatalog",
    "name": "Carpet Cleaning Services",
    "itemListElement": [
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Bond-Back Carpet Cleaning" }},
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Couch and Upholstery Cleaning" }},
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Pet Stain and Odour Removal" }},
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Spot and Stain Treatment" }},
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Carpet Cleaning and Pest Control Combo" }}
    ]
  }
}
```

---

## Lat/Long Coordinates

| Suburb | Latitude | Longitude |
|---|---|---|
| Pimpama | -27.8333 | 153.3000 |
| Coomera | -27.8667 | 153.3167 |
| Upper Coomera | -27.9000 | 153.3000 |
| Ormeau | -27.7500 | 153.2500 |
| Oxenford | -27.8833 | 153.3167 |
| Pacific Pines | -27.9333 | 153.3333 |
| Hope Island | -27.8667 | 153.3500 |
| Sanctuary Cove | -27.8500 | 153.3667 |
| Helensvale | -27.9167 | 153.3333 |

---

## Suburb Hero Images

Located at `/full/suburbs/`. Use the specified alt text exactly in the hero `<img>` tag on each suburb page.

| Suburb | Filename | Alt Text |
|---|---|---|
| Helensvale | carpet-cleaning-helensvale-station.webp | Same-day steam carpet cleaning services available near Helensvale Station. |
| Coomera | carpet-cleaners-coomera-dreamworld.webp | Professional steam extraction and stain removal services near Dreamworld Coomera. |
| Pimpama | steam-carpet-cleaning-pimpama-sports-hub.webp | Deep steam carpet cleaning to remove construction dust near Pimpama Sports Hub. |
| Upper Coomera | pet-stain-removal-upper-coomera-springs.webp | Local carpet cleaning and pet stain treatment near Coomera Springs Park. |
| Sanctuary Cove | luxury-carpet-cleaning-sanctuary-cove-marina.webp | Premium wool carpet cleaning and delicate rug care at Sanctuary Cove Marina. |
| Hope Island | wool-carpet-care-hope-island-marina.webp | Safe wool carpet care and premium upholstery cleaning at Hope Island Marina. |
| Pacific Pines | allergen-free-carpet-cleaning-pacific-pines-park.webp | Allergen reduction and deep carpet steam cleaning near Pacific Pines Central Park. |
| Oxenford | stain-removal-oxenford-movie-world.webp | Stubborn stain removal and carpet restoration near Warner Bros Movie World. |
| Ormeau | acreage-carpet-cleaning-ormeau-fields.webp | Heavy-duty steam carpet cleaning for acreage estates in Ormeau. |

---

## Content Uniqueness Rule

The blueprint provides a near-identical opening paragraph formula for all 9 suburbs. **Do not use it as-is.** For each suburb, write a unique 60-90 word opening paragraph that weaves in:

- The dominant property type (from blueprint Section 4)
- 2-3 specific local entities (e.g. "Westfield Helensvale", "Sanctuary Cove Marina")
- The suburb-specific pain points (e.g. "red clay tracked in from new estate construction in Pimpama")

No two pages should share more than 35% of their body content.

---

## Testimonial Handling

Reuse the 3 existing testimonials from the homepage initially. Change only the location label to match the current suburb (Sarah M. becomes Helensvale on Helensvale page, etc., rotating naturally across pages). Add this HTML comment above the testimonials section on every suburb page:

```html
<!-- TODO: Replace with real suburb-specific reviews when available -->
```

Do not invent new fake testimonials.

---

## Reassurance Line

Use "Upper Coomera locals - servicing the full Gold Coast" wherever the blueprint specifies a reassurance nudge. Do NOT use "Southport and Northern Gold Coast locals."

---

## Suburb Cluster (from blueprint Section 4)

Quality Nodes (deepest content treatment): Helensvale, Coomera, Pimpama

Supporting Nodes: Upper Coomera, Ormeau, Oxenford, Pacific Pines, Hope Island, Sanctuary Cove

Neighbour links per suburb (for internal linking and `areaServed` schema): see blueprint Section 4 matrix.

---

## Homepage Fixes (do these as part of the build)

1. Footer Suburbs column has 3 empty `<li>` slots - populate with the missing suburb links
2. Footer Services link `/carpet-cleaning-queensland/` - change to `/carpet-cleaning-gold-coast/`
3. Homepage FAQ answer about service areas - link each suburb name to its new page

---

## Build Order (STOP at each checkpoint)

1. Parent hub page at `/carpet-cleaning-gold-coast/`. Stop for review.
2. Helensvale only. Stop for review.
3. Coomera + Pimpama. Stop for review.
4. The 6 Supporting Nodes. Stop for review.
5. Homepage fixes + cross-page link audit.