#!/bin/bash

# macOS Shell Script
# Created: $(date)
# Description: [Add description here]

set -e  # Exit on any error
set -u  # Exit on undefined variables

# Script starts here
echo "Starting script execution..."

# Step 1: Check if Python is installed, install if not present
echo "Step 1: Checking Python installation..."

if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo "✓ Python is already installed: $PYTHON_VERSION"
else
    echo "Python not found. Installing Python..."

    # Check if Homebrew is installed
    if command -v brew &> /dev/null; then
        echo "Installing Python using Homebrew..."
        brew install python3
    else
        echo "Homebrew not found. Installing Homebrew first..."
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

        # Add Homebrew to PATH for this session
        if [[ $(uname -m) == "arm64" ]]; then
            export PATH="/opt/homebrew/bin:$PATH"
        else
            export PATH="/usr/local/bin:$PATH"
        fi

        echo "Installing Python using Homebrew..."
        brew install python3
    fi

    # Verify installation
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version)
        echo "✓ Python successfully installed: $PYTHON_VERSION"
    else
        echo "❌ Failed to install Python"
        exit 1
    fi
fi

# Step 2: Check if uv is installed, install if not present
echo "Step 2: Checking uv installation..."

if command -v uv &> /dev/null; then
    UV_VERSION=$(uv --version)
    echo "✓ uv is already installed: $UV_VERSION"
else
    echo "uv not found. Installing uv..."

    # Install uv using the official installer
    curl -LsSf https://astral.sh/uv/install.sh | sh

    # Add uv to PATH for current session
    export PATH="$HOME/.cargo/bin:$PATH"

    # Verify installation
    if command -v uv &> /dev/null; then
        UV_VERSION=$(uv --version)
        echo "✓ uv successfully installed: $UV_VERSION"
    else
        echo "❌ Failed to install uv"
        exit 1
    fi
fi

brew install python3
brew install uv

# Step 2.5: Fix Python version compatibility for fastmcp
echo "Step 2.5: Ensuring Python 3.10+ compatibility..."

# Check if newer Python versions are available but not linked
PYTHON_LINKED=false

# Try to link Python 3.13 first
if brew list python@3.13 &> /dev/null; then
    echo "Found Python 3.13 installed via Homebrew, linking..."
    brew link --overwrite python@3.13 2>/dev/null || echo "Python 3.13 link may already exist"
    PYTHON_LINKED=true
elif brew list python@3.12 &> /dev/null; then
    echo "Found Python 3.12 installed via Homebrew, linking..."
    brew link --overwrite python@3.12 2>/dev/null || echo "Python 3.12 link may already exist"
    PYTHON_LINKED=true
elif brew list python@3.11 &> /dev/null; then
    echo "Found Python 3.11 installed via Homebrew, linking..."
    brew link --overwrite python@3.11 2>/dev/null || echo "Python 3.11 link may already exist"
    PYTHON_LINKED=true
elif brew list python@3.10 &> /dev/null; then
    echo "Found Python 3.10 installed via Homebrew, linking..."
    brew link --overwrite python@3.10 2>/dev/null || echo "Python 3.10 link may already exist"
    PYTHON_LINKED=true
fi

# Verify Python version after linking
PYTHON_VERSION_AFTER=$(python3 --version | grep -o '[0-9]\+\.[0-9]\+' | head -1)
MAJOR_VERSION=$(echo $PYTHON_VERSION_AFTER | cut -d. -f1)
MINOR_VERSION=$(echo $PYTHON_VERSION_AFTER | cut -d. -f2)

if [[ $MAJOR_VERSION -eq 3 && $MINOR_VERSION -ge 10 ]]; then
    echo "✓ Python version is now compatible: $(python3 --version)"
elif [[ $MAJOR_VERSION -gt 3 ]]; then
    echo "✓ Python version is now compatible: $(python3 --version)"
else
    echo "⚠️  Warning: Python version $(python3 --version) may not be compatible with fastmcp"
    echo "   fastmcp requires Python 3.10 or higher"
    echo "   Installing Python 3.12 via Homebrew..."
    brew install python@3.12
    brew link --overwrite python@3.12
    echo "✓ Python 3.12 installed and linked"
fi

# Step 3: Create VenturaMCP directory in Documents folder
echo "Step 3: Creating VenturaMCP directory..."

VENTURA_DIR="$HOME/Documents"
cd "$VENTURA_DIR"
uv init VenturaMCP
VENTURA_DIR="$HOME/Documents/VenturaMCP"

cd "$VENTURA_DIR"

# Use the correct Python version for virtual environment
echo "Creating virtual environment with $(python3 --version)..."
python3 -m venv venv
source venv/bin/activate

# Verify virtual environment Python version
echo "Virtual environment Python version: $(python --version)"

# Step 6: Install fastmcp using uv
echo "Step 6: Installing fastmcp package..."

uv pip install fastmcp

if [ $? -eq 0 ]; then
    echo "✓ fastmcp installed successfully"
else
    echo "❌ Failed to install fastmcp"
    echo "Current Python version in venv: $(python --version)"
    echo "Please ensure Python 3.10 or higher is being used"
    exit 1
fi

# Step 7: Create client_proxy.py file
echo "Creating client_proxy.py..."
cat > client_proxy.py << 'EOF'
import asyncio
from fastmcp import Client, FastMCP

async def run():
    async with Client("https://mcp.venturasecurities.com/mcp") as connected_client:
        proxy = FastMCP.as_proxy(connected_client)
        await proxy.run_stdio_async()


if __name__ == "__main__":
    asyncio.run(run())
EOF

echo "client_proxy.py created successfully."


# Detect architecture and download appropriate Claude Desktop
echo
echo "Detecting system architecture..."

ARCH=$(uname -m)
echo "Architecture detected: $ARCH"


#!/bin/bash
# ==========================================
# CLAUDE DESKTOP INSTALLATION - macOS ONLY
# ==========================================

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
CLAUDE_APP_PATH="/Applications/Claude.app"
CLAUDE_DMG_URL="https://storage.googleapis.com/osprey-downloads-c02f6a0d-347c-492b-a752-3e0651722e97/nest/Claude.dmg"

log() {
    echo -e "${BLUE}[INSTALLER]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

download_file() {
    local url="$1"
    local output_path="$2"

    log "Downloading from $url..."

    if command -v curl &> /dev/null; then
        curl -L -o "$output_path" "$url" --progress-bar
    elif command -v wget &> /dev/null; then
        wget -O "$output_path" "$url" --progress=bar
    else
        log_error "Neither curl nor wget found. Please install one of them."
        return 1
    fi

    log_success "Download completed"
}

download_claude_desktop() {
    log "Downloading Claude Desktop..."

    local installer_path="/tmp/Claude.dmg"

    if download_file "$CLAUDE_DMG_URL" "$installer_path"; then
        log_success "Claude Desktop downloaded to: $installer_path"
        return 0
    else
        return 1
    fi
}

update_claude_config() {
    local username="${1:-$(whoami)}"

    local python_command="$HOME/Documents/VenturaMCP/venv/bin/python3"
    local client_script="$HOME/Documents/VenturaMCP/client_proxy.py"
    local config_path="/Users/$username/Library/Application Support/Claude/claude_desktop_config.json"

    echo "Updating Claude Desktop configuration..."
    echo "Config path: $config_path"
    echo "Python command: $python_command"
    echo "Client script: $client_script"

    # Ensure config directory exists
    sudo mkdir -p "$(dirname "$config_path")"

    # Write the configuration
    sudo tee "$config_path" > /dev/null << EOF
{
  "mcpServers": {
    "ventura-spotlight": {
      "command": "uv",
      "args": ["run", "$python_command", "$client_script"],
      "env": {}
    }
  }
}
EOF

    echo "Claude Desktop configuration updated successfully"
}


install_claude_desktop_mac() {
    local installer_path="/tmp/Claude.dmg"

    log "Installing Claude Desktop on macOS..."

    # Verify DMG file exists
    if [[ ! -f "$installer_path" ]]; then
        log_error "DMG file not found: $installer_path"
        return 1
    fi

    # Verify DMG file size (should be > 1MB)
    local file_size=$(stat -f%z "$installer_path" 2>/dev/null || echo "0")
    if [[ $file_size -lt 1048576 ]]; then
        log_error "DMG file appears to be too small or corrupted (${file_size} bytes)"
        return 1
    fi

    log_success "DMG file verified ($(( file_size / 1048576 )) MB)"

    # Mount DMG
    log "Mounting DMG..."
    hdiutil detach /Volumes/Claude
    local mount_output
    if ! mount_output=$(hdiutil attach "$installer_path" -nobrowse 2>/dev/null); then
        log_error "Failed to mount DMG"
        return 1
    fi

    # Debugging mount output
    echo "Mount Output: $mount_output"  # Add this line to print the output

    # Extract mount point from hdiutil output
    local mount_point=$(echo "$mount_output" | grep '/Volumes' | awk '{print $NF}')

    if [[ -z "$mount_point" ]]; then
        log_error "Could not find mount point in hdiutil output"
        return 1
    fi

    log_success "DMG mounted at: $mount_point"


    # Find and copy Claude.app
    local app_file=$(find "$mount_point" -name "*.app" -type d | head -1)

    if [[ -z "$app_file" ]]; then
        hdiutil detach "$mount_point" -quiet 2>/dev/null
        log_error "Claude.app not found in DMG"
        return 1
    fi

    log "Found Claude app at: $app_file"

    # Remove existing Claude.app if it exists
    if [[ -d "$CLAUDE_APP_PATH" ]]; then
        log "Removing existing Claude.app..."
        if ! sudo rm -rf "$CLAUDE_APP_PATH"; then
            log_error "Failed to remove existing Claude.app"
            hdiutil detach "$mount_point" -quiet 2>/dev/null
            return 1
        fi
        log_success "Removed existing Claude.app"
    fi

    # Copy to Applications using ditto (preserves permissions and metadata)
    log "Installing Claude to Applications..."
    if sudo ditto "$app_file" "$CLAUDE_APP_PATH"; then
        sudo xattr -d com.apple.quarantine "/Applications/Claude.app"
        log_success "Claude copied successfully with ditto"
    else
        log_error "Failed to copy Claude to Applications"
        hdiutil detach "$mount_point" -quiet 2>/dev/null
        return 1
    fi

    # Set proper permissions
    log "Setting permissions..."
    if sudo chmod -R 755 "$CLAUDE_APP_PATH"; then
        log_success "Permissions set successfully"
    else
        log_warning "Could not set permissions, but installation may still work"
    fi

    # Unmount DMG
    log "Unmounting DMG..."
    if hdiutil detach "$mount_point" -quiet 2>/dev/null; then
        log_success "DMG unmounted successfully"
    else
        log_warning "Could not unmount DMG cleanly"
    fi

    # Clean up installer
    rm -f "$installer_path"

    # Verify installation
    if [[ -d "$CLAUDE_APP_PATH" ]] && [[ -f "$CLAUDE_APP_PATH/Contents/MacOS/Claude" ]]; then
        log_success "Claude Desktop installation completed successfully"
        log_success "Claude.app installed at: $CLAUDE_APP_PATH"
        return 0
    else
        log_error "Installation verification failed - Claude.app not found or incomplete"
        return 1
    fi
}

install_claude_desktop() {
    log "Starting Claude Desktop installation..."

    # Check if we're on macOS
    if [[ "$(uname -s)" != "Darwin" ]]; then
        log_error "This script is for macOS only"
        return 1
    fi

    # Download Claude Desktop
    if download_claude_desktop; then
        # Install Claude Desktop
        install_claude_desktop_mac
    else
        log_error "Failed to download Claude Desktop"
        return 1
    fi
}

echo "=========================================="
echo "    Claude Desktop Installer - macOS"
echo "=========================================="
echo ""

log "macOS version: $(sw_vers -productVersion)"
log "Architecture: $(uname -m)"
echo ""
#update_claude_config
# Run installation
if install_claude_desktop; then
    echo ""
    echo "=========================================="
    log_success "🎉 Installation completed successfully!"
    echo "=========================================="
    echo ""
    log_success "Claude Desktop is now installed"
    log_success "Location: $CLAUDE_APP_PATH"
    log_success "You can find Claude in your Applications folder"
    echo ""
    echo "To launch Claude Desktop:"
    echo "  - Open Applications folder"
    echo "  - Double-click Claude.app"
    echo "  - Or use Spotlight: Cmd+Space, type 'Claude'"
    echo ""
    update_claude_config
    nohup /Applications/Claude.app/Contents/MacOS/Claude >/dev/null 2>&1 &

else
    echo ""
    echo "=========================================="
    log_error "❌ Installation failed!"
    echo "=========================================="
    echo ""
    log_error "Claude Desktop installation was not successful"
    echo ""
    echo "Manual installation steps:"
    echo "1. Download Claude Desktop from: https://claude.ai/desktop"
    echo "2. Open the downloaded DMG file"
    echo "3. Drag Claude.app to your Applications folder"
    echo ""
    exit 1
fi

echo
echo "===================================="
echo "Setup Complete!"
echo "===================================="
echo
echo "VenturaMCP directory: $VENTURA_DIR"
echo "Virtual environment created and activated"
echo "fastmcp installed"
echo "client_proxy.py created"
echo "Claude Desktop downloaded and installed"
echo "Claude Desktop has been installed to /Applications/Claude.app"
echo "You can launch it from Launchpad or Applications folder."
echo "Python version used: $(python3 --version)"

# Add your next steps here

echo "Script completed successfully!"