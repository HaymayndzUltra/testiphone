#!/usr/bin/env python3
"""Test listing devices from C2"""

import asyncio
from c2_server import C2Client

async def main():
    client = C2Client("http://localhost:9443")
    
    print("[*] Fetching devices from C2 server...")
    
    try:
        devices = await client.list_devices()
        
        print(f"\n[+] Found {len(devices)} devices:")
        for device in devices:
            print(f"\n  Device ID: {device['device_id']}")
            print(f"  Status: {'🟢 ONLINE' if device['online'] else '🔴 OFFLINE'}")
            print(f"  Last seen: {device['last_seen']}")
            print(f"  Info: {device['info']}")
            
    except Exception as e:
        print(f"[!] Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
