---
name: collab-docx-edit
description: Use when collaboratively editing a Drive document (DOCX / Google Doc) where the user is ALSO making direct edits in the Drive UI. Forces a "download current → patch in place → upload" loop to preserve user's manual changes. Trigger phrases — "corrige le doc", "applique cette modif", "je fais des commentaires/corrections, tu fixes", "fix this in the doc", or anytime the user mentions a Drive doc URL they are editing live.
metadata:
  type: feedback
---

# Collaborative DOCX editing — preserve user's live edits

## The trap

When the user is editing a Drive doc and asks for changes, the wrong workflow is:

1. Edit a local `.md` / source file
2. Run `pandoc source.md -o out.docx`
3. Upload `out.docx` to Drive (overwriting)

**This wipes every edit the user made in Drive between two AI corrections.** Real edits get lost this way — never again.

## The right workflow

Always: **download current → patch in place → upload back**. The Drive doc is the source of truth, not any local file.

### Step 1 — Download the live Drive doc

```bash
gws drive files get \
  --params '{"fileId":"<DRIVE_FILE_ID>","alt":"media"}' \
  --output "$TMPDIR/docx-build/<name>_LIVE.docx"
```

### Step 2 — Locate the target paragraph by CONTENT match

Never trust paragraph indices across edits — search by text fragment.

```python
from docx import Document
doc = Document(r"...path_LIVE.docx")
for i, p in enumerate(doc.paragraphs):
    if 'distinctive phrase to find' in p.text:
        # found — apply patch
        ...
```

### Step 3 — Apply targeted patch

Three common patches:

**Delete a paragraph** (e.g. user removed a sentence you put back):

```python
def delete_paragraph(doc, needle):
    for p in doc.paragraphs:
        if needle in p.text:
            el = p._element
            el.getparent().remove(el)
            return True
    return False
```

**Replace text inside a paragraph** (preserves the paragraph itself):

```python
def replace_in_paragraph(doc, needle, replacement):
    for p in doc.paragraphs:
        if needle in p.text:
            # Simplest: clear runs, add one new run
            # WARNING: this loses inline formatting (bold/italic mid-paragraph)
            for r in p.runs:
                r.text = ''
            if p.runs:
                p.runs[0].text = p.text.replace(needle, replacement)
            else:
                p.add_run(replacement)
            return True
    return False
```

**Insert a paragraph after another** (e.g. add a bullet):

```python
from copy import deepcopy
from docx.oxml.ns import qn
def insert_after(doc, anchor_text, new_text, style=None):
    for p in doc.paragraphs:
        if anchor_text in p.text:
            new_p = deepcopy(p)  # carry over style
            for r in new_p.runs: r.text = ''
            new_p.runs[0].text = new_text if new_p.runs else None
            if not new_p.runs:
                new_p.add_run(new_text)
            p._element.addnext(new_p._element)
            return True
    return False
```

For tables, headers, lists, see python-docx docs — same principle: locate by content, mutate in place.

### Step 4 — Save + upload back to same fileId

```bash
gws drive files update \
  --params '{"fileId":"<DRIVE_FILE_ID>"}' \
  --upload "$TMPDIR/docx-build/<name>_PATCHED.docx"
```

### Step 5 — Verify the patch took

Re-download, check the change is present and only the expected paragraphs changed.

```bash
gws drive files get --params '{"fileId":"<ID>","alt":"media"}' --output verify.docx
python3 -c "from docx import Document; d=Document('verify.docx'); print(any('needle' in p.text for p in d.paragraphs))"
```

## When this rule does NOT apply

- **First creation** of a doc (no user edits yet) → free to generate from local source
- **User explicitly says** "regenerate the whole doc from scratch" or "I haven't touched it, push your version"
- **Doc has zero user edits since last AI upload** — verify via `modifiedTime` in Drive metadata vs last upload timestamp

In doubt → ask the user before regenerating from local source.

## Companion rule for Google Docs (native, mimeType `application/vnd.google-apps.document`)

For native Google Docs, prefer the **Docs API batchUpdate** with `replaceAllText` requests:

```bash
gws docs documents batchUpdate --params '{"documentId":"<ID>"}' --json '{
  "requests": [
    {"replaceAllText":{"containsText":{"text":"old text","matchCase":true},"replaceText":"new text"}}
  ]
}'
```

This preserves ALL formatting and surgical-edits the doc without touching anything else.

## Why this matters

Typical reaction after such an incident: *"I'm correcting into the void!"* — losing trust in the loop kills the iteration. Preserve user edits at all costs.
