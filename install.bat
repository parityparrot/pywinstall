@echo off

virtualenv venv & ^
.\venv\Scripts\activate & ^
pip install -r requirements.txt & ^
copy /Y ".\patch\hook-usb.py" ".\venv\Lib\site-packages\PyInstaller\hooks\hook-usb.py" & ^
pyinstaller main.py -F -n pywinstall
