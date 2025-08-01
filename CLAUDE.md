# 🤖 Hybrid+ Claude Workflow Configuration (`hybrid-plus-claude.md`)

## 🧭 Purpose

- ✅ Maintain human-readable task planning and role-driven prompts  
- ⚡ Maximize batch parallelization with swarm coordination  
- 🔁 Enable adaptive workflows based on runtime conditions  
- 🧠 Persist swarm memory and summarize reasoning across PRs  
- 🛡 Comply with model auditability and provenance tracking  

---

## 🧠 Core Principles

1. All tasks must be declared in a single batched message  
2. Use `swarm_init` to maximize concurrency and resource allocation  
3. Enable memory tracking and reuse across sessions  
4. Capture Claude model identity and actions for transparency  
5. Support adaptive agents that react to runtime signals (e.g. failed PR checks)  

---

## 🔁 Role Definitions

| Role               | Responsibilities                                                             | Batch | Adaptive | GitHub Integrated |
|--------------------|------------------------------------------------------------------------------|-------|----------|-------------------|
| `planner`          | Translate specs/issues into technical plans                                  | ✅    | ❌        | ✅                 |
| `coder`            | Generate/modify backend code                                                 | ✅    | ❌        | ✅                 |
| `reviewer`         | Analyze diffs, style, and quality, post PR comments                          | ✅    | ❌        | ✅                 |
| `tester`           | Generate, execute, and report on tests                                       | ✅    | ❌        | ✅                 |
| `adaptive`         | Monitor CI status, spawn agents dynamically (e.g., re-run tests, fix style)  | 🟡    | ✅        | ✅                 |
| `release-manager`  | Generate changelogs, GitHub Releases, version tags                           | ✅    | ❌        | ✅                 |

---

## ⚙️ Batch Workflow Template

```js
[BatchTool]:
  mcp__claude-flow__swarm_init {
    topology: "flat",
    maxAgents: 6,
    memory: true,
    auditLedger: true
  }

  mcp__claude-flow__agent_spawn { type: "planner" }
  mcp__claude-flow__agent_spawn { type: "coder" }
  mcp__claude-flow__agent_spawn { type: "reviewer" }
  mcp__claude-flow__agent_spawn { type: "tester" }
  mcp__claude-flow__agent_spawn { type: "adaptive" }

  TodoWrite {
    todos: [
      "Plan API spec for new subscription flow",
      "Write implementation logic for endpoint",
      "Generate tests and validate coverage",
      "Monitor PR checks, re-trigger if failed"
    ]
  }

  Bash("mkdir -p src/subscription && touch src/subscription/endpoint.ts")
  Write("src/subscription/endpoint.ts")

  MemoryWrite("swarm-graph", {
    key: "pr-#94-subscription",
    tags: ["API", "backend", "coverage"],
    insights: [
      "used zod for input validation",
      "added JWT check for secure access"
    ]
  })

  LedgerLog("claude-3-opus", "coder", "sha256:ab8e...", "Add subscription endpoint", "2025-08-01T15:20Z")
````

---

## 📑 Prompt Templates

### 🧠 `planner`

```
System: You are a software architect.
Prompt: Break down the feature "<feature>" into implementable backend tasks and acceptance criteria.
```

### 🧑‍💻 `coder`

```
System: You are a secure backend developer.
Prompt: Implement "<feature>" using TypeScript. Follow existing patterns and include doc comments.
```

### 🧪 `tester`

```
System: You are a QA engineer.
Prompt: Generate test cases for "<module>". Cover edge cases and validate all branches.
```

### 👀 `reviewer`

```
System: You are a senior reviewer.
Prompt: Review this PR diff. Identify bugs, style violations, and logic errors. Use bullets.
```

### 🔁 `adaptive`

```
System: You are an adaptive DevOps agent.
Prompt: Monitor CI checks and trigger agents (e.g. tester or formatter) based on failures.
```

---

## 🔐 Permissions

```json
{
  "permissions": {
    "allow": [
      "Edit",
      "Write",
      "Bash(npm *)",
      "Bash(pytest *)",
      "Bash(gh *)",
      "Bash(git *)",
      "mcp__claude-flow__*",
      "MemoryWrite",
      "LedgerLog"
    ]
  }
}
```

---

## 📊 Progress & Observability

### Format for Swarm Status Updates

```
📊 Claude Swarm Progress
├── Total: 5
├── ✅ Completed: 3
├── 🔄 In Progress: 1
├── ⭕ Todo: 1
└── ❌ Blocked: 0
```

### Trigger for real-time update

```bash
npx claude-flow hooks post-edit | tee swarm-status.log
```

---

## 📁 Ledger + Memory Usage

### Memory Write Example

```json
{
  "key": "user-flow-refactor",
  "tags": ["auth", "jwt", "performance"],
  "insights": [
    "replaced bcrypt with argon2",
    "removed redundant DB calls in middleware"
  ]
}
```

### Ledger Log Example

```json
{
  "model": "claude-3-opus",
  "agent": "reviewer",
  "task": "Review login refactor PR",
  "hash": "sha256:eeb9...",
  "timestamp": "2025-08-01T15:00:00Z"
}
```

Stored under: `.claude-ledger/pr-<number>.json`

---

## 🧩 Coordination Hooks

```bash
npx claude-flow@alpha hooks pre-task
npx claude-flow@alpha hooks post-edit
npx claude-flow@alpha hooks notify
npx claude-flow@alpha hooks post-task
```

---

## 🔗 CLI Commands

| Task          | Command                                                            |
| ------------- | ------------------------------------------------------------------ |
| Spec + Plan   | `npx claude-flow sparc run spec-pseudocode "<task>" --parallel`    |
| Implement     | `npx claude-flow sparc run architect "<task>" --parallel`          |
| Test/Validate | `npx claude-flow sparc tdd "<feature>" --batch-tdd`                |
| PR Integrate  | `npx claude-flow sparc run integration "<task>" --parallel`        |
| Release       | `npx claude-flow release-manager generate --from main --to v1.2.0` |

---
