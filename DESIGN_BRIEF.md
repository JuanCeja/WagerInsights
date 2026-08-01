# WagerInsights — Design Brief

This document defines the visual identity and design direction for WagerInsights. AI agents (Claude Code, Cursor, etc.) should read this before making any styling changes so the look stays cohesive across sessions.

## Current state

The app is functionally complete but visually generic. It uses shadcn/ui's default dark theme with a purple `--primary` (`#a855f7`) and a teal `--accent`. Components work, the layout is clean, but it doesn't feel distinctive — it could be any SaaS dashboard. Goal of any styling work is to make it feel like a real sports betting product, not a generic admin panel.

## Design direction — sports betting product aesthetic

Reference apps that nail the look (study these, don't clone them):

- **PrizePicks** — purple accent on near-black background, bold typography, confident contrast
- **DraftKings** — orange + green accents, dense layouts, game-card-forward
- **FanDuel** — blue accent, clean spacing, big typography for odds
- **Stake.com / Bet365** — pro-sportsbook vibe, dense data, no wasted space

**What we're going for:** dark base, **single vivid accent color**, generous use of monospace for odds/numbers, big confident typography for key data (odds, balance, payout). Should feel like a product, not a tutorial.

## Color palette

**Use these consistently. Do not introduce new colors without updating this doc first.**

- **Background base:** `#0a0a0f` (near-black, slightly cooler than pure black) or stay with shadcn's current `--background`
- **Surface (cards, dialogs):** one step lighter than background, e.g. `#15151c`
- **Primary accent:** `#a855f7` (purple) — KEEP this. It's already wired through shadcn variables and recharts chart colors. Changing it is a bigger refactor than it looks.
- **Secondary accent:** the teal `--accent` is fine for now but underutilized — consider dropping it or using it strictly for wins/positive states
- **Wins / positive:** green, but muted — not stoplight green. Something like `#22c55e` at reduced opacity, or use the primary purple for "won" badges to keep the palette tight
- **Losses / negative:** red, muted — `#ef4444` at reduced opacity. Avoid bright red anywhere except destructive actions
- **Text primary:** off-white, never pure `#fff`. Around `#fafafa` or `#f4f4f5`
- **Text secondary:** muted gray, e.g. `#a1a1aa` or `#71717a`
- **Borders:** very subtle, e.g. `#27272a` — borders should whisper, not shout

## Typography

- **Sans-serif:** keep the current shadcn default (Inter or similar). Don't introduce a new sans font.
- **Monospace:** add a monospace font for **odds, balance, dollar amounts, and any numeric data**. JetBrains Mono, Fira Code, or IBM Plex Mono are good choices. This is the single biggest visual upgrade available — numbers in monospace immediately read as "data" and gives the app a professional/financial feel.
- **Headings:** bold, larger than current. Page titles should be visually distinct.
- **Sentence case** everywhere except brand name. Never ALL CAPS for body content. ALL CAPS is acceptable only for small ui labels like "WIN RATE" or "BALANCE" in stat cards.

## Layout & spacing

- **Generous whitespace** between major sections. Cards should breathe.
- **Tighter spacing inside data tables and stat cards.** Dense where data lives, spacious where you navigate.
- **Game cards** are the headline component. They should feel like the focal point of the dashboard, not a generic list item. Big teams, big odds, clear "tap me to bet" affordance.
- **Stat cards on MyBets** — odds and balance numbers should be the largest text on the screen. Currently they're competing with labels. Flip the hierarchy.

## Component-specific direction

### Navbar
- Sticky to top, slight dark backdrop blur, clear brand mark on left, user info + balance on right
- Balance should be in monospace, prominent

### Game cards (Dashboard)
- Home team / away team prominent, centered
- Odds in monospace, large, with subtle hover state
- The two bet buttons should feel like distinct choices, not identical buttons

### BetDialog
- Live payout calculation is the star. Big monospace number that updates as the user types.
- The "Analyze Bet" button is a value-add feature — give it some visual weight (subtle gradient or distinct outline) but don't make it the primary CTA. Placing the bet is the primary CTA.

### MyBets stat cards
- Total bets, win rate, net P/L
- Numbers should DOMINATE. Labels should be small uppercase muted gray. The number is the answer; the label is the question.

### Charts (recharts)
- Already using purple `#a855f7` and slate `#475569` — keep this
- Increase font size of axis labels (currently look small)
- Add subtle gridlines (low opacity), not heavy ones
- Tooltip should match the app's surface color, not recharts default white

### Leaderboard
- Top 3 deserve visual distinction — slight highlight on row, maybe a small medal/rank indicator
- Win rate should be the most prominent column visually

### Deposit form
- Stripe Elements already theme-matched to purple/dark — keep this
- The "$50 / $100 / $250" quick-pick buttons could be more prominent
- Success state should feel celebratory, not just "ok done" — slight scale animation, balance counter ticking up, etc.

## Animation & motion

- **Subtle.** No bouncy springs, no extended timing.
- Transitions should be 150-200ms ease for most interactions
- Hover states should be near-instant but visible (background lighten, border accent)
- The "balance updated" moment on deposit success is the one place to invest in a richer animation

## What NOT to do

- No gradients on backgrounds or large surfaces (small accents OK)
- No glassmorphism / blur effects (looks dated)
- No emojis as UI elements (use lucide-react icons if needed)
- No bright neon colors — everything muted/considered
- No multiple accent colors competing for attention — purple is the accent, period
- No fancy fonts — sans + mono is the entire type system
- No carousels, parallax scrolling, or decorative motion
- No light mode for now — dark only

## When in doubt

Ask: "would PrizePicks ship this?" If the answer is no, redesign it. The product is a sports betting tracker — it should look serious and confident, not playful.

## Logo

The app currently has no logo, just the text "WagerInsights" in the navbar. A simple logo mark would significantly upgrade the perceived polish. Direction: minimalist, monochrome (so it works on dark + light), incorporates either a "W" mark or an abstract icon related to betting/data (bar chart, line trend, dice would be too literal). See the bottom of this doc for tools to create it.