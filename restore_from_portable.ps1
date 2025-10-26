# iPhone Media Restore - Portable Device Version
# Automatically copies from "This PC\Apple iPhone"

param(
    [string]$OutputPath = "$env:USERPROFILE\Desktop\iPhone_Restored_Media"
)

$Host.UI.RawUI.BackgroundColor = "Black"
$Host.UI.RawUI.ForegroundColor = "Green"
Clear-Host

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "iPhone Media Restore - Portable Device Version" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Function to write colored output
function Write-Status {
    param([string]$Message, [string]$Type = "Info")
    switch ($Type) {
        "Success" { Write-Host "[+] $Message" -ForegroundColor Green }
        "Error"   { Write-Host "[!] $Message" -ForegroundColor Red }
        "Warning" { Write-Host "[*] $Message" -ForegroundColor Yellow }
        "Info"    { Write-Host "[*] $Message" -ForegroundColor Cyan }
    }
}

# Find iPhone in Shell namespace
Write-Status "Searching for iPhone..." "Info"

$shell = New-Object -ComObject Shell.Application
$computer = $shell.NameSpace(17) # My Computer

$iphone = $null
foreach ($item in $computer.Items()) {
    if ($item.Name -like "*iPhone*" -or $item.Name -like "*Apple*") {
        $iphone = $item
        Write-Status "Found: $($item.Name)" "Success"
        break
    }
}

if (-not $iphone) {
    Write-Status "iPhone not found!" "Error"
    Write-Host ""
    Write-Status "Please ensure:" "Warning"
    Write-Status "  1. iPhone is connected via USB" "Info"
    Write-Status "  2. iPhone is unlocked" "Info"
    Write-Status "  3. You tapped 'Trust This Computer'" "Info"
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

# Access iPhone folders
Write-Status "Accessing iPhone storage..." "Info"

$iphoneFolder = $shell.NameSpace($iphone.GetFolder)
$internalStorage = $null

foreach ($folder in $iphoneFolder.Items()) {
    if ($folder.Name -eq "Internal Storage") {
        $internalStorage = $folder
        break
    }
}

if (-not $internalStorage) {
    Write-Status "Internal Storage not found!" "Error"
    Write-Status "Make sure iPhone is unlocked" "Warning"
    Read-Host "Press Enter to exit"
    exit 1
}

# Access DCIM folder
$storageFolder = $shell.NameSpace($internalStorage.GetFolder)
$dcim = $null

foreach ($folder in $storageFolder.Items()) {
    if ($folder.Name -eq "DCIM") {
        $dcim = $folder
        break
    }
}

if (-not $dcim) {
    Write-Status "DCIM folder not found!" "Error"
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Status "Found DCIM folder" "Success"
Write-Host ""

# Create output directories
Write-Status "Creating output directories..." "Info"
$photosPath = Join-Path $OutputPath "photos"
$videosPath = Join-Path $OutputPath "videos"

New-Item -ItemType Directory -Path $photosPath -Force | Out-Null
New-Item -ItemType Directory -Path $videosPath -Force | Out-Null

Write-Status "Output: $OutputPath" "Success"
Write-Host ""

# Confirm
Write-Status "Ready to copy media files" "Info"
$confirm = Read-Host "Continue? (Y/N)"

if ($confirm -ne "Y" -and $confirm -ne "y") {
    Write-Status "Cancelled" "Warning"
    exit 0
}

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Status "Copying files..." "Info"
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Copy files from DCIM
$dcimFolder = $shell.NameSpace($dcim.GetFolder)
$photoCount = 0
$videoCount = 0
$totalFiles = 0

# Photo extensions
$photoExts = @('.jpg', '.jpeg', '.png', '.heic', '.heif', '.gif', '.bmp')
$videoExts = @('.mp4', '.mov', '.m4v', '.avi', '.3gp')

foreach ($appleFolder in $dcimFolder.Items()) {
    if ($appleFolder.IsFolder) {
        Write-Status "Processing: $($appleFolder.Name)" "Info"
        
        $appleSubFolder = $shell.NameSpace($appleFolder.GetFolder)
        
        foreach ($file in $appleSubFolder.Items()) {
            $totalFiles++
            $fileName = $file.Name
            $fileExt = [System.IO.Path]::GetExtension($fileName).ToLower()
            
            try {
                if ($photoExts -contains $fileExt) {
                    $destPath = Join-Path $photosPath $fileName
                    
                    # Handle duplicates
                    $counter = 1
                    while (Test-Path $destPath) {
                        $nameWithoutExt = [System.IO.Path]::GetFileNameWithoutExtension($fileName)
                        $destPath = Join-Path $photosPath "$nameWithoutExt`_$counter$fileExt"
                        $counter++
                    }
                    
                    # Copy file using Shell
                    $destFolder = $shell.NameSpace($photosPath)
                    $destFolder.CopyHere($file, 16) # 16 = Yes to All
                    
                    $photoCount++
                    Write-Host "  [+] Photo: $fileName" -ForegroundColor Green
                }
                elseif ($videoExts -contains $fileExt) {
                    $destPath = Join-Path $videosPath $fileName
                    
                    # Handle duplicates
                    $counter = 1
                    while (Test-Path $destPath) {
                        $nameWithoutExt = [System.IO.Path]::GetFileNameWithoutExtension($fileName)
                        $destPath = Join-Path $videosPath "$nameWithoutExt`_$counter$fileExt"
                        $counter++
                    }
                    
                    # Copy file using Shell
                    $destFolder = $shell.NameSpace($videosPath)
                    $destFolder.CopyHere($file, 16)
                    
                    $videoCount++
                    Write-Host "  [+] Video: $fileName" -ForegroundColor Green
                }
            }
            catch {
                Write-Status "Failed: $fileName - $($_.Exception.Message)" "Error"
            }
        }
    }
}

Write-Host ""
Write-Host "============================================================" -ForegroundColor Green
Write-Host "[+] Copy completed!" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Green
Write-Host ""

Write-Status "Photos copied: $photoCount" "Success"
Write-Status "Videos copied: $videoCount" "Success"
Write-Status "Total files: $($photoCount + $videoCount)" "Success"
Write-Host ""
Write-Status "Location: $OutputPath" "Info"
Write-Host ""

# Open folder
Write-Status "Opening output folder..." "Info"
Start-Process explorer.exe -ArgumentList $OutputPath

Write-Host ""
Write-Status "Done! You can now safely disconnect your iPhone." "Success"
Write-Host ""
Read-Host "Press Enter to exit"
