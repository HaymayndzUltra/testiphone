#!/usr/bin/env python3
"""Test direct database insertion"""

import sqlite3
import json
import time

device_id = "00008030-001234567890ABCD"
device_info = {
    'status': {
        'jailbroken': False,
        'ios_version': '17.0'
    },
    'credentials': {},
    'compromise_time': '2025-01-26T23:00:00',
    'method': 'demo'
}

print("[*] Testing direct database insertion...")

try:
    conn = sqlite3.connect('c2_data.db')
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT OR REPLACE INTO devices (device_id, info, registered_at, last_seen, status)
        VALUES (?, ?, ?, ?, ?)
    """, (device_id, json.dumps(device_info), time.time(), time.time(), 'active'))
    
    conn.commit()
    conn.close()
    
    print("[+] Device inserted successfully!")
    
    # Verify
    conn = sqlite3.connect('c2_data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM devices')
    devices = cursor.fetchall()
    conn.close()
    
    print(f"\n[*] Devices in database: {len(devices)}")
    for device in devices:
        print(f"  {device}")
        
except Exception as e:
    print(f"[!] Error: {e}")
    import traceback
    traceback.print_exc()
