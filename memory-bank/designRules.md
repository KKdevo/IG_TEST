# Design Rules - Avoiding "Vibe Coded" Design

*Source: Aftermark AI Vibe Coded Websites Report*

This document serves as the design quality checklist for all HTML/CSS output in this project. Every generated report, calendar, or web view must adhere to these principles.

---

## Core Design Principles

### Spacing System
- Use **8-point spacing** system consistently
- Predictable rhythm: 8px, 16px, 24px, 32px, 48px, 64px increments
- No random spacing values

### Typography
- **Heading Font:** Instrument Serif
- **Body Font:** Manrope
- Consistent type ramp with logical hierarchy
- Body text: never overly bold or overly light
- Consistent spacing between text blocks

### Color Palette
- Primary Background: #FAF9F7
- Secondary Background: #FFFFFF
- Primary Text: #1A1A1A
- Secondary Text: #6B6B6B
- Muted Text: #9A9A9A
- Accent: #2D2D2D
- Warm Accent: #C4A484
- Borders: #E8E6E3

### Border Radius Standard
- Cards: 16px
- Large containers: 20px
- Buttons: 6px (small), 100px (pill)
- No mixing of random radiuses

---

## Visual Red Flags to AVOID

### 1. The Purple Problem ❌
- Random purple gradient hero sections
- Neon purple text shadows
- Purple hover fills on buttons
- Purple accents without brand justification

### 2. Sparkle Overload ❌
- One sparkle = maybe fine
- Twenty sparkles = vibe coded diagnosis
- Sparkles in hero text, buttons, pricing cards

### 3. Excessive Hover Animations ❌
- Cards lifting up aggressively
- Cards rotating slightly
- Hover shadows like flashlight under mouse
- Bouncing buttons

### 4. Emoji as UI ❌
- Emojis instead of icons
- Emojis inside headings
- Emojis on buttons
- Emoji overload signals rushed UI

### 5. Fake Testimonials ❌
- AI-generated avatars
- Generic names like "Sarah P."
- Generic quotes like "Helped me so much"
- No job title or link

### 6. Broken Social Icons ❌
- Instagram linking to "#"
- Twitter linking to twitter.com
- LinkedIn opening 404

### 7. Massive Icons + Tiny Text ❌
- Creates inverted visual hierarchy
- Feels cheap and rushed

### 8. Generic Font Usage ❌
Problems arise when:
- Heading weight too thick
- Body text too light
- Line height inconsistent
- No spacing rhythm

### 9. Semi-Transparent Headers ❌
- Blur backgrounds that interact poorly with scroll
- Low contrast text
- Thin borders hard to see

### 10. Bad Animations ❌
- Lottie animations that don't match brand
- Wiggle effects
- Bounce overshoot
- Cards popping with no easing
- Scroll animations that stutter

---

## Structural Red Flags to AVOID

### 1. No Loading States ❌
- Always add loading indicators
- Buttons should show state during async
- Use skeleton screens for data loading

### 2. Inconsistent Components ❌
- Button sizes should be uniform
- Padding must be consistent
- Text alignment shouldn't randomly switch
- Container widths should be predictable

### 3. Misaligned Grids ❌
- Cards must align
- Even spacing throughout
- No margins collapsing
- Sticky elements shouldn't drift

### 4. Mixed Border Radiuses ❌
- Don't mix 4px, 12px, 32px randomly
- Choose 1-2 radius values and stick to them

---

## Content Red Flags to AVOID

### 1. Off Copyright Text ❌
- "All right reversed" (typo)
- "Copyright 2024 YourSiteName"
- "Made by Me"

### 2. Meaningless Taglines ❌
- "Build your dreams"
- "Launch faster"
- "Create without limits"
- "The future of something"

### 3. Overloaded Hero Sections ❌
Don't combine all at once:
- Sparkle + Emoji + Gradient + Multiple buttons + Animated card + Background image + Shadow

---

## Technical Requirements

### 1. Meta Tags Required ✅
- OpenGraph image
- Meaningful page title
- Description meta tag

### 2. Mobile First ✅
- No text overflowing
- Cards stack properly
- Buttons properly sized
- Layout doesn't collapse

### 3. Interactive Elements Must Work ✅
- Carousels must slide
- Tabs must switch
- Accordions must open/close
- Modals must close
- All buttons must respond

---

## Pre-Ship Checklist

Before generating final HTML, verify:

**Brand & Visuals:**
- [ ] No purple gradients (unless brand requires)
- [ ] No sparkle emoji overload
- [ ] Subtle hover animations only
- [ ] No emojis in headings
- [ ] Consistent font usage
- [ ] Standard border radiuses

**UX & Layout:**
- [ ] Consistent component sizes
- [ ] Loading states present
- [ ] Grid alignment is perfect
- [ ] 8pt spacing rhythm

**Technical:**
- [ ] OG image set
- [ ] Proper page title
- [ ] Mobile layout tested
- [ ] All buttons functional
- [ ] No placeholder text

**Copy:**
- [ ] Specific, not generic taglines
- [ ] Correct copyright text
- [ ] Clear value proposition

---

## LLM Design Prompt

When generating UI, apply these rules:

> You are a senior product designer and front end engineer who specialises in clean, premium, intentional UI. Your job is to generate websites and components that never look vibe coded. Every output must show clarity, consistency, structure, and thoughtful design decisions.
>
> Begin every project by establishing a strict 8-point spacing rhythm. Typography must follow a clear system with one font pair. Color choices should feel disciplined - small palette, consistent usage. All components must share the same design language (border radius, shadow style, padding logic).
>
> Interactions and animations must be subtle. Layout should follow a proper grid. Loading states are required. Copy must be specific and grounded. Technical fundamentals must be complete (meta tags, responsive design, functional links).
>
> The final result should feel like something shipped by a mature product team. Intention in every choice, clarity in every layout, calm and confident design voice.

---

*This document informs all HTML generation in the templates/ folder.*
