# MScAC Event Proposals

Working directory for drafting and tracking this MScAC cohort's Social Initiative Fund event proposals.

See [CLAUDE.md](./CLAUDE.md) for the authoring guide, proposal template, budget norms, and funding rules. That guide and workflow were adapted from a prior cohort's proposal repository: https://github.com/davidcagoh/mscac-event-proposals-2026

## Workflow: proposed → approved

Each proposal's `.md` file (and matching `.pdf` once exported for submission) moves through two folders that track its current status:

- **`proposed/`** — drafted and/or submitted, awaiting a decision from the program team.
- **`approved/`** — signed off by the program team. Move the `.md` + `.pdf` pair here once approved.

`proposed/` files are work-in-progress and safe to edit directly; `approved/` files are final and should not be edited — open a new proposal in `proposed/` instead.

Naming convention: `YYMMDD-event-slug.md`, with a matching `.pdf` where a submitted copy exists — see PDF Export below for how to generate it.

## PDF Export

Generate a proposal's `.pdf` from its `.md` with [`scripts/render_proposal_pdf.py`](./scripts/render_proposal_pdf.py):

```
python3 scripts/render_proposal_pdf.py proposed/<file>.md proposed/<file>.pdf
```

Requires Python 3 with `reportlab` installed (`pip install reportlab`). The script only understands the Markdown subset the Proposal Template in `CLAUDE.md` uses (headers, bold labels, bullets, dividers, and a single budget table), so it won't handle a proposal that deviates from that structure. This is unrelated to Claude Code's `document-skills` plugin (the `pdf` skill) — that plugin is for general PDF editing/merging and isn't needed just to run this script.

## Agents

Three project-scoped agents in [.claude/agents/](./.claude/agents/) cover the pipeline, one per stage:

| Agent | Role |
| :---- | :---- |
| [`researcher`](./.claude/agents/researcher.md) | Given an event idea, web-searches for real venues/vendors/pricing and returns 2-3 concrete, costed options that comply with the budget norms and funding rules in `CLAUDE.md`. |
| [`writer`](./.claude/agents/writer.md) | Once an option is agreed on, fills in the proposal template from `CLAUDE.md` and saves it to `proposed/`. |
| [`evaluator`](./.claude/agents/evaluator.md) | Independently checks a proposal in `proposed/` against every rule in `CLAUDE.md` — required sections, budget arithmetic, funding rules, writing guidelines — and returns a ready-to-submit verdict. |

They're scoped to this project only (they live in this repo's `.claude/agents/`, not a global agents directory), so they won't appear or run in other projects.

## Tooling

This repo's `CLAUDE.md` and agent setup are built for [Claude Code](https://claude.com/claude-code). Compatibility with other AI coding tools hasn't been tested.
