@echo off

rmdir /s /q .\build\ 2>nul
rmdir /s /q .\dist\ 2>nul
del /f /q pywince.spec 2>nul

copy /y ".\resources\patch\hook-usb.py" ".\venv\Lib\site-packages\PyInstaller\hooks\hook-usb.py"

pyinstaller --paths .\venv\Lib\site-packages\ ^
--add-data ".\venv\Lib\site-packages\_sounddevice_data\portaudio-binaries\libportaudio64bit.dll;_sounddevice_data\portaudio-binaries" ^
--add-data ".\venv\Lib\site-packages\_soundfile_data\libsndfile64bit.dll;_soundfile_data" ^
-F main.py -n pywince