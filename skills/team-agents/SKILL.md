---
name: team-agents
description: Deploy and coordinate parallel Agent Teams. Use when the user asks for parallel agents, teams, swarms, or when a task has 2+ independent workstreams. Guides the full lifecycle from TeamCreate through dispatch, monitoring, and cleanup.
trigger: /team-agents
---

# Agent Teams — Parallel Agent Orchestration

Use this skill whenever you need to run multiple agents in parallel. You are the **team leader** — you orchestrate, you NEVER do the work yourself.

## When to Use Teams

| Situation | Use Teams? |
|---|---|
| 2+ independent tasks that can run in parallel | YES |
| Sequential tasks with dependencies | YES — chain with `addBlockedBy` |
| Single simple task | NO — just do it directly |
| Quick research/lookup | NO — use Agent() without a team |

## The Flow

```
TeamCreate → TaskCreate (with deps) → Agent × N (background) → monitor TaskList
→ SendMessage to wake idle agents → TaskUpdate(completed) → TeamDelete
```

## Step-by-Step

### 1. Create the Team

```
TeamCreate({
  team_name: "my-feature",
  description: "Building X with parallel agents"
})
```

- One team per leader session. Team name = kebab-case.
- This creates `~/.claude/teams/my-feature/config.json` and `~/.claude/tasks/my-feature/`.

### 2. Create Tasks

Create ALL tasks upfront, then set dependencies:

```
TaskCreate({
  subject: "Scaffold project structure",
  description: "Create package.json, tsconfig, src/ dirs..."
})
// → returns task #1

TaskCreate({
  subject: "Build API endpoints",
  description: "Create REST endpoints for /users, /posts..."
})
// → returns task #2

TaskCreate({
  subject: "Build frontend components",
  description: "Create React components for dashboard..."
})
// → returns task #3
```

Set dependencies (tasks 2 and 3 wait for task 1):
```
TaskUpdate({ taskId: "2", addBlockedBy: ["1"] })
TaskUpdate({ taskId: "3", addBlockedBy: ["1"] })
```

### 3. Dispatch Agents

Launch agents with ALL of these parameters — missing any one causes problems:

```
Agent({
  name: "scaffolder",          // REQUIRED — makes agent addressable
  team_name: "my-feature",    // REQUIRED — joins the team
  mode: "bypassPermissions",  // REQUIRED — no permission prompts
  run_in_background: true,    // REQUIRED — don't block leader
  prompt: "..."               // REQUIRED — FULL context (see below)
})
```

**Launch multiple agents simultaneously** by putting multiple Agent() calls in a single message.

**CRITICAL — the prompt must be SELF-CONTAINED:**
- Agents cannot see your conversation. They start blank.
- Include: what to do, which task IDs to claim, file paths, context, constraints.
- Include: "When you encounter ANY issue — search online FIRST (WebSearch/WebFetch)."
- Include: "When done, mark your task as completed via TaskUpdate."
- Include: "After completing a task, check TaskList for newly unblocked tasks to claim."

Example prompt:
```
You are "scaffolder" on team "my-feature".

Your task: #1 — Scaffold project structure
- Create package.json with dependencies: react, vite, typescript
- Create tsconfig.json, src/main.tsx, src/App.tsx
- Run npm install
- Working directory: /path/to/project

When done:
1. TaskUpdate({ taskId: "1", status: "completed" })
2. Check TaskList for unblocked tasks — claim and do them if available
3. If no more work, go idle

When you encounter ANY issue — search online FIRST.
```

### 4. Monitor Progress

You are the leader. You DON'T work — you coordinate:

- **Agents report automatically.** When they complete tasks or need help, you get messages.
- **Agents go idle between turns.** This is NORMAL. It does NOT mean they crashed or are done.
- **To wake an idle agent:** `SendMessage({ to: "scaffolder", message: "Task 2 is now unblocked, please claim it" })`
- **Check progress:** `TaskList()` to see task statuses.
- **DON'T poll in a loop.** Wait for agent messages — they arrive automatically.

### 5. Handle Completions

When an agent reports a task is done:
1. Verify if needed (read files, run tests)
2. Check if downstream tasks are unblocked
3. SendMessage to available agents to pick up unblocked work
4. Or let agents self-assign (if you told them to check TaskList)

### 6. Shutdown

When ALL tasks are complete:

```
// Gracefully shutdown each agent
SendMessage({ to: "scaffolder", message: { type: "shutdown_request", reason: "All done" } })
SendMessage({ to: "builder", message: { type: "shutdown_request", reason: "All done" } })

// Wait for shutdown responses, then:
TeamDelete()
```

If a stale team blocks a new one:
```bash
rm -rf ~/.claude/teams/my-feature
```

## Common Mistakes

### 1. Forgetting `name` or `team_name` on Agent()
Agent becomes invisible — can't receive messages, can't be monitored. ALWAYS set both.

### 2. Forgetting `run_in_background: true`
Leader blocks waiting for agent to finish — defeats the purpose of parallelism.

### 3. Prompts that assume conversation context
Agent: "Based on what we discussed..." — NO. Agent has ZERO context. Put everything in the prompt.

### 4. Leader doing work instead of delegating
If you're writing code or reading files for implementation, you're doing it wrong. Delegate to an agent.

### 5. Panicking about idle agents
Idle = waiting for input. It's normal. Send a message to wake them.

### 6. Not setting task dependencies
Without `addBlockedBy`, agents race on dependent tasks. Scaffolding must finish before building.

### 7. Using `Agent()` without a team
Bare `Agent()` calls are invisible — no progress tracking, no task coordination. Use teams for any multi-agent work.

## Patterns

### Fan-Out / Fan-In
1 setup task → N parallel tasks → 1 merge task
```
Task 1: Setup (blocks 2, 3, 4)
Task 2: Build module A (blocks 5)
Task 3: Build module B (blocks 5)
Task 4: Build module C (blocks 5)
Task 5: Integration test (blocked by 2, 3, 4)
```

### Pipeline
Each task feeds the next:
```
Task 1: Research (blocks 2)
Task 2: Design (blocks 3)
Task 3: Implement (blocks 4)
Task 4: Test
```

### Specialist Teams
Different agent types for different jobs:
```
Agent({ name: "researcher", subagent_type: "Explore", ... })   // read-only research
Agent({ name: "builder", subagent_type: "general-purpose", ... }) // implementation
Agent({ name: "tester", subagent_type: "test-engineer", ... })  // testing
```

Note: read-only agents (Explore, Plan) CANNOT edit files. Only assign them research tasks.

## Quick Reference

| Tool | When |
|---|---|
| `TeamCreate({ team_name, description })` | Start a team |
| `TaskCreate({ subject, description })` | Add a task |
| `TaskUpdate({ taskId, addBlockedBy })` | Set dependencies |
| `TaskUpdate({ taskId, status, owner })` | Claim/complete tasks |
| `TaskList()` | Check progress |
| `Agent({ name, team_name, mode, run_in_background, prompt })` | Dispatch agent |
| `SendMessage({ to, message })` | Wake/direct an agent |
| `SendMessage({ to, message: { type: "shutdown_request" } })` | Shutdown agent |
| `TeamDelete()` | Clean up team |
