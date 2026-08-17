---
name: TableMate AI
colors:
  surface: '#131316'
  surface-dim: '#131316'
  surface-bright: '#39393c'
  surface-container-lowest: '#0e0e11'
  surface-container-low: '#1b1b1e'
  surface-container: '#1f1f22'
  surface-container-high: '#2a2a2d'
  surface-container-highest: '#353438'
  on-surface: '#e4e1e6'
  on-surface-variant: '#e4bebc'
  inverse-surface: '#e4e1e6'
  inverse-on-surface: '#303033'
  outline: '#ab8987'
  outline-variant: '#5b403f'
  surface-tint: '#ffb3b1'
  primary: '#ffb3b1'
  on-primary: '#680011'
  primary-container: '#ff535a'
  on-primary-container: '#5b000e'
  inverse-primary: '#bb162c'
  secondary: '#ffb955'
  on-secondary: '#452b00'
  secondary-container: '#dc9100'
  on-secondary-container: '#4f3100'
  tertiary: '#c7c5d4'
  on-tertiary: '#2f2f3b'
  tertiary-container: '#908f9e'
  on-tertiary-container: '#292934'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#ffdad8'
  primary-fixed-dim: '#ffb3b1'
  on-primary-fixed: '#410007'
  on-primary-fixed-variant: '#92001c'
  secondary-fixed: '#ffddb4'
  secondary-fixed-dim: '#ffb955'
  on-secondary-fixed: '#291800'
  on-secondary-fixed-variant: '#633f00'
  tertiary-fixed: '#e3e1f1'
  tertiary-fixed-dim: '#c7c5d4'
  on-tertiary-fixed: '#1a1b26'
  on-tertiary-fixed-variant: '#464652'
  background: '#131316'
  on-background: '#e4e1e6'
  surface-variant: '#353438'
typography:
  display-lg:
    fontFamily: Inter
    fontSize: 48px
    fontWeight: '700'
    lineHeight: 56px
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Inter
    fontSize: 32px
    fontWeight: '700'
    lineHeight: 40px
    letterSpacing: -0.01em
  headline-lg-mobile:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '700'
    lineHeight: 32px
  headline-md:
    fontFamily: Inter
    fontSize: 20px
    fontWeight: '600'
    lineHeight: 28px
  body-lg:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  body-ai-italic:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 26px
  label-md:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '500'
    lineHeight: 20px
    letterSpacing: 0.01em
  label-sm:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '600'
    lineHeight: 16px
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  base: 4px
  xs: 8px
  sm: 12px
  md: 16px
  lg: 24px
  xl: 32px
  gutter: 16px
  margin-mobile: 20px
  margin-desktop: 40px
---

## Brand & Style
The design system for TableMate AI is centered on a "Sophisticated Gastronomy" aesthetic, blending the precision of a high-end developer tool with the warmth of a premium concierge service. The brand personality is discerning, intelligent, and effortless. It aims to evoke a sense of exclusivity and reliability, ensuring users feel they are receiving expert, AI-curated recommendations. 

The style utilizes a **Modern Corporate** foundation with **Glassmorphism** highlights to denote "intelligence." Drawing inspiration from high-productivity tools, it maintains a strict grid and functional clarity, while using warm accents to ground the experience in the culinary world.

## Colors
The palette is built on a "Deep Charcoal" foundation to allow high-quality food photography and AI insights to pop. 

- **Primary (Warm Coral):** Used exclusively for high-priority actions, primary buttons, and active navigation states.
- **Secondary (Soft Amber):** Reserved for quantitative quality indicators like star ratings and "Best Match" badges.
- **Surface & Borders:** Interactive elements use a layered dark approach. Surfaces should never be pure black; they utilize a #1A1A22 fill with a #2E2E3A stroke to maintain structural definition in a dark environment.
- **Feedback States:** Success, Info, and Warning banners use low-saturation, deep-toned backgrounds with high-contrast text to ensure they remain secondary to the main content.

## Typography
The system uses **Inter** for its neutral, systematic clarity. 

- **Headlines:** Use Bold (700) or SemiBold (600) weights for restaurant titles and section headers. 
- **AI Narrative:** AI-generated explanations and summaries must be rendered in `body-ai-italic` with a secondary text color (#A0A0B0). This visual distinction separates human-curated data from machine-generated insights.
- **Scale:** On mobile devices, large headlines should scale down to 24px to ensure readability without excessive wrapping.

## Layout & Spacing
This design system employs a **Fluid Grid** model based on a 4px baseline. 

- **Grid:** Use a 12-column grid for desktop and a 4-column grid for mobile.
- **Rhythm:** Vertical spacing between cards should be consistent at `lg` (24px). Internal card padding should be `md` (16px).
- **Safe Areas:** On mobile, a horizontal margin of 20px is required to ensure content does not hug the screen edges.

## Elevation & Depth
Depth is conveyed through **Tonal Layers** and subtle ambient shadows. 

1. **Level 0 (Background):** #0F0F12.
2. **Level 1 (Cards/Panels):** #1A1A22 with a 1px border of #2E2E3A.
3. **Level 2 (Popovers/Modals):** #252530 with a 10% opacity white border and a diffused shadow (0px 8px 24px rgba(0,0,0,0.5)).

**AI Surfaces:** Elements specifically containing AI logic (like the recommendation engine) should use a subtle backdrop-blur (12px) if positioned over images to reinforce the "smart" layer of the interface.

## Shapes
The shape language is modern and "Soft-Industrial." 

- **Default Radius:** Most containers, including restaurant cards and input fields, use a **14px** corner radius.
- **Large Components:** Hero sections or large modal containers use `rounded-xl` (1.5rem / 24px) to feel more approachable.
- **Buttons:** Buttons use `rounded-lg` (1rem / 16px) to maintain a distinct clickable appearance from the square-ish grid.

## Components

- **Buttons:** Primary buttons use the Warm Coral (#E23744) background with White text. Secondary buttons use a transparent background with a #2E2E3A border.
- **Restaurant Cards:** These are the primary atomic unit. They feature a 14px radius, #1A1A22 surface, and a subtle shadow. The restaurant name is always `headline-md`. Ratings are displayed in the top-right corner using the Soft Amber (#F5A623) color.
- **AI "Reasoning" Chips:** Small, semi-transparent pills used to tag why a restaurant was recommended (e.g., "Matches your love for Spicy Food"). These use the `info` color palette.
- **Input Fields:** Search bars should be elongated with a 1px #2E2E3A border. On focus, the border transitions to Primary Coral.
- **Selection Controls:** Checkboxes and Radio buttons use a subtle scale-up animation on hover, utilizing the Primary Coral for the "Checked" state.
- **AI Summary Block:** A specialized component with a 2px left-border of Primary Coral, containing italicized text to signal AI concierge communication.