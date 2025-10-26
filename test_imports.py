#!/usr/bin/env python3

# Test script to check if all required modules are available
modules_to_test = [
    'cryptography',
    'cryptography.fernet',
    'aiohttp',
    'sqlite3',
    'asyncio',
    'json',
    'base64',
    'hashlib',
    'time',
    'datetime',
    'pathlib',
    'typing'
]

print("Testing Python module imports...")
print(f"Python executable: {__import__('sys').executable}")
print(f"Python version: {__import__('sys').version}")
print()

missing_modules = []

for module in modules_to_test:
    try:
        if '.' in module:
            # Handle nested imports like cryptography.fernet
            parts = module.split('.')
            parent = __import__(parts[0])
            try:
                child = getattr(parent, parts[1])
                print(f"✓ {module}")
            except AttributeError:
                # Try importing the submodule directly
                __import__(module)
                print(f"✓ {module}")
        else:
            __import__(module)
            print(f"✓ {module}")
    except ImportError as e:
        print(f"✗ {module} - ERROR: {e}")
        missing_modules.append(module)

print()
if missing_modules:
    print(f"Missing modules: {missing_modules}")
    print("Install with: pip install " + " ".join(missing_modules))
else:
    print("All required modules are available!")
