#!/bin/bash
set -e

echo "🚀 Installing Amplifier plugins for Claude Code..."
echo ""

# Check if claude CLI is available
if ! command -v claude &> /dev/null; then
    echo "❌ Error: claude CLI not found"
    echo ""
    echo "Please install Claude Code first:"
    echo "  https://claude.ai/download"
    exit 1
fi

echo "✅ Claude CLI found"
echo ""

# Add Amplifier marketplace (amplifier-claude branch)
echo "📦 Adding Amplifier marketplace..."
if claude plugin marketplace add https://github.com/kenotron-ms/amplifier#amplifier-claude; then
    echo "✅ Marketplace added (amplifier-claude branch)"
else
    echo "⚠️  Marketplace may already be added (continuing...)"
fi
echo ""

# Install plugins in project scope
echo "📥 Installing plugins..."
echo ""

echo "  Installing amp plugin (core philosophy & agents)..."
if claude plugin install amp@amplifier --scope project; then
    echo "  ✅ amp installed"
else
    echo "  ⚠️  amp may already be installed"
fi

echo "  Installing git plugin (workflow helpers)..."
if claude plugin install git@amplifier --scope project; then
    echo "  ✅ git installed"
else
    echo "  ⚠️  git may already be installed"
fi

echo "  Installing dev-kit plugin (SDLC toolkit)..."
if claude plugin install dev-kit@amplifier --scope project; then
    echo "  ✅ dev-kit installed"
else
    echo "  ⚠️  dev-kit may already be installed"
fi

echo ""
echo "🎉 Installation complete!"
echo ""
echo "Available commands:"
echo "  /amp:*        - Core Amplifier commands and agents"
echo "  /git:*        - Git workflow helpers"
echo "  /dev-kit:*    - Feature development SDLC workflow"
echo ""
echo "📚 Plugin guidance is automatically loaded from installed plugins."
echo "   Edit your CLAUDE.md to add project-specific instructions."
echo ""
echo "For more info: https://github.com/kenotron-ms/amplifier"
