# claude-code-skills — 35 reusable skills for Claude Code

Working methods packaged as Claude Code [skills](https://code.claude.com/docs/en/skills): how to think
on a hard problem, how to contradict usefully, what to check before sending something to a third party, how to commit,
how to watch long-running work, how to pick a visual direction, and a few tools around documents, audio and calendars.

> The skills are written in **French** (their trigger phrases too, with some English ones). Each one is a single
> `SKILL.md` — a text you can read in two minutes — plus, for a few, a small script.

## Install

```bash
git clone https://github.com/anthohunt/claude-code-skills.git
# a) as a plugin, for one session (skills appear as /work-methods:<name>)
claude --plugin-dir ./claude-code-skills
# b) or copy the ones you want into your own skills folder (they then appear as /<name>)
mkdir -p ~/.claude/skills && cp -r claude-code-skills/skills/think claude-code-skills/skills/adverse ~/.claude/skills/
```

To plug the same skills folder into several Claude accounts or computers, see the companion repository
`claude-code-setup` (`provisionner.py`).

## The skills

**Think and challenge**

| Skill | What it does |
|---|---|
| `think` | A long reflection cycle for a hard problem: frame it, produce competing options, search the web, eliminate by evidence, return one defended recommendation. |
| `adverse` | Launches an agent whose only goal is to break your reasoning, plan or numbers — before a long computation, a publication, an irreversible decision. |
| `honest` | Truth-first mode: verify before asserting, challenge the substance, calibrate certainty (know / think / don't know), no contrarianism for show. |
| `self-reflect` | Unblocks an agent that loops: fresh sub-agents that never saw the failed attempts, a mandatory web search, and a permanent repair of the root cause. |
| `simple` | Explain by what things do rather than by their names; the example comes before the rule. |
| `rattrapage` | Re-explain, standalone, something the user missed while the agent was working alone. |
| `bullet-points` | A summary as concise bullets and nothing else. |

**Check before you act or claim**

| Skill | What it does |
|---|---|
| `confirm-external-send` | Show the exact draft and get an explicit yes before anything leaves the machine (mail, message, form); re-check every quoted fact. |
| `monitor` | A living watch-list file plus a check–act–reschedule loop for a manager agent following background work. |
| `data-sourcing` | Figures with proof: finder agents, an adversarial judge that tries to refute each number, a reliability scale. |
| `audit-loop` | Independent "quality agents" criticise a web app through a real browser; the main agent repairs; repeat until only minor issues remain. |
| `create-account-in-chrome` | Never create accounts in the automation browser: open the exact page in the user's own browser so the password manager captures the credentials. |

**Deliver and design**

| Skill | What it does |
|---|---|
| `streamline` | Cut a page, document or flow to its signal — and make it look professional, not only shorter; count the clicks. |
| `harmony` | Fix layout defects (truncated text, overlaps, misalignment) by looking at a rendered image, never at the code. |
| `format-notion` | A Notion-like layout standard with semantic callout colours (and ready-to-copy CSS). |
| `design-on-the-go` | Iterate on a visual with short feedback and no questions: guess, build, announce in two lines, refresh. |
| `visuel-recherche` | An evolutionary visual tournament (challenger vs champion) driven by a written "theory of what makes it good". |
| `illustrate` | Put a real web image (press screenshot, image search) on a slide, judged on the rendered result. |
| `dashboard` | Build a private one-file web dashboard in a Notion look (`assets/notion.css`), served locally. |
| `brainstorming-design` | Turn a rough idea into a design through one question at a time, 2–3 approaches, and sectioned validation. Derived from superpowers' `brainstorming` (MIT). |

**Organise the work**

| Skill | What it does |
|---|---|
| `commit` | Atomic commits (one intention each), titles that read well in `git log --oneline`, bodies that say why, push verified. |
| `team-agents` | Run parallel agent teams: tasks with dependencies, self-contained prompts, monitoring, shutdown. |
| `add-autonomous-task` / `launch-autonomous-task` | Fix an autonomous task now (goal, verifiable success criteria), launch it later under a `monitor` loop that stops by itself. Pairs with the `taches-autonomes` mod of `claude-code-mods`. |
| `nightshift` | (Windows) Overnight tasks register in a shared registry; the last one to finish powers the machine off. |
| `continue-conversation` | Find and resume a Claude Code conversation that crashed (searches `~/.claude*/projects`, optionally other machines over SSH). |

**Documents, audio, calendar**

| Skill | What it does |
|---|---|
| `analyse-reunion` | A meeting transcript → one structured analysis (summary, decisions, actions, open points), nothing invented. |
| `transcribe-audio` | Audio/video → text with faster-whisper (local) or the Groq Whisper API; optional multi-agent synthesis with an anti-fabrication check. |
| `drive-audio` | Fetch the latest audio file(s) from Google Drive and transcribe them. |
| `sign-docx` | (Windows + Word) Signing workflow where the human sees the document before signing, then PDF export. |
| `collab-docx-edit` | Edit a Drive document the user is also editing: download the live version, patch in place, upload back. |
| `note-agenda` | Add one line to a per-day all-day "À faire" event in Google Calendar. |

**Unity / Meta XR, and disk space**

| Skill | What it does |
|---|---|
| `doc` | Search the official Meta Horizon documentation (local index of the site's `llms.txt`) *before* wiring anything. |
| `debug-xr` | A debugging loop for XR behaviour in Unity: docs first, compare with the SDK's reference prefab, persistent probe, one discriminating run. |
| `disk-clean` | Audit disk space and clean authorised batches on a computer, server or external disk, protecting active projects; includes a read-only inventory script. |

## Requirements by skill

Most skills need nothing but Claude Code. Exceptions: `note-agenda`, `drive-audio`, `collab-docx-edit` use
[`gws`](https://github.com/googleworkspace/cli) (Google Workspace CLI, logged in); `transcribe-audio` needs `ffmpeg` and either
`faster-whisper` (+ an NVIDIA GPU, optional) or a `GROQ_API_KEY` in the environment; `collab-docx-edit` needs `python-docx`;
`illustrate` and `audit-loop` use a Playwright browser tool; `sign-docx` and `nightshift` are Windows-only
(PowerShell; Word for `sign-docx`); `visuel-recherche` uses `puppeteer` for its headless check.

## Not included on purpose

Personal and organisation-specific skills, and these generic ones that live in their own repositories: `mission` (repository
`mission-loop`), `iterative-prompt-tuning` and the `autoresearch-*` skills (repository `la-boucle-methode`).
Skills by other authors are **not redistributed**; install them from their source, mind their licences:
[Anthropic skills](https://github.com/anthropics/skills) (document skills are "all rights reserved"),
[obra/superpowers](https://github.com/obra/superpowers) (MIT),
[addyosmani/agent-skills](https://github.com/addyosmani/agent-skills),
[Imbad0202/academic-research-skills](https://github.com/Imbad0202/academic-research-skills) (`deep-research`; **CC BY-NC**: non-commercial,
incompatible with Apache 2.0).

## Tests

```bash
python3 tests/verifier_skills.py            # every SKILL.md has a valid front matter, no personal path or address
```

## Licences

- Scripts (`*.py`, `*.mjs`, `*.ps1`, `*.sh`): [Apache License 2.0](LICENSE), see [NOTICE](NOTICE).
- The texts of the skills (`SKILL.md`, references) and `assets/notion.css`: [Creative Commons Attribution 4.0](LICENSE-docs).
- `skills/brainstorming-design` is derived from the `brainstorming` skill of obra/superpowers, MIT, Copyright (c) 2025 Jesse Vincent
  (`skills/brainstorming-design/LICENSE-superpowers-MIT`).

---

**Anthony Hunt** · [Project page on ingevision.cloud](https://ingevision.cloud/?lang=en&p=outils-claude-code) · [LinkedIn](https://www.linkedin.com/in/anthony-hunt-3948a9196) · [GitHub profile](https://github.com/anthohunt)
