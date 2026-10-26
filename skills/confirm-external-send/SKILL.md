---
name: confirm-external-send
description: Use BEFORE any outbound communication that leaves the local environment — email, chat message (Discord/Slack/WhatsApp), SMS, postal letter, API call to a third party that delivers content, file upload to an external party, administrative form submission. Requires explicit user confirmation of the exact final content AND verification of any data from files or scrapes referenced in the message. Never reuse a prior "go-ahead" — each send needs its own confirmation.
---

# Confirm before external send

## When this skill applies

Any action where the **content leaves the user's environment** and reaches a third party. Reversibility is not the test — visibility is. If a stranger could read it after the call, the rule applies.

**In scope:**
- E-mail send (SMTP, or an IMAP APPEND if the recipient sees it; web mailboxes of administrations, employers, insurers)
- Discord/Slack/SMS/WhatsApp messages (bot or user)
- Postal letter generation followed by physical mailing
- API calls that post on behalf of the user or of someone they act for (administrative forms, banks, insurers)
- Public uploads (gist, pastebin, diagram renderers, public shares of a drive)

**Out of scope:**
- Local file writes
- Reading external sites
- Internal channels the user fully controls (own server, own bot) — still confirm if the message reaches a stakeholder they would not expect

## The rule

```
Draft → Show the EXACT final content (subject, body, recipients, sender, attachments) →
Verify sourced facts → ASK explicitly → WAIT for explicit yes →
Only then send.
```

A user saying "go ahead" earlier on a similar task does **not** authorize a new send. Each draft is its own gate.

## What "explicit confirmation" means

| Acceptable | Not acceptable |
|---|---|
| "OK envoie", "c'est parfait, envoie", "go", "send it" | Silence after the draft |
| "yes, that one", "valide" | "looks good" without an explicit verb (re-ask) |
| Affirmative reply to "Tu valides l'envoi ?" | Earlier authorization on a different draft |

When ambiguous, re-ask. The cost of a re-ask is cheap; the cost of an unwanted send is high.

## Verifying facts before they leave

If the message quotes any fact extracted from files, scans, scraped pages or account exports, **verify it is current** before drafting the send:

1. Re-read the source to confirm the fact still holds
2. Cross-check dates — data older than 30 days may be stale; flag it
3. If the fact is "X happened on date Y" and Y is a reference point of the message, double-check Y is real and not a typo or a misread

Common gotchas:
- A subject line in a cache ≠ what the person actually wrote; verify the body
- "Latest balance" from a scrape ≠ today's balance; flag the snapshot date
- Phone numbers/addresses extracted by pattern may be partial or wrong

## Send protocol

When ready to send, output one of these patterns explicitly:

### Pattern A — fresh draft
```
**De** : <sender>
**À** : <recipient>
**CC** : <cc if any>
**Objet** : <subject>
**Pièces jointes** : <list or none>

<full body, exactly as it will be sent>

---
Tu valides l'envoi ?
```

Then **stop** and wait. Do not call the send tool until the user explicitly says yes.

### Pattern B — modified after feedback
Show the full revised version (not just the diff) and re-ask. Don't assume the prior approval covers the revision.

### Pattern C — several recipients in one batch
List each separate message individually with its own subject/body. Either ask per message or ask once with an explicit "OK to send all 3 as drafted above".

## After sending

Always confirm completion with:
- Recipients delivered
- Sent vs. queued vs. error
- Whether a copy was archived (Sent folder, local file…)
- Where the user can read what was sent

## Edge cases

- **Automatic anti-spam validation** (a sender-verification service asking to click a link): clicking it is part of the original send, not a new send — but still flag it: "Le filtre anti-spam X demande validation, je clique. OK ?"
- **Auto-resend after failure**: a bounce or a 4xx is a new send opportunity; re-ask before retrying.
- **Background agents**: agents dispatched from Claude Code that send external messages must inherit this rule. Their prompts must include: "Before any external send, surface the draft to the team lead and wait for explicit confirmation."
- **Form submissions on administrative or bank sites**: clicking the final "Valider" button that triggers an action (request, claim, change of details) **is** a send. Confirm first.

## Why this exists

When someone acts for several people or ongoing cases, a single mis-sent or premature message can cascade into administrative complications, alert the wrong stakeholders, or commit the user (or the people they represent) to positions they never agreed to. The cost of a 30-second pause is negligible; the cost of an unwanted send can be days of cleanup.
