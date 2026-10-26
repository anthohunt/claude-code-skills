---
name: brainstorming-design
description: Use when creating or developing, before writing code or implementation plans - refines rough ideas into fully-formed designs through collaborative questioning, alternative exploration, and incremental validation. Don't use during clear 'mechanical' processes
---

# Brainstorming Ideas Into Designs

> Derived from the `brainstorming` skill of [obra/superpowers](https://github.com/obra/superpowers) (MIT, Copyright (c) 2025 Jesse Vincent; licence text in `LICENSE-superpowers-MIT`), modified. The modifications are under the same licences as the rest of this repository.

## Overview

Help turn ideas into fully formed designs and specs through natural collaborative dialogue.

Start by understanding the current project context, then ask questions one at a time to refine the idea. Once you understand what you're building, present the design in small sections (200-300 words), checking after each section whether it looks right so far.

## The Process

**Understanding the idea:**
- Check out the current project state first (files, docs, recent commits)
- Ask questions one at a time to refine the idea
- Prefer multiple choice questions when possible, but open-ended is fine too
- Only one question per message - if a topic needs more exploration, break it into multiple questions
- Focus on understanding: purpose, constraints, success criteria

**Exploring approaches:**
- Propose 2-3 different approaches with trade-offs
- Present options conversationally with your recommendation and reasoning
- Lead with your recommended option and explain why

**Presenting the design:**
- Once you believe you understand what you're building, present the design
- Break it into sections of 200-300 words
- Ask after each section whether it looks right so far
- Cover: architecture, components, data flow, error handling, testing strategy
- Be ready to go back and clarify if something doesn't make sense

## After the Design

**Once the design is validated by the user, dispatch a subagent to write and commit it:**

Use the Agent tool with a small, fast model:

```markdown
Agent tool parameters:
- subagent_type: "general-purpose"
- model: "haiku"
- description: "Write design document for [topic]"
- prompt: |
  Write the design document based on the brainstorming discussion.

  Context from brainstorming:
  [Paste the validated design content from discussion]

  Task:
  1. Write design document to: docs/plans/YYYY-MM-DD-<topic>-design.md
  2. Ensure all sections present: problem statement, solution, architecture, UX flow, success criteria, out of scope
  3. Commit to git with message: "docs: add <topic> design document"

  Report when complete.
```

**After subagent completes:**

Report to CEO: "Design phase complete. Design document committed to git at docs/plans/YYYY-MM-DD-<topic>-design.md"

## Design for Successful Implementation

**When creating designs, consider how the plan will be executed:**

- **Clear success criteria** - Define what "done" looks like for each feature
- **Testable requirements** - Ensure each feature can be validated with tests
- **Logical task breakdown** - Features that naturally divide into 5-15 implementation tasks
- **Explicit dependencies** - Call out what must be built before what
- **Error handling strategy** - How failures are detected and recovered

**Why this matters:** The implementation agent will follow the plan autonomously. Designs that are clear, testable, and well-scoped lead to higher success rates (research shows 39% improvement with plan-centric approaches).

## Key Principles

- **One question at a time** - Don't overwhelm with multiple questions
- **Multiple choice preferred** - Easier to answer than open-ended when possible
- **YAGNI ruthlessly** - Remove unnecessary features from all designs
- **Explore alternatives** - Always propose 2-3 approaches before settling
- **Incremental validation** - Present design in sections, validate each
- **Be flexible** - Go back and clarify when something doesn't make sense
- **Testing strategy** - Include high-level testing approach in design
- **Implementation-ready** - Consider how design translates to executable tasks
