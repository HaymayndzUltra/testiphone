@echo off
REM iPhone Media Restore - Simple Windows Script
REM Restore photos and videos from iPhone via USB

title iPhone Media Restore Tool
color 0A

echo ============================================================
echo iPhone Media Restore Tool
echo Restore photos and videos from iPhone via USB
echo ============================================================
echo.

REM Check if running as administrator
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo [!] Please run as Administrator for best results
    echo.
)

REM Set default output directory
set "OUTPUT_DIR=%USERPROFILE%\Desktop\iPhone_Restored_Media"

echo [*] Default save location: %OUTPUT_DIR%
echo.
set /p "CUSTOM_DIR=Enter custom path (or press Enter to use default): "

if not "%CUSTOM_DIR%"=="" (
    set "OUTPUT_DIR=%CUSTOM_DIR%"
)

echo.
echo [*] Files will be saved to: %OUTPUT_DIR%
echo.

REM Create output directories
if not exist "%OUTPUT_DIR%" mkdir "%OUTPUT_DIR%"
if not exist "%OUTPUT_DIR%\photos" mkdir "%OUTPUT_DIR%\photos"
if not exist "%OUTPUT_DIR%\videos" mkdir "%OUTPUT_DIR%\videos"

echo [+] Created output directories
echo.

REM Detect iPhone
echo [*] Detecting iPhone...
echo [*] Please ensure:
echo     1. iPhone is connected via USB
echo     2. iPhone is unlocked
echo     3. You tapped "Trust This Computer" on iPhone
echo.

REM Check common drive letters for iPhone
set "IPHONE_DRIVE="
for %%D in (D E F G H I J K L M N O P Q R S T U V W X Y Z) do (
    if exist "%%D:\DCIM\" (
        echo [+] Found iPhone at drive %%D:\
        set "IPHONE_DRIVE=%%D:"
        goto :found_iphone
    )
)

:not_found
echo [!] iPhone not detected as drive
echo.
echo [*] Alternative methods:
echo     1. Open Windows Photos app
echo     2. Click "Import" button
echo     3. Select your iPhone
echo     4. Choose photos/videos to import
echo.
echo [*] Or try:
echo     1. Unplug and replug iPhone
echo     2. Unlock iPhone
echo     3. Tap "Trust This Computer"
echo     4. Run this script again
echo.
pause
exit /b 1

:found_iphone
echo.
echo [*] Ready to copy media files
echo [*] This may take several minutes depending on file count
echo.
set /p "CONFIRM=Continue? (Y/N): "

if /i not "%CONFIRM%"=="Y" (
    echo [*] Cancelled by user
    pause
    exit /b 0
)

echo.
echo [*] Starting file copy...
echo.

REM Copy photos
echo [*] Copying photos...
xcopy "%IPHONE_DRIVE%\DCIM\*.jpg" "%OUTPUT_DIR%\photos\" /E /H /C /I /Y >nul 2>&1
xcopy "%IPHONE_DRIVE%\DCIM\*.jpeg" "%OUTPUT_DIR%\photos\" /E /H /C /I /Y >nul 2>&1
xcopy "%IPHONE_DRIVE%\DCIM\*.png" "%OUTPUT_DIR%\photos\" /E /H /C /I /Y >nul 2>&1
xcopy "%IPHONE_DRIVE%\DCIM\*.heic" "%OUTPUT_DIR%\photos\" /E /H /C /I /Y >nul 2>&1
xcopy "%IPHONE_DRIVE%\DCIM\*.heif" "%OUTPUT_DIR%\photos\" /E /H /C /I /Y >nul 2>&1

REM Copy videos
echo [*] Copying videos...
xcopy "%IPHONE_DRIVE%\DCIM\*.mp4" "%OUTPUT_DIR%\videos\" /E /H /C /I /Y >nul 2>&1
xcopy "%IPHONE_DRIVE%\DCIM\*.mov" "%OUTPUT_DIR%\videos\" /E /H /C /I /Y >nul 2>&1
xcopy "%IPHONE_DRIVE%\DCIM\*.m4v" "%OUTPUT_DIR%\videos\" /E /H /C /I /Y >nul 2>&1
xcopy "%IPHONE_DRIVE%\DCIM\*.avi" "%OUTPUT_DIR%\videos\" /E /H /C /I /Y >nul 2>&1

echo.
echo ============================================================
echo [+] Media restore completed!
echo ============================================================
echo.

REM Count files
set "PHOTO_COUNT=0"
set "VIDEO_COUNT=0"

for /f %%A in ('dir /b /a-d "%OUTPUT_DIR%\photos\*.*" 2^>nul ^| find /c /v ""') do set "PHOTO_COUNT=%%A"
for /f %%A in ('dir /b /a-d "%OUTPUT_DIR%\videos\*.*" 2^>nul ^| find /c /v ""') do set "VIDEO_COUNT=%%A"

echo [*] Photos copied: %PHOTO_COUNT%
echo [*] Videos copied: %VIDEO_COUNT%
echo.
echo [*] Location: %OUTPUT_DIR%
echo.

REM Open output folder
echo [*] Opening output folder...
explorer "%OUTPUT_DIR%"

echo.
echo [+] Done! You can now safely disconnect your iPhone.
echo.
pause
