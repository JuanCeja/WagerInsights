# WagerInsights — Project Handoff & Continuation

I'm Juan, continuing work on **WagerInsights**, a full-stack virtual sports betting tracker I built as a portfolio piece for new-grad/early-career SWE job applications. It's **fully deployed to production** at `https://wagerinsights.app` and I've been iterating on it across many sessions. This prompt re-anchors you to exactly where things stand.

## Live URLs

- **Frontend:** `https://wagerinsights.app` (Vercel, custom domain via Cloudflare)
- **Backend:** `https://wagerinsights-api.onrender.com` (Render, with `/docs` available)
- **Repo:** `https://github.com/JuanCeja/WagerInsights`
- **Demo account:** `juan_admin_prod` (admin user — I'll give the password when needed)

## The Stack

**Backend** (Python, deployed on Render):

- FastAPI + SQLAlchemy + Alembic
- PostgreSQL (managed Postgres on Render in production; local Postgres in dev)
- JWT auth via OAuth2PasswordRequestForm + bcrypt
- The Odds API integration (live game odds across 10 sports)
- APScheduler (auto-sync games every 12hr, auto-settle bets every 1hr)
- Anthropic API integration with web_search tool (Claude Haiku for the bet analyzer)
- Stripe SDK (PaymentIntents flow, test mode)
- Project at `C:\Users\jmc34\OneDrive\Desktop\WagerInsights\backend\`
- Directory structure:
  - `app/main.py` — FastAPI app, CORS middleware, scheduler init
  - `app/auth.py` — JWT logic, `get_current_user`, `get_admin_user`
  - `app/models.py` — User, Game, Bet, Deposit
  - `app/schemas.py` — all Pydantic schemas
  - `app/crud.py` — DB query functions
  - `app/database.py` — engine + session setup
  - `app/routers/` — auth, users, bets, games, deposits, admin
  - `app/api_clients/` — odds_api_client, anthropic_client, stripe_client
  - `app/utils/odds_parser.py` — Odds API response → DB model mapper
  - `alembic/versions/` — migration history

**Frontend** (deployed on Vercel):

- Vite + React (plain JavaScript, not TypeScript) + Tailwind v4 (`@tailwindcss/vite`) + `@tailwindcss/typography` plugin
- shadcn/ui (Radix-based, Nova preset)
- React Router (BrowserRouter)
- Axios for HTTP
- recharts for charts
- react-markdown for AI analyzer output
- `@stripe/stripe-js` + `@stripe/react-stripe-js`
- `@/` path alias
- Dark theme: dark mode on, purple `--primary` (`#a855f7`), teal `--accent` via shadcn CSS variables
- Pages: Dashboard, Login, Register, MyBets, Leaderboard, Deposit
- Components: Navbar, BetDialog, DepositForm, GameCard, ProtectedRoute
- Services (one per resource): `authService`, `betsService`, `gamesService`, `userService`, `leaderBoardService`, `depositsService`
- Context: `UserContext` provides `user` + `refreshUser()` globally

## Database Schema

- **users**: id, email, username, hashed_password, balance (default 1000.0), is_admin (default False, server_default sa.false()), created_at, updated_at
- **games**: id, sport, home_team, away_team, home_team_odds, away_team_odds, game_date, status (upcoming/completed/expired), winner (home/away/null), external_api_id (unique, from Odds API), created_at
- **bets**: id, user_id (FK), game_id (FK), bet_type (home/away), bet_amount, odds_at_bet, potential_payout, status (pending/won/lost), created_at
- **deposits**: id, user_id (FK), amount, stripe_payment_intent_id (unique — idempotency guard), status (succeeded), created_at

## Features (all complete)

**Auth & Users**

- JWT auth with refresh-on-action via UserContext
- Login, Register (auto-login after register), ProtectedRoute for gated pages
- `is_admin` boolean controls access to `/admin/*` endpoints via `get_admin_user` dependency

**Dashboard**

- Public page (logged-out visitors can browse; bet buttons redirect to login)
- Sport filter dropdown (shadcn Select)
- Game cards with home/away odds + bet buttons
- BetDialog with live payout calculation (American odds), bet placement, shadcn Sonner toast on success

**My Bets**

- Bet history with nested game data (`joinedload` on the backend — N+1 fix)
- Status tabs: All/Pending/Won/Lost (shadcn Tabs)
- Stats cards: total bets, total wagered, win rate, net P/L
- **Win/Loss pie chart** (recharts) — purple/slate, no stoplight colors
- **Balance over time line chart** (recharts) — running balance built via `.reduce()` from sorted settled bets, seeded with `user.created_at` and `STARTING_BALANCE=1000`. Uses `bet.game.game_date` as the timestamp (known limitation: same-kickoff-time games collide on the X-axis; TODO is a `game.completed_at` column from Odds API completion time)

**Leaderboard**

- Public page, ranked list of users
- Backend uses a single aggregate `GROUP BY` query with conditional `func.count(case(...))` to avoid N+1 across users. Win rate computed in Python after the query; zero-bet users handled with a zero-guard
- Tiebreaker: total bets (not balance) — defensible as "more proven track record"
- Lean schema `LeaderBoardEntry` (no PII leak — username, balance, win_rate, total_bets only)

**AI Bet Analyzer** (the V2 headline feature)

- Backend-only Anthropic API call (key in env, never frontend) — `POST /bets/analyze`
- Uses Claude Haiku with `web_search_20250305` tool, `max_uses=3`
- Prompt includes recalibrated rubric (5/10 = fairly priced, not a warning; full balanced range)
- Response parsing handles multi-text-block content via `"".join()` of all text blocks (because tool use interleaves text + tool blocks)
- Frontend: Analyze button on BetDialog, three-state UI (loading/error/data), `react-markdown` renders the markdown with `prose prose-invert` styling
- Cost: ~$0.05/call with search enabled; $10/month cap on Anthropic console

**Stripe Deposits**

- Test mode only. PCI scope avoided — card data stays in Stripe's iframe via `<PaymentElement>`
- Two-endpoint flow: `POST /deposits/create-intent` creates a PaymentIntent and returns `client_secret`; `POST /deposits/confirm` verifies with Stripe directly and credits balance
- Backend re-verifies PaymentIntent status with Stripe before crediting (don't trust frontend)
- Four verification checks on confirm: status=succeeded, metadata.user_id match (int cast for Stripe's string), idempotency lookup, then atomic credit
- Transactional integrity: balance update + deposit row INSERT in one session, single `db.commit()`
- Frontend: multi-stage `Deposit.jsx` (amount/card/processing/success), `<Elements>` provider wraps `<DepositForm>` (must be separate components because `useStripe`/`useElements` only work inside the provider — same Context pattern as UserContext)
- Stripe Elements theme-matched to the app (purple primary, dark slate background)

**Admin Router (RBAC-protected)**

- `get_admin_user` dependency chains on `get_current_user` — JWT check, then `is_admin` check
- Endpoints: sync games (single sport), bulk_sync_games, settle_game_and_bets, auto_settle_games, available_sports, cleanup-stale-games
- Returns 401 if no JWT, 403 if non-admin

## Architectural decisions worth knowing (locked-in lessons)

- **Backend-only third-party API calls** — Anthropic, Stripe secret, Odds API all server-side. Frontend only ever gets safe references (publishable keys, client_secrets, IDs)
- **Single aggregate query, finish math in Python** — leaderboard uses one GROUP BY with conditional COUNT; division + sort in Python (cheap, free, avoids SQL divide-by-zero gymnastics). Avoids N+1
- **N+1 generally** — `joinedload` on `BetResponse` for nested game data
- **f-strings are evaluated where they're written** — prompts must be built INSIDE functions, not at module level (variables don't exist there)
- **Three state pieces per fetch** — loading, output, error. Not two
- **`useEffect([])` for fetch-on-mount** — omitting deps causes infinite loops via setState
- **React Context Provider/Consumer pattern** — UserContext for user state app-wide; same shape used by Stripe's `<Elements>` wrapping `<DepositForm>`
- **NOT NULL columns added to populated tables need `server_default` in the migration**, not just `default` in the model (Python default vs server default are separate things)
- **Vite env vars need `VITE_` prefix** — security feature, not convention
- **CORS is backend-defined, env-driven, multi-origin** via `CORS_ALLOWED_ORIGINS` comma-separated
- **SPA routing on Vercel** — `vercel.json` rewrites `/(.*)` → `/` so React Router handles client-side routes
- **Production Postgres bootstrapped with `Base.metadata.create_all()` + `alembic stamp head`** because original migrations never had a "create base tables" step
- **Case-sensitive import paths** — works on Windows local, breaks on Linux deployments (caught this multiple times)

## How I want you to work with me

- **Socratic / hands-on**. I write the code first; you review. Before we build something, ask me how I think we should approach it. If I'm wrong, correct me and explain WHY — don't just give me the answer
- **Don't dump full solutions unprompted.** Hints first, let me try, then walk me through if I'm stuck
- **Don't invent or guess at my code.** If you need to see a file before suggesting edits, ask me to paste it. Don't make up imports, function signatures, or anything that's not in front of you
- **Git commit message after every meaningful change**, small and frequent, with the file path
- **Journal entries when we finish a concept/feature**, in my format: a date-stamped title that includes the relevant file names, "What I built" / Concepts / Interview angle / Takeaway sections. **Code-first** in every concept block — show the code, *then* explain it (not the other way around). Code blocks get the file path noted above them
- **I care more about technical/architectural depth than CSS/styling.** Keep styling explanations brief unless I ask

## Future ideas (not scheduled, but on the radar)

- **Dark theme overhaul** matching PrizePicks/DraftKings/FanDuel aesthetic (dark base + single vivid accent — dedicated session, not a quick task)
- **Free sports news API on Dashboard** — show current sports headlines alongside games
- **Stripe webhooks for production-grade payment confirmation** (currently using direct-confirmation, fine for portfolio)
- **`game.completed_at` column** populated from Odds API's actual completion time (would fix the balance chart's same-kickoff-time collision issue)
- **Citations rendered in the AI analyzer output** (currently shown as inline prose; could be clickable source links pulled from `message.content[*].citations`)
- **Demo account auto-reset** so recruiters always land on a fresh state