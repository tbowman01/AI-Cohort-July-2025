# Claude Code + SPARC/BATCHTOOLS Quick Reference

## 🚨 Absolute Rule: Batch & Parallelize Everything
- **All related operations (todos, agents, file ops, bash, memory) must be batched in one message.**
- **Never execute related operations sequentially.**

**Correct:**
```js
[Single Message]: TodoWrite([todos]), Task([agents]), Bash([commands]), Write([files])
```
**Incorrect:**
```js
Message 1: TodoWrite, Message 2: Task, Message 3: Bash
```

## SPARC Workflow (Batchtools Enhanced)
1. **Spec:** `npx claude-flow sparc run spec-pseudocode "<task>" --parallel`
2. **Pseudo:** `npx claude-flow sparc run spec-pseudocode "<task>" --batch-optimize`
3. **Arch:** `npx claude-flow sparc run architect "<task>" --parallel`
4. **Refine:** `npx claude-flow sparc tdd "<feature>" --batch-tdd`
5. **Integrate:** `npx claude-flow sparc run integration "<task>" --parallel`

## Agent Categories (Examples)
- Core: coder, reviewer, tester, planner, researcher
- Coordination: coordinator, mesh, adaptive, swarm-memory
- Distributed: raft, gossip, consensus, crdt, security
- GitHub: pr-manager, code-review, issue-tracker, release-manager
- SPARC: specification, pseudocode, architecture, refinement

**Concurrent Agent Deployment:**
```js
Task("Research requirements", "...", "researcher")
Task("Plan architecture", "...", "planner")
Task("Implement features", "...", "coder")
Task("Create tests", "...", "tester")
Task("Review code", "...", "reviewer")
```

## Batchtools Features
- Parallel file/code/test/doc operations
- Smart batching, pipeline processing, resource management

## Performance
- 2-4x speedup, 30%+ token reduction, 80%+ solve rate (SWE-Bench)

## Best Practices
- Batch all operations, use memory for coordination, monitor with swarm_status

## MCP vs Claude Code
- **MCP:** Plans, coordinates, stores memory, tracks performance
- **Claude Code:** Executes all real work (file ops, code, bash, todos, git, tests)

## Example: Full-Stack Swarm (Parallel)
```js
[BatchTool]:
  mcp__claude-flow__swarm_init { topology: "hierarchical", maxAgents: 8 }
    mcp__claude-flow__agent_spawn { type: "architect" }
      mcp__claude-flow__agent_spawn { type: "coder" }
        mcp__claude-flow__agent_spawn { type: "tester" }
          TodoWrite { todos: [multiple todos] }
            Bash("mkdir -p app/{src,tests,docs}")
              Write("app/package.json")
              ```

              ## Coordination Protocol (Every Agent)
              - Pre-task: `npx claude-flow@alpha hooks pre-task`
              - Post-edit: `npx claude-flow@alpha hooks post-edit`
              - Notify: `npx claude-flow@alpha hooks notify`
              - Post-task: `npx claude-flow@alpha hooks post-task`

              ## Visual Progress Format
              ```
              📊 Progress
              ├── Total: X
              ├── ✅ Completed: X
              ├── 🔄 In Progress: X
              ├── ⭕ Todo: X
              └── ❌ Blocked: X
              ```

              ## Links
              - [SPARC Guide](https://github.com/ruvnet/claude-code-flow/docs/sparc.md)
              - [Batchtools Docs](https://github.com/ruvnet/claude-code-flow/docs/batchtools.md)
              - [Claude Flow](https://github.com/ruvnet/claude-flow)

              