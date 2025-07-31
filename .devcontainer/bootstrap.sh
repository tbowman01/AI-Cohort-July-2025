#!/bin/bash
set -euo pipefail

# ⚙️ Install latest NPM
npm install -g npm@11

# 🧪 Install uv and Claude monitor tools
curl -LsSf https://astral.sh/uv/install.sh | sh
uv tool install claude-monitor

# 🧠 Install Claude Code
echo "🧠 Installing Claude Code..."
npm install -g @anthropic-ai/claude-code

# ⚙️ Init Claude Flow
echo "⚙️ Activating Claude..."
claude --dangerously-skip-permissions

echo "🚀 Initialize Claude Flow with enhanced MCP setup (auto-configures permissions!)"
npx claude-flow@alpha init --force

echo "🤖 Spawning Claude Hive-Mind agent..."
echo 'npx claude-flow@alpha hive-mind spawn "analyze github repo, triage issues and pull requests and prompt me for your recommendation on what to tackle next" --auto-spawn --monitor'

echo "🎉 Done! 🎉"
