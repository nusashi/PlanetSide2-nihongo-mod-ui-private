@echo off
timeout /T 1 /NOBREAK > nul
tasklist /FI "IMAGENAME eq PS2JPMod.exe" | findstr /I "PS2JPMod.exe" > nul
if %errorlevel% == 0 (
    echo PS2JPMod.exe is still running. Please close it and try again.
    pause
    exit /b 1
)
copy /Y data\PS2JPMod.exe .\PS2JPMod.exe
copy /Y data\はじめにお読みください.txt .\はじめにお読みください.txt
del data\PS2JPMod.exe
del data\はじめにお読みください.txt
start .\PS2JPMod.exe