#!/usr/bin/env python3
"""
iPhone Media Restore Tool
Restore photos and videos from iPhone connected via USB
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path
from datetime import datetime
import platform

class iPhoneMediaRestore:
    """Restore photos and videos from iPhone via USB"""
    
    def __init__(self, output_dir=None):
        """Initialize restore tool"""
        self.output_dir = output_dir or Path("restored_media")
        self.output_dir = Path(self.output_dir)
        self.system = platform.system()
        
    def check_dependencies(self):
        """Check if required tools are installed"""
        print("[*] Checking dependencies...")
        
        if self.system == "Windows":
            # Check if iTunes or Apple Mobile Device Support is installed
            itunes_paths = [
                r"C:\Program Files\iTunes",
                r"C:\Program Files (x86)\iTunes",
                r"C:\Program Files\Common Files\Apple\Mobile Device Support",
            ]
            
            itunes_found = any(Path(p).exists() for p in itunes_paths)
            
            if not itunes_found:
                print("[!] iTunes or Apple Mobile Device Support not found")
                print("[*] Please install iTunes from: https://www.apple.com/itunes/download/")
                return False
            
            print("[+] iTunes/Apple Mobile Device Support found")
            return True
            
        else:  # Linux/Mac
            # Check for libimobiledevice
            try:
                result = subprocess.run(['which', 'idevice_id'], 
                                      capture_output=True, text=True)
                if result.returncode == 0:
                    print("[+] libimobiledevice found")
                    return True
                else:
                    print("[!] libimobiledevice not found")
                    print("[*] Install with:")
                    if self.system == "Darwin":
                        print("    brew install libimobiledevice")
                    else:
                        print("    sudo apt-get install libimobiledevice-utils")
                    return False
            except Exception as e:
                print(f"[!] Error checking dependencies: {e}")
                return False
    
    def detect_device(self):
        """Detect connected iPhone"""
        print("\n[*] Detecting iPhone...")
        
        if self.system == "Windows":
            # On Windows, we'll use the Apple Mobile Device Service
            # Check if device is visible in Windows
            print("[*] Please ensure:")
            print("    1. iPhone is connected via USB")
            print("    2. iPhone is unlocked")
            print("    3. You tapped 'Trust This Computer' on iPhone")
            
            # Try to access iPhone via Windows file system
            # iPhones appear as portable devices
            return self._detect_windows_device()
            
        else:  # Linux/Mac
            try:
                result = subprocess.run(['idevice_id', '-l'], 
                                      capture_output=True, text=True, timeout=10)
                if result.returncode == 0 and result.stdout.strip():
                    device_id = result.stdout.strip().split('\n')[0]
                    print(f"[+] Device detected: {device_id}")
                    return device_id
                else:
                    print("[!] No device detected")
                    print("[*] Please ensure:")
                    print("    1. iPhone is connected via USB")
                    print("    2. iPhone is unlocked")
                    print("    3. You tapped 'Trust This Computer' on iPhone")
                    return None
            except Exception as e:
                print(f"[!] Error detecting device: {e}")
                return None
    
    def _detect_windows_device(self):
        """Detect iPhone on Windows"""
        try:
            # Check for iPhone in portable devices
            # This is a simplified check - in production, you'd use Windows APIs
            print("[*] Checking for iPhone in Windows...")
            
            # Common iPhone mount points in Windows
            possible_paths = []
            
            # Check all drive letters
            for letter in 'DEFGHIJKLMNOPQRSTUVWXYZ':
                drive = f"{letter}:\\"
                if os.path.exists(drive):
                    # Check if it looks like an iPhone
                    dcim_path = os.path.join(drive, "DCIM")
                    if os.path.exists(dcim_path):
                        possible_paths.append(drive)
            
            if possible_paths:
                print(f"[+] Found possible iPhone at: {possible_paths[0]}")
                return possible_paths[0]
            else:
                print("[!] iPhone not detected as drive")
                print("[*] Trying alternative method...")
                return "WINDOWS_DEVICE"
                
        except Exception as e:
            print(f"[!] Error: {e}")
            return None
    
    def restore_photos_videos(self, device_id):
        """Restore photos and videos from iPhone"""
        print(f"\n[*] Starting media restore...")
        
        # Create output directories
        photos_dir = self.output_dir / "photos"
        videos_dir = self.output_dir / "videos"
        photos_dir.mkdir(parents=True, exist_ok=True)
        videos_dir.mkdir(parents=True, exist_ok=True)
        
        if self.system == "Windows":
            return self._restore_windows(device_id, photos_dir, videos_dir)
        else:
            return self._restore_unix(device_id, photos_dir, videos_dir)
    
    def _restore_windows(self, device_id, photos_dir, videos_dir):
        """Restore media on Windows"""
        print("[*] Restoring media on Windows...")
        
        try:
            # Method 1: Direct DCIM access if iPhone is mounted
            if device_id and device_id != "WINDOWS_DEVICE":
                dcim_path = os.path.join(device_id, "DCIM")
                if os.path.exists(dcim_path):
                    return self._copy_from_dcim(dcim_path, photos_dir, videos_dir)
            
            # Method 2: Use Windows Photos app integration
            print("\n[*] Alternative method:")
            print("    1. Open 'Photos' app in Windows")
            print("    2. Click 'Import' button")
            print("    3. Select your iPhone")
            print("    4. Choose photos/videos to import")
            print("    5. Select destination folder")
            
            # Method 3: Use iTunes backup
            print("\n[*] Or use iTunes backup method:")
            print("    1. Open iTunes")
            print("    2. Select your iPhone")
            print("    3. Click 'Back Up Now'")
            print("    4. Backup will be saved to:")
            
            backup_path = Path.home() / "AppData" / "Roaming" / "Apple Computer" / "MobileSync" / "Backup"
            print(f"       {backup_path}")
            
            # Try to find and extract from backup
            if backup_path.exists():
                print(f"\n[*] Found iTunes backup folder")
                return self._extract_from_backup(backup_path, photos_dir, videos_dir)
            
            return False
            
        except Exception as e:
            print(f"[!] Error: {e}")
            return False
    
    def _copy_from_dcim(self, dcim_path, photos_dir, videos_dir):
        """Copy media files from DCIM folder"""
        print(f"[*] Copying from DCIM: {dcim_path}")
        
        photo_count = 0
        video_count = 0
        
        try:
            # Walk through DCIM folder structure
            for root, dirs, files in os.walk(dcim_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    file_ext = os.path.splitext(file)[1].lower()
                    
                    # Photo formats
                    if file_ext in ['.jpg', '.jpeg', '.png', '.heic', '.heif']:
                        dest = photos_dir / file
                        shutil.copy2(file_path, dest)
                        photo_count += 1
                        print(f"[+] Copied photo: {file}")
                    
                    # Video formats
                    elif file_ext in ['.mp4', '.mov', '.m4v', '.avi']:
                        dest = videos_dir / file
                        shutil.copy2(file_path, dest)
                        video_count += 1
                        print(f"[+] Copied video: {file}")
            
            print(f"\n[+] Restore complete!")
            print(f"    Photos: {photo_count}")
            print(f"    Videos: {video_count}")
            print(f"    Location: {self.output_dir}")
            
            return True
            
        except Exception as e:
            print(f"[!] Error copying files: {e}")
            return False
    
    def _restore_unix(self, device_id, photos_dir, videos_dir):
        """Restore media on Linux/Mac"""
        print("[*] Restoring media on Unix system...")
        
        try:
            # Use ifuse to mount iPhone filesystem
            mount_point = Path("/tmp/iphone_mount")
            mount_point.mkdir(exist_ok=True)
            
            print(f"[*] Mounting iPhone at {mount_point}")
            
            # Mount device
            result = subprocess.run(['ifuse', str(mount_point)], 
                                  capture_output=True, text=True)
            
            if result.returncode != 0:
                print("[!] Failed to mount iPhone")
                print("[*] Install ifuse:")
                if self.system == "Darwin":
                    print("    brew install ifuse")
                else:
                    print("    sudo apt-get install ifuse")
                return False
            
            # Copy from DCIM
            dcim_path = mount_point / "DCIM"
            if dcim_path.exists():
                success = self._copy_from_dcim(str(dcim_path), photos_dir, videos_dir)
            else:
                print("[!] DCIM folder not found")
                success = False
            
            # Unmount
            subprocess.run(['fusermount', '-u', str(mount_point)])
            
            return success
            
        except Exception as e:
            print(f"[!] Error: {e}")
            return False
    
    def _extract_from_backup(self, backup_path, photos_dir, videos_dir):
        """Extract media from iTunes backup"""
        print(f"[*] Searching iTunes backups...")
        
        try:
            # Find most recent backup
            backups = [d for d in backup_path.iterdir() if d.is_dir()]
            if not backups:
                print("[!] No backups found")
                return False
            
            latest_backup = max(backups, key=lambda x: x.stat().st_mtime)
            print(f"[+] Found backup: {latest_backup.name}")
            
            # iTunes backups are encrypted and complex to parse
            # Recommend using third-party tools
            print("\n[*] iTunes backups require special tools to extract")
            print("[*] Recommended tools:")
            print("    - iMazing (https://imazing.com)")
            print("    - iBackup Viewer (https://www.imactools.com/iphonebackupviewer/)")
            print("    - Dr.Fone (https://drfone.wondershare.com)")
            
            print(f"\n[*] Backup location: {latest_backup}")
            
            return False
            
        except Exception as e:
            print(f"[!] Error: {e}")
            return False

def main():
    """Main function"""
    print("="*60)
    print("iPhone Media Restore Tool")
    print("Restore photos and videos from iPhone via USB")
    print("="*60)
    
    # Get output directory
    print("\n[*] Where do you want to save restored media?")
    output_dir = input("    Enter path (or press Enter for 'restored_media'): ").strip()
    
    if not output_dir:
        output_dir = "restored_media"
    
    # Initialize restore tool
    restore = iPhoneMediaRestore(output_dir)
    
    # Check dependencies
    if not restore.check_dependencies():
        print("\n[!] Please install required dependencies first")
        return
    
    # Detect device
    device_id = restore.detect_device()
    
    if not device_id:
        print("\n[!] No iPhone detected")
        print("\n[*] Troubleshooting:")
        print("    1. Try a different USB cable")
        print("    2. Try a different USB port")
        print("    3. Restart your iPhone")
        print("    4. Restart your computer")
        print("    5. Reinstall iTunes (Windows) or libimobiledevice (Linux/Mac)")
        return
    
    # Restore media
    print("\n[*] Ready to restore media")
    confirm = input("    Continue? (y/n): ").strip().lower()
    
    if confirm != 'y':
        print("[*] Cancelled")
        return
    
    success = restore.restore_photos_videos(device_id)
    
    if success:
        print("\n" + "="*60)
        print("[+] Media restore completed successfully!")
        print("="*60)
        print(f"\n[*] Files saved to: {Path(output_dir).absolute()}")
    else:
        print("\n[!] Media restore failed or incomplete")
        print("\n[*] Alternative methods:")
        print("    1. Use Windows Photos app (Windows)")
        print("    2. Use Image Capture app (Mac)")
        print("    3. Use iTunes backup + extraction tool")
        print("    4. Use third-party tools like iMazing")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[!] Cancelled by user")
    except Exception as e:
        print(f"\n[!] Error: {e}")
        import traceback
        traceback.print_exc()
