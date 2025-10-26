# Gabay sa Pag-restore ng Photos at Videos mula sa iPhone

## 📱 Mga Paraan ng Pag-restore

### Paraan 1: Gamit ang Python Script (Pinakamabilis)

#### Mga Kailangan:
- iPhone nakakonekta sa USB
- iTunes installed (para sa Windows)
- Python 3 installed

#### Mga Hakbang:

1. **Ikonekta ang iPhone sa USB**
   ```
   - Isaksak ang iPhone sa USB port ng computer
   - I-unlock ang iPhone
   - Pindutin ang "Trust This Computer" sa iPhone
   ```

2. **Patakbuhin ang Restore Script**
   ```bash
   python restore_iphone_media.py
   ```

3. **Sundin ang mga Prompt**
   ```
   - Ilagay ang folder kung saan mo gustong i-save ang files
   - Pindutin Enter para sa default na "restored_media"
   - Hintayin na matapos ang pag-copy
   ```

4. **Makikita mo ang Results**
   ```
   restored_media/
   ├── photos/          # Lahat ng larawan
   │   ├── IMG_0001.jpg
   │   ├── IMG_0002.heic
   │   └── ...
   └── videos/          # Lahat ng video
       ├── VID_0001.mp4
       ├── VID_0002.mov
       └── ...
   ```

---

### Paraan 2: Gamit ang Windows Photos App (Para sa Windows)

#### Mga Hakbang:

1. **Ikonekta ang iPhone**
   - Isaksak sa USB
   - I-unlock ang iPhone
   - Trust the computer

2. **Buksan ang Photos App**
   - Pindutin ang Windows key
   - I-type "Photos"
   - Buksan ang Photos app

3. **Import ang Media**
   ```
   - Click ang "Import" button sa taas
   - Piliin ang "From a USB device"
   - Piliin ang iyong iPhone
   - Select ang photos/videos na gusto mong i-restore
   - Click "Import selected" o "Import all"
   ```

4. **Piliin ang Destination**
   ```
   - Click "Import settings"
   - Piliin kung saan mo gustong i-save
   - Default: C:\Users\[YourName]\Pictures\
   ```

---

### Paraan 3: Gamit ang iTunes Backup (Para sa Lahat ng Files)

#### Mga Hakbang:

1. **I-backup ang iPhone**
   ```
   - Buksan ang iTunes
   - Ikonekta ang iPhone
   - Click ang iPhone icon
   - Sa "Backups" section:
     - Piliin "This computer"
     - Click "Back Up Now"
   ```

2. **Hintayin ang Backup**
   ```
   - Makikita mo ang progress bar
   - Huwag tanggalin ang iPhone habang nag-ba-backup
   - Tapos na kapag nakita mo "Latest Backup: Today [time]"
   ```

3. **Hanapin ang Backup Files**
   ```
   Windows:
   C:\Users\[YourName]\AppData\Roaming\Apple Computer\MobileSync\Backup\
   
   Mac:
   ~/Library/Application Support/MobileSync/Backup/
   ```

4. **Extract ang Media Files**
   - Gumamit ng iTunes backup extractor tool:
     - **iMazing** (https://imazing.com) - Recommended
     - **iBackup Viewer** (https://www.imactools.com/iphonebackupviewer/)
     - **Dr.Fone** (https://drfone.wondershare.com)

---

### Paraan 4: Gamit ang File Explorer (Windows - Direkta)

#### Mga Hakbang:

1. **Ikonekta ang iPhone**
   - Isaksak sa USB
   - I-unlock at trust the computer

2. **Buksan ang File Explorer**
   - Pindutin Windows + E
   - Hanapin ang "This PC" o "My Computer"

3. **Hanapin ang iPhone**
   ```
   - Makikita mo ang iPhone sa "Devices and drives"
   - Double-click para buksan
   - Buksan ang "Internal Storage"
   - Buksan ang "DCIM" folder
   ```

4. **Copy ang Files**
   ```
   - Makikita mo ang mga folder na:
     - 100APPLE
     - 101APPLE
     - 102APPLE (etc.)
   - Select lahat ng folders
   - Right-click > Copy
   - Paste sa gusto mong location
   ```

---

### Paraan 5: Gamit ang Image Capture (Para sa Mac)

#### Mga Hakbang:

1. **Ikonekta ang iPhone**
   - Isaksak sa USB
   - I-unlock at trust the computer

2. **Buksan ang Image Capture**
   ```
   - Pindutin Command + Space
   - I-type "Image Capture"
   - Pindutin Enter
   ```

3. **Import ang Media**
   ```
   - Piliin ang iPhone sa left sidebar
   - Makikita mo lahat ng photos at videos
   - Para sa lahat: Click "Import All"
   - Para sa specific: Select files then click "Import"
   ```

4. **Piliin ang Destination**
   ```
   - Sa "Import To:" dropdown
   - Piliin ang folder o gumawa ng bago
   - Default: Pictures folder
   ```

---

## 🔧 Troubleshooting (Pag-aayos ng Problema)

### Problem: Hindi Makita ang iPhone

**Solusyon:**
1. **Check ang USB Connection**
   ```
   - Subukan ang ibang USB cable
   - Subukan ang ibang USB port
   - Siguraduhing original o certified cable
   ```

2. **Check ang iPhone Settings**
   ```
   - I-unlock ang iPhone
   - Pindutin "Trust This Computer" ulit
   - Restart ang iPhone
   ```

3. **Check ang Computer**
   ```
   Windows:
   - Siguraduhing naka-install ang iTunes
   - Restart ang Apple Mobile Device Service:
     1. Pindutin Windows + R
     2. I-type "services.msc"
     3. Hanapin "Apple Mobile Device Service"
     4. Right-click > Restart
   
   Mac:
   - Update ang macOS
   - Restart ang computer
   ```

### Problem: "Device is Locked" Error

**Solusyon:**
```
1. I-unlock ang iPhone gamit ang passcode
2. Huwag i-lock habang nag-transfer
3. Disable ang auto-lock temporarily:
   Settings > Display & Brightness > Auto-Lock > Never
```

### Problem: Hindi Makita ang Ilang Photos/Videos

**Solusyon:**
```
1. Check kung naka-sync sa iCloud:
   - Settings > [Your Name] > iCloud > Photos
   - I-download muna from iCloud

2. Check ang "Recently Deleted":
   - Photos app > Albums > Recently Deleted
   - Recover kung nandoon

3. Check ang Hidden albums:
   - Photos app > Albums > Hidden
```

### Problem: Mabagal ang Transfer

**Solusyon:**
```
1. Gumamit ng USB 3.0 port (blue color)
2. Huwag gumamit ng USB hub
3. Close other applications
4. Transfer by batches (konti-konti)
5. Gumamit ng faster USB cable
```

### Problem: "Not Enough Space" Error

**Solusyon:**
```
1. Check available space:
   - Windows: Right-click drive > Properties
   - Mac: Apple menu > About This Mac > Storage

2. Free up space:
   - Delete unnecessary files
   - Move files to external drive
   - Empty Recycle Bin/Trash

3. Transfer to external drive directly:
   - Plug in external hard drive
   - Set as destination folder
```

---

## 💡 Tips at Best Practices

### Para sa Mabilis na Transfer:

1. **Gumamit ng USB 3.0**
   ```
   - Mas mabilis 10x kaysa USB 2.0
   - Blue color ang USB 3.0 ports
   ```

2. **Organize Habang Nag-transfer**
   ```
   - Gumawa ng folders by date:
     - 2024-01-January
     - 2024-02-February
   - O by event:
     - Birthday
     - Vacation
     - Family
   ```

3. **Backup sa Multiple Locations**
   ```
   - Computer hard drive
   - External hard drive
   - Cloud storage (Google Drive, OneDrive)
   ```

### Para sa Seguridad:

1. **Huwag Tanggalin Agad sa iPhone**
   ```
   - Verify muna na complete ang transfer
   - Check kung bukas ang files
   - Gumawa ng backup copy
   ```

2. **Encrypt Sensitive Files**
   ```
   - Gumamit ng password-protected folders
   - O i-compress with password:
     Right-click > Send to > Compressed folder
     Then add password
   ```

---

## 📊 Comparison ng Mga Paraan

| Paraan | Bilis | Difficulty | Pros | Cons |
|--------|-------|------------|------|------|
| Python Script | ⭐⭐⭐⭐⭐ | Medium | Automated, organized | Needs Python |
| Windows Photos | ⭐⭐⭐⭐ | Easy | Built-in, simple | Windows only |
| iTunes Backup | ⭐⭐⭐ | Medium | Complete backup | Needs extraction tool |
| File Explorer | ⭐⭐⭐⭐⭐ | Very Easy | Direct access | Manual organization |
| Image Capture | ⭐⭐⭐⭐⭐ | Very Easy | Built-in Mac app | Mac only |

---

## 🎯 Recommended Workflow

### Para sa Regular Backup:

```
1. Weekly: Gumamit ng Windows Photos o Image Capture
   - Quick at simple
   - Para sa recent photos lang

2. Monthly: Gumamit ng iTunes Backup
   - Complete backup ng lahat
   - Kasama ang settings at data

3. Important Events: Gumamit ng File Explorer
   - Manual selection
   - Organize by event
```

### Para sa One-Time Full Restore:

```
1. Gumamit ng Python Script
   - Automated
   - Organized output
   - Mabilis

2. O gumamit ng File Explorer
   - Copy lahat ng DCIM folders
   - Organize later
```

---

## 📱 Supported File Formats

### Photos:
- **JPG/JPEG** - Standard photos
- **PNG** - Screenshots
- **HEIC/HEIF** - High Efficiency Image (iOS 11+)
- **GIF** - Animated images
- **TIFF** - High quality images

### Videos:
- **MP4** - Standard videos
- **MOV** - QuickTime videos
- **M4V** - iTunes videos
- **AVI** - Alternative format

### Notes:
```
- HEIC files ay mas maliit pero same quality
- Para mabuksan sa Windows:
  1. Install HEIF Image Extensions from Microsoft Store
  2. O convert to JPG using online tools
```

---

## 🆘 Emergency Recovery

### Kung Nawala ang Photos sa iPhone:

1. **Check iCloud**
   ```
   - Go to iCloud.com
   - Login with Apple ID
   - Check Photos
   ```

2. **Check Recently Deleted**
   ```
   - Photos app > Albums > Recently Deleted
   - Recover within 30 days
   ```

3. **Check iTunes Backup**
   ```
   - Kung may backup, pwede i-restore
   - Use backup extraction tool
   ```

4. **Use Recovery Software**
   ```
   - Dr.Fone
   - EaseUS MobiSaver
   - Disk Drill
   ```

---

## 📞 Quick Reference Commands

### Python Script:
```bash
# Basic restore
python restore_iphone_media.py

# Specify output directory
python restore_iphone_media.py
# Then enter: D:\iPhone_Backup
```

### Windows Command Line:
```cmd
# Check if iPhone is connected
dir \\Apple iPhone\Internal Storage\DCIM

# Copy all photos (if drive letter is E:)
xcopy E:\DCIM\*.* D:\iPhone_Photos\ /E /H /C /I
```

### PowerShell:
```powershell
# Find iPhone drive
Get-PSDrive -PSProvider FileSystem

# Copy with progress
Copy-Item -Path "E:\DCIM\*" -Destination "D:\iPhone_Photos\" -Recurse -Verbose
```

---

## ⚠️ Important Reminders

1. **Huwag Tanggalin ang iPhone** habang nag-transfer
2. **I-unlock ang iPhone** during transfer
3. **Gumawa ng Backup** bago mag-restore
4. **Check Available Space** sa computer
5. **Verify ang Files** after transfer
6. **Keep Original Files** sa iPhone hanggang ma-verify

---

## 📚 Additional Resources

### Official Apple Support:
- https://support.apple.com/en-us/HT201302 (Transfer photos)
- https://support.apple.com/en-us/HT204136 (iTunes backup)

### Third-Party Tools:
- **iMazing**: https://imazing.com
- **AnyTrans**: https://www.imobie.com/anytrans/
- **Syncios**: https://www.syncios.com

### Video Tutorials:
- Search YouTube: "How to transfer iPhone photos to PC"
- Search YouTube: "iPhone backup and restore"

---

**Last Updated**: October 26, 2025  
**Compatibility**: iPhone 6 and later, iOS 12+  
**Tested on**: Windows 10/11, macOS 12+

Para sa karagdagang tulong, mag-email sa: support@example.com
