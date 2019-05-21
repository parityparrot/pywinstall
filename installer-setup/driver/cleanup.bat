@echo off
setlocal enabledelayedexpansion
:: reg query HKLM /f "{ECFB0CFD-74C4-4f52-BBF7-343461CD72AC}" /s /k
echo "Removing libusbK device class registry keys..."

for /f "tokens=*" %%a in ('reg query HKLM /f "{ECFB0CFD-74C4-4f52-BBF7-343461CD72AC}" /s /k') do (
    set KEY=%%a
    IF /i "!KEY:~0,4!" == "HKEY" (
        reg delete !KEY! /f
    )
)