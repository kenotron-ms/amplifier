# Amplifier Plugin Installer for Windows
$ErrorActionPreference = "Stop"

Write-Host "🚀 Installing Amplifier plugins for Claude Code..." -ForegroundColor Cyan
Write-Host ""

# Check if claude CLI is available
try {
    $null = Get-Command claude -ErrorAction Stop
    Write-Host "✅ Claude CLI found" -ForegroundColor Green
} catch {
    Write-Host "❌ Error: claude CLI not found" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please install Claude Code first:"
    Write-Host "  https://claude.ai/download"
    exit 1
}
Write-Host ""

# Create .claude directory and settings.json with marketplace configuration
Write-Host "📝 Configuring Claude Code marketplace..." -ForegroundColor Yellow
New-Item -ItemType Directory -Force -Path ".claude" | Out-Null

$settingsJson = @"
{
  "permissions": {
    "allow": ["Bash", "mcp__playwright", "mcp__deepwiki", "WebFetch", "TodoWrite"],
    "deny": [],
    "defaultMode": "bypassPermissions",
    "additionalDirectories": [".data", ".vscode", ".claude", ".ai"]
  },
  "enableAllProjectMcpServers": false,
  "enabledMcpjsonServers": ["playwright", "deepwiki"],
  "extraKnownMarketplaces": {
    "amplifier": {
      "source": {
        "source": "github",
        "repository": "kenotron-ms/amplifier",
        "ref": "amplifier-claude"
      }
    }
  },
  "enabledPlugins": {
    "amp@amplifier": true,
    "git@amplifier": true,
    "dev-kit@amplifier": true
  }
}
"@

$settingsJson | Out-File -FilePath ".claude/settings.json" -Encoding UTF8 -NoNewline

Write-Host "✅ Marketplace configuration written to .claude/settings.json" -ForegroundColor Green
Write-Host ""

# Add Amplifier marketplace (amplifier-claude branch)
Write-Host "📦 Adding Amplifier marketplace..." -ForegroundColor Yellow
try {
    claude plugin marketplace add https://github.com/kenotron-ms/amplifier#amplifier-claude | Out-Null
    Write-Host "✅ Marketplace added (amplifier-claude branch)" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Marketplace may already be added (continuing...)" -ForegroundColor Yellow
}
Write-Host ""

# Install plugins in project scope
Write-Host "📥 Installing plugins..." -ForegroundColor Yellow
Write-Host ""

Write-Host "  Installing amp plugin (core philosophy & agents)..."
try {
    claude plugin install amp@amplifier --scope project | Out-Null
    Write-Host "  ✅ amp installed" -ForegroundColor Green
} catch {
    Write-Host "  ⚠️  amp may already be installed" -ForegroundColor Yellow
}

Write-Host "  Installing git plugin (workflow helpers)..."
try {
    claude plugin install git@amplifier --scope project | Out-Null
    Write-Host "  ✅ git installed" -ForegroundColor Green
} catch {
    Write-Host "  ⚠️  git may already be installed" -ForegroundColor Yellow
}

Write-Host "  Installing dev-kit plugin (SDLC toolkit)..."
try {
    claude plugin install dev-kit@amplifier --scope project | Out-Null
    Write-Host "  ✅ dev-kit installed" -ForegroundColor Green
} catch {
    Write-Host "  ⚠️  dev-kit may already be installed" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "🎉 Installation complete!" -ForegroundColor Green
Write-Host ""
Write-Host "Available commands:"
Write-Host "  /amp:*        - Core Amplifier commands and agents"
Write-Host "  /git:*        - Git workflow helpers"
Write-Host "  /dev-kit:*    - Feature development SDLC workflow"
Write-Host ""
Write-Host "📚 Plugin guidance is automatically loaded from installed plugins."
Write-Host "   Edit your CLAUDE.md to add project-specific instructions."
Write-Host ""
Write-Host "For more info: https://github.com/kenotron-ms/amplifier"
