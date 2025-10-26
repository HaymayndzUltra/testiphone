# iPhone Media Restore Tool - PowerShell Version
# Advanced version with progress bars and detailed logging

param(
    [string]$OutputPath = "$env:USERPROFILE\Desktop\iPhone_Restored_Media",
    [switch]$IncludeMetadata,
    [switch]$OrganizeByDate
)

# Set console colors
$Host.UI.RawUI.BackgroundColor = "Black"
$Host.UI.RawUI.ForegroundColor = "Green"
Clear-Host

# Banner
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "iPhone Media Restore Tool - PowerShell Edition" -ForegroundColor Cyan
Write-Host "Restore photos and videos from iPhone via USB" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Function to write colored output
function Write-Status {
    param(
        [string]$Message,
        [string]$Type = "Info"
    )
    
    switch ($Type) {
        "Success" { Write-Host "[+] $Message" -ForegroundColor Green }
        "Error"   { Write-Host "[!] $Message" -ForegroundColor Red }
        "Warning" { Write-Host "[*] $Message" -ForegroundColor Yellow }
        "Info"    { Write-Host "[*] $Message" -ForegroundColor Cyan }
    }
}

# Function to detect iPhone
function Find-iPhone {
    Write-Status "Detecting iPhone..." "Info"
    
    # Check all removable drives
    $drives = Get-PSDrive -PSProvider FileSystem | Where-Object { 
        $_.Root -match '^[D-Z]:\\$' 
    }
    
    foreach ($drive in $drives) {
        $dcimPath = Join-Path $drive.Root "DCIM"
        if (Test-Path $dcimPath) {
            Write-Status "Found iPhone at drive $($drive.Root)" "Success"
            return $drive.Root
        }
    }
    
    # Check for iPhone in portable devices
    $shell = New-Object -ComObject Shell.Application
    $portableDevices = $shell.NameSpace(17) # Computer namespace
    
    foreach ($item in $portableDevices.Items()) {
        if ($item.Name -like "*iPhone*" -or $item.Name -like "*Apple*") {
            Write-Status "Found iPhone: $($item.Name)" "Success"
            return $item
        }
    }
    
    return $null
}

# Function to copy files with progress
function Copy-MediaFiles {
    param(
        [string]$SourcePath,
        [string]$DestPath,
        [string[]]$Extensions,
        [string]$MediaType
    )
    
    Write-Status "Searching for $MediaType files..." "Info"
    
    # Get all files matching extensions
    $files = @()
    foreach ($ext in $Extensions) {
        $found = Get-ChildItem -Path $SourcePath -Filter "*.$ext" -Recurse -ErrorAction SilentlyContinue
        $files += $found
    }
    
    if ($files.Count -eq 0) {
        Write-Status "No $MediaType files found" "Warning"
        return 0
    }
    
    Write-Status "Found $($files.Count) $MediaType files" "Success"
    
    # Copy files with progress
    $copied = 0
    $failed = 0
    
    foreach ($file in $files) {
        $progress = [math]::Round(($copied / $files.Count) * 100, 2)
        Write-Progress -Activity "Copying $MediaType" -Status "$copied of $($files.Count) files" -PercentComplete $progress
        
        try {
            $destFile = Join-Path $DestPath $file.Name
            
            # Handle duplicate filenames
            $counter = 1
            while (Test-Path $destFile) {
                $nameWithoutExt = [System.IO.Path]::GetFileNameWithoutExtension($file.Name)
                $extension = [System.IO.Path]::GetExtension($file.Name)
                $destFile = Join-Path $DestPath "$nameWithoutExt`_$counter$extension"
                $counter++
            }
            
            Copy-Item -Path $file.FullName -Destination $destFile -Force
            $copied++
            
            # Organize by date if requested
            if ($OrganizeByDate) {
                $date = $file.LastWriteTime.ToString("yyyy-MM")
                $dateFolder = Join-Path $DestPath $date
                
                if (-not (Test-Path $dateFolder)) {
                    New-Item -ItemType Directory -Path $dateFolder -Force | Out-Null
                }
                
                Move-Item -Path $destFile -Destination $dateFolder -Force
            }
            
        } catch {
            Write-Status "Failed to copy: $($file.Name) - $($_.Exception.Message)" "Error"
            $failed++
        }
    }
    
    Write-Progress -Activity "Copying $MediaType" -Completed
    
    Write-Status "Copied: $copied, Failed: $failed" "Info"
    return $copied
}

# Function to create summary report
function New-RestoreReport {
    param(
        [string]$OutputPath,
        [int]$PhotoCount,
        [int]$VideoCount,
        [datetime]$StartTime,
        [datetime]$EndTime
    )
    
    $duration = $EndTime - $StartTime
    $reportPath = Join-Path $OutputPath "restore_report.txt"
    
    $report = @"
iPhone Media Restore Report
============================

Date: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")
Duration: $($duration.ToString("hh\:mm\:ss"))

Files Restored:
- Photos: $PhotoCount
- Videos: $VideoCount
- Total: $($PhotoCount + $VideoCount)

Output Location: $OutputPath

System Information:
- Computer: $env:COMPUTERNAME
- User: $env:USERNAME
- OS: $([System.Environment]::OSVersion.VersionString)
- PowerShell: $($PSVersionTable.PSVersion.ToString())

"@
    
    $report | Out-File -FilePath $reportPath -Encoding UTF8
    Write-Status "Report saved to: $reportPath" "Success"
}

# Main script
try {
    $startTime = Get-Date
    
    # Check prerequisites
    Write-Status "Checking prerequisites..." "Info"
    
    # Create output directories
    Write-Status "Creating output directories..." "Info"
    $photosPath = Join-Path $OutputPath "photos"
    $videosPath = Join-Path $OutputPath "videos"
    
    New-Item -ItemType Directory -Path $photosPath -Force | Out-Null
    New-Item -ItemType Directory -Path $videosPath -Force | Out-Null
    
    Write-Status "Output directory: $OutputPath" "Success"
    Write-Host ""
    
    # Detect iPhone
    Write-Status "Please ensure:" "Warning"
    Write-Status "  1. iPhone is connected via USB" "Warning"
    Write-Status "  2. iPhone is unlocked" "Warning"
    Write-Status "  3. You tapped 'Trust This Computer' on iPhone" "Warning"
    Write-Host ""
    
    $iphonePath = Find-iPhone
    
    if (-not $iphonePath) {
        Write-Status "iPhone not detected!" "Error"
        Write-Host ""
        Write-Status "Troubleshooting:" "Warning"
        Write-Status "  1. Try a different USB cable" "Info"
        Write-Status "  2. Try a different USB port" "Info"
        Write-Status "  3. Restart your iPhone" "Info"
        Write-Status "  4. Restart your computer" "Info"
        Write-Status "  5. Reinstall iTunes" "Info"
        Write-Host ""
        Read-Host "Press Enter to exit"
        exit 1
    }
    
    # Get DCIM path
    $dcimPath = Join-Path $iphonePath "DCIM"
    
    if (-not (Test-Path $dcimPath)) {
        Write-Status "DCIM folder not found!" "Error"
        Write-Status "iPhone may not be properly connected or trusted" "Warning"
        Read-Host "Press Enter to exit"
        exit 1
    }
    
    Write-Host ""
    Write-Status "Ready to restore media files" "Success"
    Write-Status "This may take several minutes depending on file count" "Info"
    Write-Host ""
    
    $confirm = Read-Host "Continue? (Y/N)"
    if ($confirm -ne "Y" -and $confirm -ne "y") {
        Write-Status "Cancelled by user" "Warning"
        exit 0
    }
    
    Write-Host ""
    Write-Host "============================================================" -ForegroundColor Cyan
    Write-Status "Starting media restore..." "Info"
    Write-Host "============================================================" -ForegroundColor Cyan
    Write-Host ""
    
    # Photo extensions
    $photoExtensions = @("jpg", "jpeg", "png", "heic", "heif", "gif", "bmp")
    $photoCount = Copy-MediaFiles -SourcePath $dcimPath -DestPath $photosPath -Extensions $photoExtensions -MediaType "photo"
    
    Write-Host ""
    
    # Video extensions
    $videoExtensions = @("mp4", "mov", "m4v", "avi", "3gp")
    $videoCount = Copy-MediaFiles -SourcePath $dcimPath -DestPath $videosPath -Extensions $videoExtensions -MediaType "video"
    
    Write-Host ""
    
    # Create report
    $endTime = Get-Date
    New-RestoreReport -OutputPath $OutputPath -PhotoCount $photoCount -VideoCount $videoCount -StartTime $startTime -EndTime $endTime
    
    # Summary
    Write-Host ""
    Write-Host "============================================================" -ForegroundColor Green
    Write-Host "[+] Media restore completed successfully!" -ForegroundColor Green
    Write-Host "============================================================" -ForegroundColor Green
    Write-Host ""
    Write-Status "Photos restored: $photoCount" "Success"
    Write-Status "Videos restored: $videoCount" "Success"
    Write-Status "Total files: $($photoCount + $videoCount)" "Success"
    Write-Host ""
    Write-Status "Location: $OutputPath" "Info"
    Write-Host ""
    
    # Open output folder
    Write-Status "Opening output folder..." "Info"
    Start-Process explorer.exe -ArgumentList $OutputPath
    
    Write-Host ""
    Write-Status "You can now safely disconnect your iPhone" "Success"
    Write-Host ""
    
} catch {
    Write-Status "An error occurred: $($_.Exception.Message)" "Error"
    Write-Host ""
    Write-Host $_.ScriptStackTrace -ForegroundColor Red
    Write-Host ""
} finally {
    Read-Host "Press Enter to exit"
}
