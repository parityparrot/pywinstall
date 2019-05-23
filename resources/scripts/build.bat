@echo off

rmdir /s /q ..\..\build\ 2>nul
rmdir /s /q ..\..\dist\ 2>nul
del /f /q ..\..\pywince.spec 2>nul

copy /y "..\patch\hook-usb.py" "..\..\venv\Lib\site-packages\PyInstaller\hooks\hook-usb.py"

pyinstaller --paths ..\..\venv\Lib\site-packages\ ^
--specpath "..\..\." --distpath "..\..\dist" --workpath "..\..\build" ^
--add-data ".\venv\Lib\site-packages\_sounddevice_data\portaudio-binaries\libportaudio64bit.dll;_sounddevice_data\portaudio-binaries" ^
--add-data ".\venv\Lib\site-packages\_soundfile_data\libsndfile64bit.dll;_soundfile_data" ^
..\..\main.py -F -n pywince

..\tools\iscc.exe ..\..\installer-setup\setup.iss