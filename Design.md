---
name: Confidence & Care
colors:
  surface: '#fbf9f8'
  surface-dim: '#dcd9d9'
  surface-bright: '#fbf9f8'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f6f3f2'
  surface-container: '#f0eded'
  surface-container-high: '#eae8e7'
  surface-container-highest: '#e4e2e1'
  on-surface: '#1b1c1c'
  on-surface-variant: '#45474d'
  inverse-surface: '#303030'
  inverse-on-surface: '#f3f0f0'
  outline: '#75777d'
  outline-variant: '#c5c6cd'
  surface-tint: '#545e76'
  primary: '#051125'
  on-primary: '#ffffff'
  primary-container: '#1b263b'
  on-primary-container: '#828da7'
  inverse-primary: '#bbc6e2'
  secondary: '#a14000'
  on-secondary: '#ffffff'
  secondary-container: '#fe7a34'
  on-secondary-container: '#622400'
  tertiary: '#101110'
  on-tertiary: '#ffffff'
  tertiary-container: '#252625'
  on-tertiary-container: '#8d8d8b'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#d7e2ff'
  primary-fixed-dim: '#bbc6e2'
  on-primary-fixed: '#101b30'
  on-primary-fixed-variant: '#3c475d'
  secondary-fixed: '#ffdbcc'
  secondary-fixed-dim: '#ffb694'
  on-secondary-fixed: '#351000'
  on-secondary-fixed-variant: '#7b2f00'
  tertiary-fixed: '#e3e2e0'
  tertiary-fixed-dim: '#c7c6c4'
  on-tertiary-fixed: '#1a1c1a'
  on-tertiary-fixed-variant: '#464745'
  background: '#fbf9f8'
  on-background: '#1b1c1c'
  surface-variant: '#e4e2e1'
  surface-white: '#FFFFFF'
  text-muted: '#666666'
  status-success: '#2D6A4F'
typography:
  display:
    fontFamily: Outfit
    fontSize: 64px
    fontWeight: '700'
    lineHeight: '1.1'
    letterSpacing: -0.02em
  display-mobile:
    fontFamily: Outfit
    fontSize: 42px
    fontWeight: '700'
    lineHeight: '1.2'
  headline-h1:
    fontFamily: Outfit
    fontSize: 42px
    fontWeight: '600'
    lineHeight: '1.2'
  headline-h2:
    fontFamily: Outfit
    fontSize: 32px
    fontWeight: '600'
    lineHeight: '1.3'
  headline-h3:
    fontFamily: Outfit
    fontSize: 24px
    fontWeight: '600'
    lineHeight: '1.4'
  body-lg:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '400'
    lineHeight: '1.6'
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: '1.6'
  label-caps:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '700'
    lineHeight: '1'
    letterSpacing: 0.1em
  button-text:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '600'
    lineHeight: '1'
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  base: 8px
  section-desktop: 120px
  section-mobile: 80px
  gutter: 32px
  container-max: 1200px
---

## Brand & Style

This design system is built on the narrative of "The Professional Neighbor." It rejects the sterile, detached feel of corporate cleaning franchises in favor of a "tradie-business" aesthetic that balances industrial competence with residential warmth. The style is **Corporate / Modern** but heavily flavored with **Tactile** elements to ground the digital experience in the physical reality of the service.

The brand personality is confident, direct, and authoritative (Navy), yet energetic and helpful (Orange). It evokes a sense of relief for the homeowner—knowing that a capable expert is handling their home. Visually, this is achieved through generous whitespace, high-quality photography of real equipment/people, and a structured layout that feels organized and reliable.

## Colors

The palette is anchored by **Deep Navy**, representing the "blue-collar professional" authority and trustworthiness. **Warm Orange** is used strategically as a high-visibility action color for conversions and vital information.

The background is a **Warm Cream/Off-white** rather than a sterile pure white, ensuring the digital experience feels as inviting as a clean home. Surface elements like cards and accordions use pure white to pop against the cream background. Text is kept in a deep charcoal to maintain high legibility without the harshness of pure black.

## Typography

This system uses a "Modern Humanist" pairing. **Outfit** is selected for headlines to provide a clean, geometric, yet friendly presence that feels contemporary. **Inter** is used for all body text and UI labels due to its exceptional clarity and systematic feel.

- **Headlines:** Use tight letter spacing for display sizes to create a "bold" impact.
- **Body Text:** Maintain generous line heights (1.6) to ensure the information feels accessible and easy to scan for busy homeowners.
- **Scale:** On mobile, display sizes should aggressively scale down to prevent awkward word breaks while maintaining a strong visual hierarchy.

## Layout & Spacing

The layout follows a **Fixed Grid** philosophy with a maximum width of 1200px. It utilizes a 12-column system for desktop and a single-column stack for mobile.

The rhythm is intentionally "slow" with 120px of vertical breathing room between major sections on desktop. This whitespace communicates a premium service level—we aren't rushing, and neither should the user.

**Component Spacing:**
- Cards use a standard 32px internal padding (the "Safe Zone").
- Elements within cards (icon, title, description) are separated by 16px.
- Grid gaps for 2x2 service cards should be 32px to match the internal padding.

## Elevation & Depth

To maintain the "Confident & Friendly" feel, elevation is subtle and organic. We avoid heavy, artificial shadows in favor of **Tonal Layers** and **Ambient Depth**.

- **Cards:** Use a soft, natural shadow (`0 4px 20px rgba(0,0,0,0.05)`) to lift them slightly off the cream background.
- **Interactive States:** On hover, cards should increase their shadow slightly and lift -2px on the Y-axis.
- **AI Widget:** Should have a higher elevation than standard cards to appear "closest" to the user, using a more pronounced shadow to indicate its floating nature.
- **Overlays:** Use a subtle Deep Navy gradient (20-40% opacity) over hero images to ensure white typography remains legible without losing the "real photography" feel.

## Shapes

A **Rounded (0.5rem / 8px - 12px)** shape language is used throughout the system. This softens the edges of a "heavy equipment" business, making the brand feel more approachable for domestic settings.

- **Small elements (buttons, inputs):** 12px radius.
- **Large elements (cards, service blocks):** 16px radius.
- **AI Widget:** Uses a circular "pill" shape or high roundedness (24px+) to distinguish it as a separate functional entity.
- **Icons:** Use "Soft" rounded corners for any custom SVG strokes to match the container language.

## Components

### Buttons
- **Primary:** Warm Orange background, white text. Bold, 12px radius. High-impact for "Get a Quote" or "Call Now."
- **Secondary (Outline):** 2px Deep Navy border, Navy text, transparent background. Used for less urgent actions like "Read More."

### Service Method Cards
A 2x2 grid style on desktop. White background, 16px radius, subtle shadow. Elements include an icon/emoji (top-left), H3 title (Navy), and Body-md description.

### Testimonial Cards
Simple white cards with a 5-star rating (Orange) at the top. Use italicized Body-md for the quote and a small "Verified Client" label in Text-muted.

### Accordion (FAQs)
Clean, flat style with a simple + / - or Chevron icon. The header uses Navy H3-sized text. Only one item should be open at a time to keep the layout tidy.

### Mobile Sticky Call Bar
Pinned to the bottom (Z-index: 1000). Solid Warm Orange background. Features a clear Phone Icon and "Call Mike & Jack Now" in bold white text.

### AI Receptionist Widget
Deep Navy bubble floating in the bottom-right. Must sit at a higher Z-index than the sticky bar. Includes a small white "typing" indicator or tooltip ("Hi, I'm Mike's AI assistant!") on initial load.

### Trust Signals
A horizontal row of clean, single-color (Navy or Orange) icons. Focus on simplicity—"Google 5-Star," "Fully Insured," and "Local Family Business." No heavy backgrounds; let the icons breathe.
