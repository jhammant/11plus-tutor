# 11+ Tutor - Easy Installer for Windows
# Run with: irm https://raw.githubusercontent.com/jhammant/11plus-tutor/main/scripts/install.ps1 | iex

$ErrorActionPreference = "Stop"

Write-Host ""
Write-Host "╔════════════════════════════════════════════════════════════╗" -ForegroundColor Blue
Write-Host "║                                                            ║" -ForegroundColor Blue
Write-Host "║   11+ Tutor Installer                                      ║" -ForegroundColor Green
Write-Host "║   Free exam practice for grammar school entrance           ║" -ForegroundColor White
Write-Host "║                                                            ║" -ForegroundColor Blue
Write-Host "╚════════════════════════════════════════════════════════════╝" -ForegroundColor Blue
Write-Host ""

Write-Host "Detected: Windows" -ForegroundColor Green
Write-Host ""
Write-Host "Checking prerequisites..." -ForegroundColor Blue

# Check for Python
$pythonFound = $false
try {
    $pythonVersion = python --version 2>&1
    if ($pythonVersion -match "Python 3\.(\d+)") {
        $minor = [int]$Matches[1]
        if ($minor -ge 10) {
            Write-Host "✓ $pythonVersion found" -ForegroundColor Green
            $pythonFound = $true
        }
    }
} catch {}

if (-not $pythonFound) {
    Write-Host "! Python 3.10+ not found" -ForegroundColor Yellow
    Write-Host "  Please install Python from: https://www.python.org/downloads/" -ForegroundColor Yellow
    Write-Host "  IMPORTANT: Check 'Add Python to PATH' during installation!" -ForegroundColor Red
    Write-Host ""
    $openPython = Read-Host "Open Python download page? (y/n)"
    if ($openPython -eq "y") {
        Start-Process "https://www.python.org/downloads/"
    }
    Write-Host "Please install Python and run this script again."
    exit 1
}

# Check for Node.js
$nodeFound = $false
try {
    $nodeVersion = node --version 2>&1
    if ($nodeVersion -match "v(\d+)") {
        $major = [int]$Matches[1]
        if ($major -ge 18) {
            Write-Host "✓ Node.js $nodeVersion found" -ForegroundColor Green
            $nodeFound = $true
        }
    }
} catch {}

if (-not $nodeFound) {
    Write-Host "! Node.js 18+ not found" -ForegroundColor Yellow
    Write-Host "  Please install Node.js from: https://nodejs.org/" -ForegroundColor Yellow
    Write-Host ""
    $openNode = Read-Host "Open Node.js download page? (y/n)"
    if ($openNode -eq "y") {
        Start-Process "https://nodejs.org/"
    }
    Write-Host "Please install Node.js and run this script again."
    exit 1
}

# Check for Git
$gitFound = $false
try {
    $gitVersion = git --version 2>&1
    if ($gitVersion -match "git version") {
        Write-Host "✓ Git found" -ForegroundColor Green
        $gitFound = $true
    }
} catch {}

if (-not $gitFound) {
    Write-Host "! Git not found" -ForegroundColor Yellow
    Write-Host "  Please install Git from: https://git-scm.com/download/win" -ForegroundColor Yellow
    Write-Host ""
    $openGit = Read-Host "Open Git download page? (y/n)"
    if ($openGit -eq "y") {
        Start-Process "https://git-scm.com/download/win"
    }
    Write-Host "Please install Git and run this script again."
    exit 1
}

# Choose install directory
Write-Host ""
$defaultDir = "$env:USERPROFILE\11plus-tutor"
Write-Host "Where would you like to install 11+ Tutor?" -ForegroundColor Blue
Write-Host "  Default: $defaultDir" -ForegroundColor Yellow
$customDir = Read-Host "  Press Enter for default, or type a path"

if ($customDir) {
    $installDir = $customDir
} else {
    $installDir = $defaultDir
}

# Clone or update repository
Write-Host ""
if (Test-Path $installDir) {
    Write-Host "! Directory exists. Updating..." -ForegroundColor Yellow
    Set-Location $installDir
    git pull origin main
} else {
    Write-Host "Downloading 11+ Tutor..." -ForegroundColor Blue
    git clone https://github.com/jhammant/11plus-tutor.git $installDir
    Set-Location $installDir
}

Write-Host "✓ Downloaded to $installDir" -ForegroundColor Green

# Set up Python virtual environment
Write-Host ""
Write-Host "Setting up Python environment..." -ForegroundColor Blue
python -m venv venv
& ".\venv\Scripts\Activate.ps1"
pip install --upgrade pip -q
pip install -r requirements.txt -q
Write-Host "✓ Python dependencies installed" -ForegroundColor Green

# Set up Node.js
Write-Host ""
Write-Host "Setting up web interface..." -ForegroundColor Blue
Set-Location web
npm install --silent 2>$null
Set-Location ..
Write-Host "✓ Web dependencies installed" -ForegroundColor Green

# Create .env if it doesn't exist
if (-not (Test-Path ".env")) {
    Copy-Item ".env.example" ".env"
    Write-Host "✓ Configuration file created" -ForegroundColor Green
}

# Create launch script
$launchScript = @'
@echo off
cd /d "%~dp0"
call venv\Scripts\activate.bat
echo.
echo Starting 11+ Tutor...
echo Opening http://localhost:3783 in your browser...
echo.
echo Press Ctrl+C to stop
echo.
start "" http://localhost:3783
python scripts/start_app.py
'@
$launchScript | Out-File -FilePath "start.bat" -Encoding ASCII

# Create PowerShell launch script too
$psLaunchScript = @'
Set-Location $PSScriptRoot
& ".\venv\Scripts\Activate.ps1"
Write-Host ""
Write-Host "Starting 11+ Tutor..."
Write-Host "Opening http://localhost:3783 in your browser..."
Write-Host ""
Write-Host "Press Ctrl+C to stop"
Write-Host ""
Start-Process "http://localhost:3783"
python scripts/start_app.py
'@
$psLaunchScript | Out-File -FilePath "start.ps1" -Encoding UTF8

# Success message
Write-Host ""
Write-Host "╔════════════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║                                                            ║" -ForegroundColor Green
Write-Host "║   ✓ Installation Complete!                                 ║" -ForegroundColor Green
Write-Host "║                                                            ║" -ForegroundColor Green
Write-Host "╚════════════════════════════════════════════════════════════╝" -ForegroundColor Green
Write-Host ""
Write-Host "  To start 11+ Tutor:" -ForegroundColor Blue
Write-Host ""
Write-Host "    Option 1: Double-click start.bat in $installDir"
Write-Host "    Option 2: Run in PowerShell: $installDir\start.ps1"
Write-Host ""
Write-Host "  The app will open at: http://localhost:3783" -ForegroundColor Blue
Write-Host ""
Write-Host "  No internet required after installation!" -ForegroundColor Green
Write-Host "  No AI/LLM required - all 1,364 questions work offline!" -ForegroundColor Green
Write-Host ""

# Ask to start now
$startNow = Read-Host "Start 11+ Tutor now? (y/n)"
if ($startNow -eq "y") {
    & ".\start.ps1"
}
