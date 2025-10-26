#!/usr/bin/env python3
"""Create demo exfiltrated data for testing"""

from pathlib import Path
import json
from datetime import datetime

device_id = "00008030-001234567890ABCD"

# Create directories
photos_dir = Path(f"exfiltrated_data/{device_id}/photos")
messages_dir = Path(f"exfiltrated_data/{device_id}/messages")
photos_dir.mkdir(parents=True, exist_ok=True)
messages_dir.mkdir(parents=True, exist_ok=True)

print("[*] Creating demo exfiltrated data...")

# Create demo photo metadata
photo_metadata = {
    "photo_001.jpg": {
        "size": "2.5 MB",
        "date": "2025-01-20 14:30:00",
        "location": {"lat": 14.5995, "lon": 120.9842},
        "camera": "iPhone 15 Pro"
    },
    "photo_002.jpg": {
        "size": "3.1 MB",
        "date": "2025-01-21 09:15:00",
        "location": {"lat": 14.6091, "lon": 121.0223},
        "camera": "iPhone 15 Pro"
    },
    "photo_003.jpg": {
        "size": "2.8 MB",
        "date": "2025-01-22 16:45:00",
        "location": {"lat": 14.5547, "lon": 121.0244},
        "camera": "iPhone 15 Pro"
    }
}

(photos_dir / "photo_metadata.json").write_text(json.dumps(photo_metadata, indent=2))
print(f"[+] Created photo metadata: {len(photo_metadata)} photos")

# Create demo messages
messages = [
    {
        "id": 1,
        "sender": "+639171234567",
        "text": "Hey, kumusta ka na?",
        "date": "2025-01-25 10:30:00",
        "type": "received"
    },
    {
        "id": 2,
        "sender": "Me",
        "text": "Okay lang, ikaw?",
        "date": "2025-01-25 10:32:00",
        "type": "sent"
    },
    {
        "id": 3,
        "sender": "+639181234567",
        "text": "Tara kain later?",
        "date": "2025-01-25 12:15:00",
        "type": "received"
    },
    {
        "id": 4,
        "sender": "Me",
        "text": "Sige, anong oras?",
        "date": "2025-01-25 12:16:00",
        "type": "sent"
    },
    {
        "id": 5,
        "sender": "+639181234567",
        "text": "6pm sa usual place",
        "date": "2025-01-25 12:18:00",
        "type": "received"
    }
]

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
(messages_dir / f"messages_{timestamp}.json").write_text(json.dumps(messages, indent=2))
print(f"[+] Created messages: {len(messages)} messages")

# Create demo contacts
contacts = [
    {"name": "Juan Dela Cruz", "phone": "+639171234567", "email": "juan@email.com"},
    {"name": "Maria Santos", "phone": "+639181234567", "email": "maria@email.com"},
    {"name": "Pedro Reyes", "phone": "+639191234567", "email": "pedro@email.com"},
    {"name": "Ana Garcia", "phone": "+639201234567", "email": "ana@email.com"}
]

(Path(f"exfiltrated_data/{device_id}") / f"contacts_{timestamp}.json").write_text(
    json.dumps(contacts, indent=2)
)
print(f"[+] Created contacts: {len(contacts)} contacts")

# Create demo location tracking
locations = [
    {
        "timestamp": "2025-01-26 08:00:00",
        "latitude": 14.5995,
        "longitude": 120.9842,
        "accuracy": 10,
        "location": "Makati City"
    },
    {
        "timestamp": "2025-01-26 12:00:00",
        "latitude": 14.6091,
        "longitude": 121.0223,
        "accuracy": 8,
        "location": "Mandaluyong City"
    },
    {
        "timestamp": "2025-01-26 18:00:00",
        "latitude": 14.5547,
        "longitude": 121.0244,
        "accuracy": 12,
        "location": "Pasig City"
    }
]

tracking_dir = Path("tracking")
tracking_dir.mkdir(exist_ok=True)

for loc in locations:
    ts = loc['timestamp'].replace(':', '').replace(' ', '_').replace('-', '')
    (tracking_dir / f"location_{ts}.json").write_text(json.dumps(loc, indent=2))

print(f"[+] Created location tracking: {len(locations)} locations")

print("\n" + "="*60)
print("[+] Demo data created successfully!")
print("="*60)
print(f"\nData location:")
print(f"  Photos: exfiltrated_data/{device_id}/photos/")
print(f"  Messages: exfiltrated_data/{device_id}/messages/")
print(f"  Contacts: exfiltrated_data/{device_id}/")
print(f"  Tracking: tracking/")
print("\nYou can now view the exfiltrated data!")
