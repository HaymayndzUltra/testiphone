#!/usr/bin/env python3
import sqlite3

conn = sqlite3.connect('c2_data.db')
cursor = conn.cursor()

print("Devices:")
cursor.execute('SELECT * FROM devices')
devices = cursor.fetchall()
for device in devices:
    print(f"  {device}")

print("\nCommands:")
cursor.execute('SELECT * FROM commands')
commands = cursor.fetchall()
for cmd in commands:
    print(f"  {cmd}")

conn.close()
