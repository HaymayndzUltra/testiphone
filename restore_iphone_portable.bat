@echo off
REM iPhone Media Restore - For Portable Device Mount
REM Works when iPhone appears as "This PC\Apple iPhone"

title iPhone Media Restore Tool (Portable Device)
color 0A

echo ============================================================
echo iPhone Media Restore Tool - Portable Device Version
echo For iPhone mounted as "This PC\Apple iPhone"
echo ============================================================
echo.

REM Set output directory
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

echo ============================================================
echo MANUAL COPY INSTRUCTIONS
echo ============================================================
echo.
echo Since your iPhone is mounted as a portable device,
echo please follow these steps:
echo.
echo 1. Open File Explorer (Windows + E)
echo 2. Click on "This PC" in the left sidebar
echo 3. Double-click "Apple iPhone"
echo 4. Double-click "Internal Storage"
echo 5. Double-click "DCIM" folder
echo 6. You'll see folders like: 100APPLE, 101APPLE, etc.
echo.
echo 7. Select ALL folders (Ctrl + A)
echo 8. Copy them (Ctrl + C)
echo 9. Navigate to: %OUTPUT_DIR%
echo 10. Paste (Ctrl + V)
echo.
echo [*] This will copy all photos and videos to your computer
echo.
pause
echo.
echo [*] After copying, I'll organize the files for you...
echo.
set /p "COPIED=Have you finished copying? (Y/N): "

if /i not "%COPIED%"=="Y" (
    echo [*] Cancelled. Run this script again when ready.
    pause
    exit /b 0
)

echo.
echo [*] Organizing files...
echo.

REM Move photos to photos folder
echo [*] Moving photos...
if exist "%OUTPUT_DIR%\*APPLE\*.jpg" move /Y "%OUTPUT_DIR%\*APPLE\*.jpg" "%OUTPUT_DIR%\photos\" >nul 2>&1
if exist "%OUTPUT_DIR%\*APPLE\*.jpeg" move /Y "%OUTPUT_DIR%\*APPLE\*.jpeg" "%OUTPUT_DIR%\photos\" >nul 2>&1
if exist "%OUTPUT_DIR%\*APPLE\*.png" move /Y "%OUTPUT_DIR%\*APPLE\*.png" "%OUTPUT_DIR%\photos\" >nul 2>&1
if exist "%OUTPUT_DIR%\*APPLE\*.heic" move /Y "%OUTPUT_DIR%\*APPLE\*.heic" "%OUTPUT_DIR%\photos\" >nul 2>&1
if exist "%OUTPUT_DIR%\*APPLE\*.heif" move /Y "%OUTPUT_DIR%\*APPLE\*.heif" "%OUTPUT_DIR%\photos\" >nul 2>&1

REM Move videos to videos folder
echo [*] Moving videos...
if exist "%OUTPUT_DIR%\*APPLE\*.mp4" move /Y "%OUTPUT_DIR%\*APPLE\*.mp4" "%OUTPUT_DIR%\videos\" >nul 2>&1
if exist "%OUTPUT_DIR%\*APPLE\*.mov" move /Y "%OUTPUT_DIR%\*APPLE\*.mov" "%OUTPUT_DIR%\videos\" >nul 2>&1
if exist "%OUTPUT_DIR%\*APPLE\*.m4v" move /Y "%OUTPUT_DIR%\*APPLE\*.m4v" "%OUTPUT_DIR%\videos\" >nul 2>&1

REM Clean up empty APPLE folders
for /d %%D in ("%OUTPUT_DIR%\*APPLE") do rd "%%D" 2>nul

echo.
echo ============================================================
echo [+] Organization complete!
echo ============================================================
echo.

REM Count files
set "PHOTO_COUNT=0"
set "VIDEO_COUNT=0"

for /f %%A in ('dir /b /a-d "%OUTPUT_DIR%\photos\*.*" 2^>nul ^| find /c /v ""') do set "PHOTO_COUNT=%%A"
for /f %%A in ('dir /b /a-d "%OUTPUT_DIR%\videos\*.*" 2^>nul ^| find /c /v ""') do set "VIDEO_COUNT=%%A"

echo [*] Photos: %PHOTO_COUNT%
echo [*] Videos: %VIDEO_COUNT%
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
