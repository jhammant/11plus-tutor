#!/bin/bash
# 11+ Tutor - Easy Installer for Mac/Linux
# Run with: curl -fsSL https://raw.githubusercontent.com/yourusername/11plus-tutor/main/scripts/install.sh | bash

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo ""
echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║                                                            ║${NC}"
echo -e "${BLUE}║   ${GREEN}11+ Tutor Installer${BLUE}                                     ║${NC}"
echo -e "${BLUE}║   ${NC}Free exam practice for grammar school entrance${BLUE}           ║${NC}"
echo -e "${BLUE}║                                                            ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Detect OS
if [[ "$OSTYPE" == "darwin"* ]]; then
    OS="mac"
    echo -e "${GREEN}✓${NC} Detected: macOS"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="linux"
    echo -e "${GREEN}✓${NC} Detected: Linux"
else
    echo -e "${RED}✗${NC} Unsupported OS. Please use Mac or Linux, or see README for Windows instructions."
    exit 1
fi

# Check for Python 3.10+
echo ""
echo -e "${BLUE}Checking prerequisites...${NC}"

check_python() {
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
        MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
        MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)
        if [ "$MAJOR" -ge 3 ] && [ "$MINOR" -ge 10 ]; then
            echo -e "${GREEN}✓${NC} Python $PYTHON_VERSION found"
            return 0
        fi
    fi
    return 1
}

check_node() {
    if command -v node &> /dev/null; then
        NODE_VERSION=$(node -v | cut -d'v' -f2 | cut -d'.' -f1)
        if [ "$NODE_VERSION" -ge 18 ]; then
            echo -e "${GREEN}✓${NC} Node.js $(node -v) found"
            return 0
        fi
    fi
    return 1
}

# Check Python
if ! check_python; then
    echo -e "${YELLOW}!${NC} Python 3.10+ not found"
    if [[ "$OS" == "mac" ]]; then
        echo -e "  Installing Python via Homebrew..."
        if ! command -v brew &> /dev/null; then
            echo -e "  Installing Homebrew first..."
            /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
        fi
        brew install python@3.12
    else
        echo -e "  Please install Python 3.10+:"
        echo -e "  ${YELLOW}sudo apt update && sudo apt install python3 python3-pip python3-venv${NC}"
        exit 1
    fi
fi

# Check Node.js
if ! check_node; then
    echo -e "${YELLOW}!${NC} Node.js 18+ not found"
    if [[ "$OS" == "mac" ]]; then
        echo -e "  Installing Node.js via Homebrew..."
        brew install node
    else
        echo -e "  Please install Node.js 18+:"
        echo -e "  ${YELLOW}curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash - && sudo apt install -y nodejs${NC}"
        exit 1
    fi
fi

# Check Git
if ! command -v git &> /dev/null; then
    echo -e "${YELLOW}!${NC} Git not found"
    if [[ "$OS" == "mac" ]]; then
        echo -e "  Installing Git via Homebrew..."
        brew install git
    else
        echo -e "  Please install Git:"
        echo -e "  ${YELLOW}sudo apt install git${NC}"
        exit 1
    fi
fi
echo -e "${GREEN}✓${NC} Git found"

# Choose install directory
echo ""
INSTALL_DIR="$HOME/11plus-tutor"
echo -e "${BLUE}Where would you like to install 11+ Tutor?${NC}"
echo -e "  Default: ${YELLOW}$INSTALL_DIR${NC}"
read -p "  Press Enter for default, or type a path: " CUSTOM_DIR

if [ -n "$CUSTOM_DIR" ]; then
    INSTALL_DIR="$CUSTOM_DIR"
fi

# Clone or update repository
echo ""
if [ -d "$INSTALL_DIR" ]; then
    echo -e "${YELLOW}!${NC} Directory exists. Updating..."
    cd "$INSTALL_DIR"
    git pull origin main
else
    echo -e "${BLUE}Downloading 11+ Tutor...${NC}"
    git clone https://github.com/yourusername/11plus-tutor.git "$INSTALL_DIR"
    cd "$INSTALL_DIR"
fi

echo -e "${GREEN}✓${NC} Downloaded to $INSTALL_DIR"

# Set up Python virtual environment
echo ""
echo -e "${BLUE}Setting up Python environment...${NC}"
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip -q
pip install -r requirements.txt -q
echo -e "${GREEN}✓${NC} Python dependencies installed"

# Set up Node.js
echo ""
echo -e "${BLUE}Setting up web interface...${NC}"
cd web
npm install --silent 2>/dev/null
cd ..
echo -e "${GREEN}✓${NC} Web dependencies installed"

# Create .env if it doesn't exist
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo -e "${GREEN}✓${NC} Configuration file created"
fi

# Create launch script
cat > start.sh << 'LAUNCH'
#!/bin/bash
cd "$(dirname "$0")"
source venv/bin/activate
echo ""
echo "Starting 11+ Tutor..."
echo "Opening http://localhost:3783 in your browser..."
echo ""
echo "Press Ctrl+C to stop"
echo ""

# Open browser after short delay
(sleep 3 && open http://localhost:3783 2>/dev/null || xdg-open http://localhost:3783 2>/dev/null) &

python scripts/start_app.py
LAUNCH
chmod +x start.sh

# Success message
echo ""
echo -e "${GREEN}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║                                                            ║${NC}"
echo -e "${GREEN}║   ✓ Installation Complete!                                 ║${NC}"
echo -e "${GREEN}║                                                            ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "  ${BLUE}To start 11+ Tutor:${NC}"
echo ""
echo -e "    cd $INSTALL_DIR"
echo -e "    ./start.sh"
echo ""
echo -e "  Or run this anytime:"
echo -e "    ${YELLOW}$INSTALL_DIR/start.sh${NC}"
echo ""
echo -e "  The app will open at: ${BLUE}http://localhost:3783${NC}"
echo ""
echo -e "  ${GREEN}No internet required after installation!${NC}"
echo -e "  ${GREEN}No AI/LLM required - all 1,364 questions work offline!${NC}"
echo ""

# Ask to start now
read -p "Start 11+ Tutor now? (y/n) " START_NOW
if [[ "$START_NOW" =~ ^[Yy]$ ]]; then
    ./start.sh
fi
