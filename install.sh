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
echo "🎉 Plugins installed successfully!"
echo ""

# Configure CLAUDE.md to import Amplifier guidance
echo "📝 Configuring CLAUDE.md..."

CLAUDE_FILE="CLAUDE.md"
AMP_IMPORT="# Amplifier Plugin Guidance
@plugins/amp/AMP_GUIDANCE.md"

if [ -f "$CLAUDE_FILE" ]; then
    # Check if already configured
    if grep -q "@plugins/amp/AMP_GUIDANCE.md" "$CLAUDE_FILE"; then
        echo "   ✅ CLAUDE.md already configured for Amplifier"
    else
        # Add import at the beginning of the file
        echo "$AMP_IMPORT

$(cat $CLAUDE_FILE)" > "$CLAUDE_FILE"
        echo "   ✅ Added Amplifier import to existing CLAUDE.md"
    fi
else
    # Create new CLAUDE.md with Amplifier import
    cat > "$CLAUDE_FILE" << 'EOF'
# CLAUDE.md

# Amplifier Plugin Guidance
@plugins/amp/AMP_GUIDANCE.md

# Project-Specific Instructions

Add your project-specific guidance below...
EOF
    echo "   ✅ Created CLAUDE.md with Amplifier import"
fi

echo ""
echo "🎉 Installation complete!"
echo ""
echo "Available commands:"
echo "  /amp:*        - Core Amplifier commands and agents"
echo "  /git:*        - Git workflow helpers"
echo "  /dev-kit:*    - Feature development SDLC workflow"
echo ""
echo "📚 Your CLAUDE.md has been configured to import Amplifier guidance."
echo "   Edit CLAUDE.md to add project-specific instructions."
echo ""
echo "For more info: https://github.com/kenotron-ms/amplifier"
