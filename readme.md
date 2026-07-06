# Date-Night Agent 🍷

An AI agent that plans an entire restaurant date — vibe, reservations, and backup plan included — so you're not stuck scrolling Google Maps 20 minutes before you're supposed to leave.

## Problem

"Where should we go?" is one of the most common, low-stakes-but-annoying decisions in dating and relationships. Generic search tools return a list of restaurants; they don't understand *vibe*, don't account for what happens if your first choice is booked, and don't help you look like you actually planned something thoughtful.

## Core Features

### 1. Vibe-Based Discovery
- User describes the date in plain language: e.g. *"romantic but not stuffy,"* *"impressive but not try-hard,"* *"casual first date, low pressure."*
- Instead of matching on star rating alone, the agent reads actual review text to infer atmosphere — candlelight and quiet corners signal romantic; "special occasion only" or "stuffy" language gets filtered out for casual requests.
- Filters by cuisine, budget, and distance/neighborhood.

### 2. Smart Restaurant Search
- Uses structured place data (name, address, rating, hours, photos, review text) to generate a real, ranked shortlist — not a guess.
- Cross-references recent web info for anything place data might miss: recent closures, chef changes, price shifts.

### 3. Primary Pick + Backup Plan
- Recommends one top choice **and** a nearby backup with a similar vibe.
- If the first spot is booked, too loud, or just doesn't feel right on arrival, there's already a fallback — no scrambling.

### 4. Reservation Guidance
- Checks whether a restaurant takes reservations and how (OpenTable, Resy, phone-only).
- Because live table availability isn't something the agent can query directly, it's upfront about this: it recommends and links to book, rather than falsely confirming a reservation.

### 5. Talking Points
- Surfaces a line or two of context about the restaurant — what it's known for, its story, a standout dish — so you can casually mention it and look like you know the place, not like you just searched "date night restaurants near me."

### 6. Visual Map Output
- Displays the primary pick and backup on an interactive map with notes, so the plan is easy to see and share, not just a wall of text.

## What This Agent Does *Not* Do (by design)
- Does **not** fabricate live table availability — it links out to book rather than pretending to confirm a reservation.
- Does **not** rely on star ratings alone — vibe is inferred from actual review language.
- Does **not** recommend just one option — always pairs a primary with a backup.

## Example Input → Output

**Input:**
> "Planning a second date, want something romantic but not too formal, Italian if possible, within 15 minutes of downtown, budget $$–$$$."

**Output:**
> - **Primary pick:** [Restaurant name] — known for candlelit patio seating and handmade pasta; reservations via Resy, book at least 2 days ahead.
> - **Backup:** [Restaurant name], 6 minutes away — similar cozy vibe, walk-ins usually fine on weeknights.
> - Talking point: the chef trained in Bologna and the restaurant's tiramisu is made table-side.

## Tools/Data Sources Used
- **Places search** — restaurant discovery, ratings, reviews, hours, location
- **Web search** — reservation systems, recent news, extra context
- **Map display** — visual presentation of primary + backup picks

## Status
Concept + architecture defined. Prototype not yet built.