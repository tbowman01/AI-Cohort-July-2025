## 🧭 Purpose

A single `hybrid-claude.md` that:
- Defines **clear agent roles and responsibilities** (like `claude.md`)
- Enables **high-throughput task orchestration** via batching (from SPARC)
- Supports **end-to-end CI/CD, review, testing, release** automation
- Optimizes **parallel execution** using `BatchTool` and `MCP` agents
- Maintains **auditability**, **transparency**, and **multi-agent coordination**

---

## 🧠 Core Principles

- **All agent tasks MUST be parallelized** where possible (batch-style)
- **Claude comments must include co-author and model disclosure**
- **Workflows should be swarm-bootstrapped and tracked**
- **Contextual prompts should be standardized by role**

---

## 🔁 Unified Agent Roles

| Role             | Task Focus                                | Batch-Aware | GitHub-Integrated | MCP/Swarm |
|------------------|--------------------------------------------|-------------|-------------------|-----------|
| `planner`        | Translate specs into implementation plans | ✅           | ✅ (Issues, PRs)   | ✅         |
| `coder`          | Generate code for a module/feature         | ✅           | ✅ (Commits)       | ✅         |
| `reviewer`       | Perform PR review with diffs + style       | ✅           | ✅ (PR comments)   | ✅         |
| `tester`         | Add and run tests for code                 | ✅           | ✅ (CI feedback)   | ✅         |
| `release-manager`| Create release notes, changelog, tags      | 🟡           | ✅                | ✅         |

---

## ⚙️ Example: Swarm Task Template

```js
[BatchTool]:
  mcp__claude-flow__swarm_init { topology: "flat", maxAgents: 6 }
  mcp__claude-flow__agent_spawn { type: "planner" }
  mcp__claude-flow__agent_spawn { type: "coder" }
  mcp__claude-flow__agent_spawn { type: "reviewer" }
  mcp__claude-flow__agent_spawn { type: "tester" }
  TodoWrite {
    todos: [
      "Plan out the new authentication module",
      "Implement backend endpoint",
      "Add unit tests",
      "Perform security review"
    ]
  }
  Bash("mkdir -p backend/auth && touch backend/auth/index.ts")
  Write("backend/auth/index.ts")
````

---

## 🛠 Prompt Templates (Hybridized)

### 🎯 Coder

```
System: You are a backend AI engineer. Write secure, clean, idiomatic code.
Prompt: Implement the following feature: <feature>. Use context files provided.
```

### ✅ Reviewer

```
System: You are a senior reviewer. Review diffs for bugs, security, style.
Prompt: Review the PR diff. Respond with bullet-pointed feedback or LGTM.
```

### 🧪 Tester

```
System: You are a test engineer. Ensure logic and edge cases are covered.
Prompt: Generate tests for <feature>. Use our test style. Include setup/teardown.
```

### 📰 Release Manager

```
System: You are an AI changelog writer.
Prompt: Summarize merged PRs into clean user-facing release notes.
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
      "Bash(git *)",
      "Bash(gh *)",
      "mcp__claude-flow__*"
    ]
  }
}
```

---

## 🧩 Coordination Hooks

```bash
npx claude-flow@alpha hooks pre-task
npx claude-flow@alpha hooks post-edit
npx claude-flow@alpha hooks notify
npx claude-flow@alpha hooks post-task
```

These should be invoked automatically via GitHub Actions or swarm-status listeners.

---

## 📊 Progress Tracker Format

```
📊 Claude Swarm Progress
├── Total: X
├── ✅ Completed: X
├── 🔄 In Progress: X
├── ⭕ Todo: X
└── ❌ Blocked: X
```

Used in CI/CD logs and `gh pr comment` feedback.

---

## 🔗 Hybrid CLI Commands

| Task         | Command                                                         |
| ------------ | --------------------------------------------------------------- |
| Spec + Plan  | `npx claude-flow sparc run spec-pseudocode "<task>" --parallel` |
| Generate     | `npx claude-flow sparc run architect "<task>" --parallel`       |
| TDD          | `npx claude-flow sparc tdd "<feature>" --batch-tdd`             |
| Integrate    | `npx claude-flow sparc run integration "<task>" --parallel`     |
| Full Feature | Combine with swarm + batchtool as shown above                   |

---

## 🧠 Summary

This `hybrid-claude.md` ensures:

* **Clarity for humans**, **speed for agents**, **power for workflows**
* Seamless **CI/CD integration**, **PR feedback**, and **release management**
* Best practices from both `claude.md` (declarative clarity) and SPARC/BATCHTOOLS (batch-first execution)

> 🧩 Use this as the single source of truth for Claude Max-5 driven automation.
> 🧠 Designed for devs, optimized for swarms.

```

Let me know if you’d like this saved to a repo, turned into a template file, or integrated with GitHub Actions.
```
