# Agent Instructions — Quick Carpet Cleaners Website

## CRITICAL INSTRUCTION

**Whenever creating any component, page, or UI element, you MUST reference and apply the design system defined in `Design.md` before writing a single line of code.** Do not invent colours, fonts, spacing, radii, or shadows from scratch. Every visual decision must trace back to a token or rule in `Design.md`.

---

## Workflow

1. Read `Design.md` at the start of any build task
2. Read `CLAUDE.md` for project context, asset list, SEO rules, and component specs
3. Build using only the tokens, typography, spacing, and component patterns defined in those files
4. Reference `/full/` images for desktop and `/mobile/` images for mobile breakpoints

---

## Design Token Quick Reference

| Token | Value |
|-------|-------|
| Primary (Navy) | `#051125` / `#1b263b` |
| Accent (Orange) | `#fe7a34` |
| Background | `#fbf9f8` |
| Surface / Cards | `#ffffff` |
| Text | `#1b1c1c` |
| Text muted | `#666666` |
| Headline font | Outfit |
| Body font | Inter |
| Border radius (small) | 8px |
| Border radius (cards) | 16px |
| Border radius (AI widget) | 24px+ |
| Card shadow | `0 4px 20px rgba(0,0,0,0.05)` |
| Container max-width | 1200px |
| Section padding desktop | 120px vertical |
| Section padding mobile | 80px vertical |
| Card internal padding | 32px |

---

## Component Rules

- **Primary button:** Orange `#fe7a34` background, white text, 12px radius
- **Secondary button:** 2px Navy border, Navy text, transparent background
- **Cards:** White background, 16px radius, `0 4px 20px rgba(0,0,0,0.05)` shadow; on hover lift -2px Y and increase shadow
- **Mobile sticky call bar:** Orange background, z-index 1000, "Call Mike & Jack Now"
- **AI widget:** Navy bubble, bottom-right, z-index above sticky bar, 24px+ radius
- **Accordion:** One item open at a time, Chevron toggle, Navy H3 text
- **Trust signals:** Single-colour Navy or Orange icons, no heavy backgrounds

---

## SEO Rules

- Every page must include its target keyword in the H1, first paragraph, and at least two subheadings
- Use the site-wide n-gram phrases consistently: "carpet cleaning Queensland", "pet stain and odour removal", "bond carpet cleaning", "end of lease carpet cleaning", "carpet cleaning with pest control", "advanced spot and stain treatment", "couch and upholstery cleaning"
- Every seed page must link to: root page + 2–4 related seeds + 3–6 nodes + booking CTA
- Every node page must link upward to its parent seed
- Add appropriate schema on every page: `LocalBusiness`, `Service`, `FAQPage`, `BreadcrumbList`, `Organization`

---

## What NOT to Do

- Do not use colours, fonts, or spacing values not found in `Design.md`
- Do not create suburb/location pages without unique local proof content
- Do not make "bond guaranteed" or "100% stain removal" claims
- Do not put the AI widget below the mobile sticky call bar in z-index
- Do not use pure white `#ffffff` as the page background — use `#fbf9f8`
