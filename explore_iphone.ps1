# iPhone Explorer - See what's inside your iPhone
# This will show all folders and help diagnose the issue

$Host.UI.RawUI.BackgroundColor = "Black"
$Host.UI.RawUI.ForegroundColor = "Green"
Clear-Host

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "iPhone Explorer - Diagnostic Tool" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

function Write-Status {
    param([string]$Message, [string]$Type = "Info")
    switch ($Type) {
        "Success" { Write-Host "[+] $Message" -ForegroundColor Green }
        "Error"   { Write-Host "[!] $Message" -ForegroundColor Red }
        "Warning" { Write-Host "[*] $Message" -ForegroundColor Yellow }
        "Info"    { Write-Host "[*] $Message" -ForegroundColor Cyan }
    }
}

# Find iPhone
Write-Status "Searching for iPhone..." "Info"

$shell = New-Object -ComObject Shell.Application
$computer = $shell.NameSpace(17)

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
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "iPhone Contents:" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# List all folders in iPhone
$iphoneFolder = $shell.NameSpace($iphone.GetFolder)

Write-Status "Root folders in iPhone:" "Info"
Write-Host ""

$folders = @()
foreach ($item in $iphoneFolder.Items()) {
    $type = if ($item.IsFolder) { "FOLDER" } else { "FILE" }
    Write-Host "  [$type] $($item.Name)" -ForegroundColor $(if ($item.IsFolder) { "Yellow" } else { "Gray" })
    
    if ($item.IsFolder) {
        $folders += $item
    }
}

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Status "Exploring each folder..." "Info"
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

foreach ($folder in $folders) {
    Write-Host ""
    Write-Host ">>> $($folder.Name)" -ForegroundColor Yellow
    Write-Host "    " -NoNewline
    Write-Host ("=" * 50) -ForegroundColor DarkGray
    
    try {
        $subFolder = $shell.NameSpace($folder.GetFolder)
        
        $itemCount = 0
        foreach ($item in $subFolder.Items()) {
            $itemCount++
            if ($itemCount -le 20) {  # Show first 20 items
                $type = if ($item.IsFolder) { "FOLDER" } else { "FILE" }
                Write-Host "    [$type] $($item.Name)" -ForegroundColor $(if ($item.IsFolder) { "Cyan" } else { "White" })
            }
        }
        
        if ($itemCount -gt 20) {
            Write-Host "    ... and $($itemCount - 20) more items" -ForegroundColor DarkGray
        }
        
        if ($itemCount -eq 0) {
            Write-Host "    (Empty)" -ForegroundColor DarkGray
        }
        
    } catch {
        Write-Host "    (Cannot access - iPhone may be locked)" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Status "Diagnostic Information:" "Info"
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Check for common photo locations
$photoLocations = @(
    "Internal Storage\DCIM",
    "DCIM",
    "Photos",
    "Camera Roll",
    "Internal Storage"
)

Write-Status "Checking common photo locations:" "Info"
Write-Host ""

foreach ($location in $photoLocations) {
    Write-Host "  Checking: $location ... " -NoNewline
    
    # Try to find this path
    $found = $false
    foreach ($folder in $folders) {
        if ($folder.Name -eq $location -or $folder.Name -like "*$location*") {
            Write-Host "FOUND" -ForegroundColor Green
            $found = $true
            break
        }
    }
    
    if (-not $found) {
        Write-Host "NOT FOUND" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host ""
Write-Host "============================================================" -ForegroundColor Yellow
Write-Status "Possible Issues:" "Warning"
Write-Host "============================================================" -ForegroundColor Yellow
Write-Host ""

Write-Host "1. iPhone may be locked" -ForegroundColor Yellow
Write-Host "   Solution: Unlock your iPhone and keep it unlocked" -ForegroundColor White
Write-Host ""

Write-Host "2. 'Trust This Computer' not tapped" -ForegroundColor Yellow
Write-Host "   Solution: Look at your iPhone screen and tap 'Trust'" -ForegroundColor White
Write-Host ""

Write-Host "3. No photos/videos on iPhone" -ForegroundColor Yellow
Write-Host "   Solution: Take a photo first, then try again" -ForegroundColor White
Write-Host ""

Write-Host "4. Photos are in iCloud, not on device" -ForegroundColor Yellow
Write-Host "   Solution: Download photos from iCloud first" -ForegroundColor White
Write-Host "   Settings > Photos > Download and Keep Originals" -ForegroundColor White
Write-Host ""

Write-Host "5. Windows doesn't have permission" -ForegroundColor Yellow
Write-Host "   Solution: Disconnect and reconnect iPhone" -ForegroundColor White
Write-Host "   Then unlock and trust again" -ForegroundColor White
Write-Host ""

Write-Host ""
Write-Status "Try these steps:" "Info"
Write-Host ""
Write-Host "  1. Disconnect iPhone from USB" -ForegroundColor Cyan
Write-Host "  2. Unlock iPhone" -ForegroundColor Cyan
Write-Host "  3. Reconnect to USB" -ForegroundColor Cyan
Write-Host "  4. Tap 'Trust This Computer' on iPhone" -ForegroundColor Cyan
Write-Host "  5. Keep iPhone unlocked" -ForegroundColor Cyan
Write-Host "  6. Run this script again" -ForegroundColor Cyan
Write-Host ""

Read-Host "Press Enter to exit"
