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
Write-Host "🎉 Plugins installed successfully!" -ForegroundColor Green
Write-Host ""

# Configure CLAUDE.md to import Amplifier guidance
Write-Host "📝 Configuring CLAUDE.md..." -ForegroundColor Yellow

$claudeFile = "CLAUDE.md"
$ampImport = @"
# Amplifier Plugin Guidance
@plugins/amp/AMP_GUIDANCE.md
"@

if (Test-Path $claudeFile) {
    # Check if already configured
    $content = Get-Content $claudeFile -Raw
    if ($content -match "@plugins/amp/AMP_GUIDANCE\.md") {
        Write-Host "   ✅ CLAUDE.md already configured for Amplifier" -ForegroundColor Green
    } else {
        # Add import at the beginning
        $newContent = $ampImport + "`n`n" + $content
        Set-Content -Path $claudeFile -Value $newContent
        Write-Host "   ✅ Added Amplifier import to existing CLAUDE.md" -ForegroundColor Green
    }
} else {
    # Create new CLAUDE.md with Amplifier import
    $newClaudeMd = @"
# CLAUDE.md

# Amplifier Plugin Guidance
@plugins/amp/AMP_GUIDANCE.md

# Project-Specific Instructions

Add your project-specific guidance below...
"@
    Set-Content -Path $claudeFile -Value $newClaudeMd
    Write-Host "   ✅ Created CLAUDE.md with Amplifier import" -ForegroundColor Green
}

Write-Host ""
Write-Host "🎉 Installation complete!" -ForegroundColor Green
Write-Host ""
Write-Host "Available commands:"
Write-Host "  /amp:*        - Core Amplifier commands and agents"
Write-Host "  /git:*        - Git workflow helpers"
Write-Host "  /dev-kit:*    - Feature development SDLC workflow"
Write-Host ""
Write-Host "📚 Your CLAUDE.md has been configured to import Amplifier guidance."
Write-Host "   Edit CLAUDE.md to add project-specific instructions."
Write-Host ""
Write-Host "For more info: https://github.com/kenotron-ms/amplifier"
