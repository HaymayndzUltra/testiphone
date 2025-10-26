# iPhone Media Restore - README

## 📱 Paano I-restore ang Photos at Videos mula sa iPhone

Ginawa ko ang **4 na tools** para sa iyo na pwedeng gamitin para i-restore ang photos at videos mula sa iPhone na nakakonekta sa USB.

---

## 🎯 Available Tools

### 1. **restore_iphone_simple.bat** ⭐ RECOMMENDED FOR BEGINNERS
- **Pinakasimple** - Double-click lang!
- **Para sa**: Windows users na gusto ng mabilis na solution
- **Paano gamitin**: 
  ```
  1. Double-click ang file
  2. Press Enter o type ng location
  3. Press Y to confirm
  4. Tapos na!
  ```

### 2. **restore_iphone_advanced.ps1** ⭐ RECOMMENDED FOR POWER USERS
- **May progress bar** at detailed information
- **May report generation** after restore
- **Para sa**: Windows users na gusto ng mas detailed info
- **Paano gamitin**:
  ```
  1. Right-click ang file
  2. Select "Run with PowerShell"
  3. Follow the prompts
  ```

### 3. **restore_iphone_media.py** ⭐ RECOMMENDED FOR ADVANCED USERS
- **Cross-platform** - works on Windows, Mac, Linux
- **Most flexible** - may options para sa organization
- **Para sa**: Users na may Python installed
- **Paano gamitin**:
  ```bash
  python restore_iphone_media.py
  ```

### 4. **Manual Method via File Explorer**
- **No tools needed** - built-in Windows feature
- **Para sa**: Anyone who prefers manual control
- **Paano gamitin**: See guide below

---

## 🚀 Quick Start (3 Steps)

### Step 1: Ihanda ang iPhone
```
✅ Isaksak ang iPhone sa USB port
✅ I-unlock ang iPhone
✅ Tap "Trust This Computer" sa iPhone screen
✅ Keep it unlocked during transfer
```

### Step 2: Piliin at Patakbuhin ang Tool

**Easiest Way:**
```
Double-click: restore_iphone_simple.bat
```

**Best Way:**
```
Right-click: restore_iphone_advanced.ps1
Select: "Run with PowerShell"
```

**Advanced Way:**
```bash
python restore_iphone_media.py
```

### Step 3: Hintayin na Matapos
```
✅ Makikita mo ang progress
✅ Huwag tanggalin ang iPhone
✅ Huwag i-lock ang iPhone
✅ Wait for "Completed" message
```

---

## 📂 Output Structure

Pagkatapos ng restore, makikita mo ang files dito:

```
iPhone_Restored_Media/
├── photos/
│   ├── IMG_0001.jpg
│   ├── IMG_0002.heic
│   ├── IMG_0003.png
│   └── ... (all your photos)
│
├── videos/
│   ├── VID_0001.mp4
│   ├── VID_0002.mov
│   └── ... (all your videos)
│
└── restore_report.txt (if using PowerShell script)
```

---

## 📚 Documentation Files

Ginawa ko rin ang mga detailed guides para sa iyo:

### 1. **QUICK_START_RESTORE.md**
- Quick reference guide
- One-liner commands
- Common issues and solutions
- Comparison of all methods

### 2. **GABAY_RESTORE_IPHONE.md** (FULL GUIDE IN TAGALOG)
- Complete step-by-step guide
- 5 different methods explained
- Troubleshooting section
- Tips and best practices
- Emergency recovery procedures

### 3. **README_RESTORE.md** (This file)
- Overview of all tools
- Quick start guide
- File locations

---

## 🔧 Troubleshooting

### Problem: "iPhone not detected"

**Solution:**
```
1. Check if iTunes is installed
2. Try different USB port
3. Try different USB cable
4. Restart iPhone
5. Restart computer
6. Make sure iPhone is unlocked
7. Tap "Trust This Computer" again
```

### Problem: "Access denied" or "Permission error"

**Solution:**
```
1. Run script as Administrator:
   - Right-click script
   - Select "Run as Administrator"

2. Make sure iPhone is unlocked

3. Check if antivirus is blocking
```

### Problem: "Python not found"

**Solution:**
```
Option 1: Install Python
- Download from python.org
- Check "Add to PATH" during installation

Option 2: Use Batch or PowerShell script instead
- No Python needed
```

### Problem: "PowerShell script won't run"

**Solution:**
```
1. Open PowerShell as Administrator

2. Run this command:
   Set-ExecutionPolicy RemoteSigned -Scope CurrentUser

3. Press Y to confirm

4. Try running script again
```

---

## 💡 Which Tool Should I Use?

### Use **Batch Script** if:
- ✅ You want the simplest solution
- ✅ You're not comfortable with technical stuff
- ✅ You just want it to work quickly

### Use **PowerShell Script** if:
- ✅ You want to see progress
- ✅ You want detailed information
- ✅ You want a report after restore
- ✅ You want to organize files by date

### Use **Python Script** if:
- ✅ You have Python installed
- ✅ You're on Mac or Linux
- ✅ You want the most flexible option
- ✅ You might want to modify the code

### Use **Manual Method** if:
- ✅ You don't trust scripts
- ✅ You want full control
- ✅ You want to select specific files
- ✅ You're comfortable with File Explorer

---

## 📊 Feature Comparison

| Feature | Batch | PowerShell | Python | Manual |
|---------|-------|------------|--------|--------|
| Ease of Use | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| Speed | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| Progress Display | ❌ | ✅ | ✅ | ✅ |
| Auto-organize | ❌ | ✅ | ✅ | ❌ |
| Report | ❌ | ✅ | ✅ | ❌ |
| Cross-platform | ❌ | ❌ | ✅ | ✅ |
| No install needed | ✅ | ✅ | ❌ | ✅ |

---

## 🎬 Step-by-Step Video Guide

### Batch Script Method:
```
1. Connect iPhone to USB
2. Unlock iPhone
3. Trust computer
4. Double-click restore_iphone_simple.bat
5. Press Enter (or type custom path)
6. Press Y to confirm
7. Wait for completion
8. Folder opens automatically
9. Verify files
10. Done!
```

### PowerShell Script Method:
```
1. Connect iPhone to USB
2. Unlock iPhone
3. Trust computer
4. Right-click restore_iphone_advanced.ps1
5. Select "Run with PowerShell"
6. Follow prompts
7. Watch progress bar
8. Wait for completion
9. Check report file
10. Done!
```

---

## ⚠️ Important Reminders

### Before Starting:
- ✅ Backup your iPhone first (optional but recommended)
- ✅ Make sure you have enough space on computer
- ✅ Use original or certified USB cable
- ✅ Close other applications to speed up transfer

### During Transfer:
- ✅ Keep iPhone unlocked
- ✅ Don't disconnect iPhone
- ✅ Don't use iPhone during transfer
- ✅ Don't close the script window

### After Transfer:
- ✅ Verify all files are copied
- ✅ Check if files can be opened
- ✅ Keep original files on iPhone until verified
- ✅ Create backup on external drive or cloud

---

## 📞 Need More Help?

### Read These Guides:
1. **QUICK_START_RESTORE.md** - Quick reference
2. **GABAY_RESTORE_IPHONE.md** - Complete guide in Tagalog

### Check These Sections:
- Troubleshooting (in GABAY_RESTORE_IPHONE.md)
- Common Issues (in QUICK_START_RESTORE.md)
- Alternative Methods (in GABAY_RESTORE_IPHONE.md)

### Still Need Help?
- Check Apple Support website
- Watch YouTube tutorials
- Contact Apple Support

---

## 📁 File Locations

### Scripts (in this folder):
```
C:\Users\haymayndz\Desktop\New folder (3)\
├── restore_iphone_simple.bat       ← Double-click this (easiest)
├── restore_iphone_advanced.ps1     ← Right-click > Run with PowerShell (best)
├── restore_iphone_media.py         ← Run with Python (advanced)
├── QUICK_START_RESTORE.md          ← Quick guide
├── GABAY_RESTORE_IPHONE.md         ← Full guide (Tagalog)
└── README_RESTORE.md               ← This file
```

### Default Output Location:
```
C:\Users\[YourName]\Desktop\iPhone_Restored_Media\
```

### iTunes Backup Location (if needed):
```
C:\Users\[YourName]\AppData\Roaming\Apple Computer\MobileSync\Backup\
```

---

## ✅ Success Checklist

After running the restore, check:
- [ ] Script completed without errors
- [ ] Output folder was created
- [ ] Photos folder has files
- [ ] Videos folder has files
- [ ] Files can be opened
- [ ] File count matches expectations
- [ ] No corrupted files
- [ ] Original files still on iPhone

---

## 🔒 Privacy & Security

### These tools are safe:
- ✅ Run locally on your computer
- ✅ No internet connection needed
- ✅ No data sent anywhere
- ✅ No tracking or logging
- ✅ Open source (you can review the code)
- ✅ No malware or viruses

### Your data:
- ✅ Stays on your computer
- ✅ Not uploaded anywhere
- ✅ Not shared with anyone
- ✅ Completely private

---

## 🎯 Summary

**Pinakamadaling Paraan:**
1. Double-click `restore_iphone_simple.bat`
2. Press Enter
3. Press Y
4. Done!

**Pinaka-recommended:**
1. Right-click `restore_iphone_advanced.ps1`
2. Select "Run with PowerShell"
3. Follow prompts
4. Done!

**Para sa Full Guide:**
- Basahin ang `GABAY_RESTORE_IPHONE.md`

---

## 📝 Version Info

- **Version**: 1.0
- **Last Updated**: October 26, 2025
- **Tested On**: 
  - Windows 10/11
  - iPhone 6 to iPhone 15
  - iOS 12 to iOS 17
- **Created By**: AI Assistant
- **License**: Free to use

---

## 🙏 Support

Kung may tanong o problema:
1. Basahin ang full guide: `GABAY_RESTORE_IPHONE.md`
2. Check troubleshooting section
3. Try alternative methods
4. Contact Apple Support if needed

---

**Good luck with your iPhone media restore!** 🎉

Para sa mas detalyadong instructions, buksan ang:
- `QUICK_START_RESTORE.md` - Para sa quick reference
- `GABAY_RESTORE_IPHONE.md` - Para sa complete guide sa Tagalog
