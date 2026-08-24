---
name: Azeez Ridwan Studio
colors:
  surface: '#131313'
  surface-dim: '#131313'
  surface-bright: '#3a3939'
  surface-container-lowest: '#0e0e0e'
  surface-container-low: '#1c1b1b'
  surface-container: '#201f1f'
  surface-container-high: '#2a2a2a'
  surface-container-highest: '#353534'
  on-surface: '#e5e2e1'
  on-surface-variant: '#c4c7c8'
  inverse-surface: '#e5e2e1'
  inverse-on-surface: '#313030'
  outline: '#8e9192'
  outline-variant: '#444748'
  surface-tint: '#c6c6c7'
  primary: '#ffffff'
  on-primary: '#2f3131'
  primary-container: '#e2e2e2'
  on-primary-container: '#636565'
  inverse-primary: '#5d5f5f'
  secondary: '#b8c3ff'
  on-secondary: '#002387'
  secondary-container: '#023fd8'
  on-secondary-container: '#b8c3ff'
  tertiary: '#ffffff'
  on-tertiary: '#2f3131'
  tertiary-container: '#e3e2e2'
  on-tertiary-container: '#646464'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#e2e2e2'
  primary-fixed-dim: '#c6c6c7'
  on-primary-fixed: '#1a1c1c'
  on-primary-fixed-variant: '#454747'
  secondary-fixed: '#dde1ff'
  secondary-fixed-dim: '#b8c3ff'
  on-secondary-fixed: '#001355'
  on-secondary-fixed-variant: '#0035bd'
  tertiary-fixed: '#e3e2e2'
  tertiary-fixed-dim: '#c7c6c6'
  on-tertiary-fixed: '#1a1c1c'
  on-tertiary-fixed-variant: '#464747'
  background: '#131313'
  on-background: '#e5e2e1'
  surface-variant: '#353534'
typography:
  display-lg:
    fontFamily: Geist
    fontSize: 80px
    fontWeight: '800'
    lineHeight: '1.0'
    letterSpacing: -0.04em
  display-sm:
    fontFamily: Geist
    fontSize: 48px
    fontWeight: '700'
    lineHeight: '1.1'
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Geist
    fontSize: 32px
    fontWeight: '600'
    lineHeight: '1.2'
    letterSpacing: -0.01em
  headline-lg-mobile:
    fontFamily: Geist
    fontSize: 24px
    fontWeight: '600'
    lineHeight: '1.2'
    letterSpacing: -0.01em
  body-lg:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '400'
    lineHeight: '1.6'
    letterSpacing: 0.01em
  body-md:
    fontFamily: Inter
    fontSize: 15px
    fontWeight: '400'
    lineHeight: '1.5'
    letterSpacing: 0.01em
  label-mono:
    fontFamily: JetBrains Mono
    fontSize: 12px
    fontWeight: '500'
    lineHeight: '1.0'
    letterSpacing: 0.08em
rounded:
  sm: 0.125rem
  DEFAULT: 0.25rem
  md: 0.375rem
  lg: 0.5rem
  xl: 0.75rem
  full: 9999px
spacing:
  unit: 8px
  container-max: 1440px
  gutter: 24px
  margin-desktop: 64px
  margin-mobile: 20px
  section-gap: 160px
---

## Brand & Style

The design system is built for a high-end digital technology studio, merging the precision of modern engineering with the editorial sophistication of a creative agency. The visual narrative is defined by "Technical Minimalism"—a style that prioritizes clarity, structural integrity, and expansive negative space to evoke a premium, authoritative atmosphere.

The emotional response should be one of confidence and technological mastery. By utilizing a monochromatic foundation with high-contrast typography and subtle glassmorphism, the UI mirrors the sleek aesthetic of professional developer tools while maintaining the artistic flair of an elite design house.

**Core Principles:**
- **Reductionist:** If an element does not serve a functional or structural purpose, it is removed.
- **Architectural:** Layouts are built on rigorous grids, favoring asymmetric balance over centered simplicity.
- **Kinetic:** The interface feels alive through high-precision micro-interactions and smooth, purposeful transitions.

## Colors

The palette is rooted in a deep, monochromatic spectrum to create a sense of infinite depth and focus. 

- **Primary (Off-white):** Used exclusively for high-priority typography and essential UI triggers.
- **Secondary (Electric Blue):** A precise, high-saturation accent used sparingly for active states, notifications, or specific data highlights.
- **Neutral (Deep Black/Graphite):** The foundation of the system. Backgrounds utilize `#0A0A0A`, while containers and surfaces use `#111111`.
- **Muted Silver:** Reserved for secondary metadata, labels, and inactive iconography to maintain a clear hierarchy without visual noise.

Surface colors should be applied in layers: the furthest back is the darkest, with each interactive layer becoming slightly lighter or gaining a fine `#242424` border to define its bounds.

## Typography

The typography system is designed to be impactful and technical. 

- **Headlines:** Use **Geist** for its clean, geometric, and developer-centric aesthetic. Large "Display" styles should always be uppercase with tight letter spacing to create a rhythmic, block-like architectural feel.
- **Body:** Use **Inter** for its neutral, highly legible characteristics. Increase letter spacing slightly for body copy to enhance the "editorial" feel and prevent text from feeling cramped against dark backgrounds.
- **Metadata/Labels:** Use **JetBrains Mono** for small labels, tags, and code snippets. This reinforces the "Digital Studio" brand, signaling technical proficiency.

Scale typography aggressively; the contrast between massive display titles and small, precise mono labels is a core feature of the design system.

## Layout & Spacing

The layout philosophy follows a **12-column fluid grid** with strict adherence to a modular 8px scale. 

**Key Layout Rules:**
- **Asymmetry:** Avoid perfectly centered compositions. Use "offset" layouts where headers occupy 4 columns and content occupies 8 columns to create visual interest.
- **Negative Space:** Use `section-gap` (160px) between major content blocks. Whitespace is treated as a design element, not "empty" space.
- **Margins:** Desktop margins are intentionally wide (64px) to frame content like a gallery piece. 
- **Adaptation:** On tablet, reduce margins to 32px. On mobile, collapse to a single column with 20px margins, but maintain the uppercase impact of headlines by utilizing the `headline-lg-mobile` tokens.

## Elevation & Depth

This design system avoids traditional shadows in favor of **Tonal Layering** and **Fine Outlines**. 

- **Base Layer:** `#0A0A0A` (Global background).
- **Surface Layer:** `#111111` (Cards, Modals, Sections).
- **Definition:** Elements are separated by 1px solid borders in `#242424`. This creates a "blueprint" or "schematic" feel that aligns with the technology studio theme.
- **Interaction Depth:** Upon hover, elements may transition their border color to `#A1A1A1` or apply a subtle background tint of `#1A1A1A`. 
- **Glassmorphism:** Use only for persistent navigation bars. Apply a `backdrop-filter: blur(12px)` with a semi-transparent background (`rgba(10, 10, 10, 0.7)`).

## Shapes

The shape language is "Soft-Technical." 

Edges are primarily sharp or minimally rounded to maintain a serious, professional tone. A `0.25rem` (4px) radius is the standard for cards and buttons, providing just enough softness to feel modern without losing the precision of a grid-based system. 

Large-scale containers and buttons should never be pill-shaped; they must remain rectangular to uphold the architectural integrity of the editorial grid.

## Components

### Buttons
- **Primary:** Solid `#F5F5F5` background with `#0A0A0A` text. No border. Uppercase mono-label.
- **Secondary:** Transparent background with 1px border in `#242424`. Text in `#F5F5F5`.
- **Interaction:** On hover, buttons should have a slight "lift" effect or a border-color shift. No heavy easing; use `cubic-bezier(0.16, 1, 0.3, 1)` for a "snappy" high-end feel.

### Cards
- **Construction:** Background `#111111`, Border 1px solid `#242424`.
- **Content:** Generous internal padding (32px). Use the `label-mono` for category tags at the top left.
- **Hover:** The border transitions to `#A1A1A1`.

### Input Fields
- **Style:** Underline only or minimal 1px border. Background should be slightly darker than the surface layer. 
- **Focus:** The underline or border transitions to the Electric Blue accent.

### Lists
- Use horizontal dividers (`#242424`) between items. 
- List items should have a significant height (64px+) with text vertically centered to maintain the expansive spacing narrative.

### Studio Specifics: Project Teasers
- Project previews should use high-contrast imagery or grayscale renders with an "overlay" effect that reveals project metadata only on hover.