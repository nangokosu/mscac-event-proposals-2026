# MScAC Initiative Budget Proposal — Authoring Guide

## What This Directory Is

This directory contains budget proposals for the MScAC (Masters of Science in Applied Computing) Social Initiative Fund. Each proposal requests reimbursement for a cohort social event.

## Reference: Source Format & Example Proposals

This authoring guide, its template, and its workflow rules were adapted from a prior cohort's proposal repository:

**https://github.com/davidcagoh/mscac-event-proposals-2026**

This is a new cohort with no proposal history of its own yet, so when a worked example is useful (seeing a fully filled-out proposal, checking how a past event structured its budget table, etc.), fetch one from that repo's `past-proposals/` directory rather than inventing one, e.g.:

```
https://raw.githubusercontent.com/davidcagoh/mscac-event-proposals-2026/master/past-proposals/260122-wellness-cafe.md
```

The repo's `past-proposals/` listing (fetchable via `https://api.github.com/repos/davidcagoh/mscac-event-proposals-2026/git/trees/master?recursive=1`) covers a range of event types — trivia nights, watch parties, dinners, recurring series — useful as precedent for format and budget scale.

## Workflow: proposed → approved

Proposals move through two folders that track their current status:

- **`proposed/`** — a proposal's `.md` file (and matching `.pdf` once exported for submission) lives here from first draft through submission, while awaiting a decision from the program team.
- **`approved/`** — once the program team signs off, move the `.md` + `.pdf` pair here. This becomes this cohort's own growing set of precedent/reference proposals over time.

Files in `proposed/` are work-in-progress: edit them directly as the plan evolves — updating the budget, activity plan, or any other section in place is expected. Once a file is moved into `approved/`, it is the final, signed-off record and must not be edited. If something needs to change after approval, open a new proposal in `proposed/` rather than editing the approved file.

Naming convention (matches the source repo): `YYMMDD-event-slug.md`, with a matching `.pdf` where a submitted copy exists.

## Proposal Template

```markdown
## **MScAC Initiative Budget Proposal**

**Event:** [Event Name]
**Date:** [Day of week], [Date], [Start Time] to [End Time]
**Venue:** [Room / Location]
**Estimated Attendance:** [Number] [players/students/attendees][+ optional spectator note]

---

### **Purpose**

[2–4 sentences. Hit these beats in order:
1. What social/community goal this serves (bonding, break from academics, camaraderie)
2. Why this particular format is well-suited to that goal
3. Evidence of demand (poll results, prior interest, recurring ask)]

### **Event Components**

[Break the event into named time blocks or activity tracks. For each block:]

**[Block Name] ([Start] – [End]):**

* [Bullet describing what happens, who facilitates, what materials/space are used]
* [Sub-bullet for specifics: format variants, inclusivity notes, logistics]

[Repeat for each block. At minimum cover: the main activity, food/refreshments, and any social/wrap-up phase.]

### **Budget Breakdown**

| Item Description | [Quantity] | Estimated Cost | Per-Person Estimate |
| :---- | :---- | :---- | :---- |
| **[Category]:** [Detail] | [Qty or "For N people"] | $[amount] | $[amount ÷ attendance] |
| **[Category]:** [Detail] | [Qty or "Bulk"] | $[amount] | $[amount ÷ attendance] |
| **[Category]:** [Detail] | [Qty] | $[amount] | $[amount ÷ attendance] |

---

### **RSVP Plan**

* **Interest Polling:** [How initial interest was gauged — Discord poll, cohort form, etc. Include numbers if available.]
* **Preference Tracking:** [How final RSVPs will be collected (Partiful, Google Form, etc.) and what preference questions will be asked.]
* **Dietary Needs:** [How dietary restrictions will be collected and accommodated.]

---

### **Other Next Steps**

* **[Category]:** [Specific action item with owner or deadline if known]
* **Reporting:** Submit all itemized receipts, final attendee list, and invitation for reimbursement. (ESSENTIAL)

**Total Budget Requested: $[total]**
```

---

## Required Inputs Checklist

Collect all of these before writing. Do not start drafting until every item is answered.

| # | Question | Notes |
| :-- | :---- | :---- |
| 1 | Event name | |
| 2 | Date(s) and day(s) of week | For series: list all dates |
| 3 | Start and end time | |
| 4 | Venue | Room number or external location |
| 5 | Expected attendance | Per session if recurring. Always a range (e.g. "15–20"), never a single number |
| 6 | Budget per line item | User decides; see norms below |
| 7 | Student organizer names | First names are sufficient |
| 8 | RSVP method | Discord poll, Partiful, Google Form, etc. |
| 9 | Equipment/materials | What's owned vs. what needs purchasing |
| 10 | Any dietary or accessibility considerations | Collect even if "standard" |

---

## Budget Norms

- Past single-event proposals (prior cohort) ranged **$800–$875** for ~20–40 attendees.
- A rough rule of thumb from past events: **~$35–40 per head** covers catering + refreshments + supplies comfortably.
- The user decides the per-line-item budget split — do not invent numbers. Ask if not provided.
- Round line items to the nearest $5 or $25. The table total must match **Total Budget Requested** exactly.

---

## Funding Rules

- **No alcohol** — any beverage line item must be explicitly non-alcoholic.
- **External venues are allowed** if the event is a dedicated cohort outing (e.g. a restaurant dinner, escape room, bowling). On-campus room bookings (MScAC Room 9014/9016) are the default.
- Equipment purchases are acceptable when justified (e.g. a board game for a recurring series). One-off consumable supplies (plates, napkins, printing) are standard.

---

## Submission

- **Format:** PDF
- **Recipient:** MScAC program team staff email
- **Deadline:** At least **2 weeks before the event date** (or first session date for a series)

### Generating the PDF

Run `scripts/render_proposal_pdf.py` to turn a proposal's `.md` file into its matching `.pdf`:

```
python3 scripts/render_proposal_pdf.py proposed/<file>.md proposed/<file>.pdf
```

Requires Python 3 with `reportlab` installed (`pip install reportlab`). The script only understands the Markdown subset the Proposal Template above uses (H2/H3 headers, `**bold**`, `* ` bullets, `---` dividers, and a single pipe table) — it is not a general Markdown-to-PDF converter, so it won't handle a proposal that deviates from the template's structure.

This is separate from Claude Code's official `document-skills` plugin (the `pdf` skill, `anthropics/skills` marketplace): that plugin is a general-purpose tool for editing, merging, or extracting from arbitrary PDFs, and is not required just to regenerate a proposal's PDF from its Markdown — the committed script handles that directly with no plugin dependency.

---

## Writing Guidelines

### Voice and Tone

- Professional but warm — this is a student community proposal, not a corporate memo.
- Active voice. Avoid passive constructions like "food will be provided by vendors."
- Confident: state what *will* happen, not what you *hope* might happen.

### Purpose Section

- Lead with the community value, not the activity itself.
- Reference concrete evidence of demand (poll votes, prior event attendance, Discord reactions) when available.
- One or two sentences is too thin; four or more is too long. Aim for three.

### Attendance Estimates

- State attendance as a range (e.g. "15–20 students"), never a single number — in the header's **Estimated Attendance** field and everywhere else a headcount appears (interest-poll results, RSVP figures, budget Quantity assumptions).
- A single-number figure from elsewhere (e.g. "19 students responded yes" in a poll) must be restated to match the stated range, not left as a raw count that falls inside or outside it inconsistently.

### Event Components

- Use named time blocks with times in parentheses: **Dinner & Social (6:00 PM – 7:00 PM):**
- Include inclusivity notes — dual-track formats, beginner-friendly options, dietary accommodation.
- Name the student leads or facilitators by first name when known.
- Be specific about logistics: number of tables, equipment sources, tech setup, delivery times.

### Budget Table

- Bold the category label, then describe the specific item after the colon.
- Include a Quantity column when items scale by headcount or units.
- Round to the nearest $5 or $25 for estimates.
- The table total must match the **Total Budget Requested** line exactly.
- Common line items: Main Catering, Refreshments (beverages + snacks), Supplies (disposables, printing), Equipment (if renting/purchasing).
- Always include a **Per-Person Estimate** column: each line item's Estimated Cost divided by the attendance count it's priced for (or by Quantity, when the item scales per head), to the nearest cent.

### RSVP Plan

- Always include how dietary restrictions will be collected — this signals responsible planning to reviewers.
- Reference the platform (Partiful, cohort form, Discord poll) by name.
- For multi-session events (recurring nights), note how RSVPs will be tracked across sessions.

### Next Steps

- The reimbursement line is mandatory and must appear last.
- Every other bullet should be a concrete action, not a vague intention.
- Assign an owner or deadline where possible.

### Multi-Session Events

When proposing a recurring series (e.g. weekly nights over several weeks):

- State the full date range and per-session frequency upfront in the header.
- Show a per-session budget and a total series budget.
- Note how consistency across sessions will be maintained (same venue, same format, same organizers).
- The Purpose section should explain the value of *continuity* — community that builds week over week.
