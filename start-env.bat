@echo off

set PATH=%PATH%;.\python37\;.\python37\Scripts\

if not exist .\venv\ (
    :: Handle `Command "python setup.py egg_info" failed with error code 3221225781`
    if not exist .\python37\Scripts\pyinstaller.exe (
        pip install pyinstaller
    )
    if not exist .\python37\Scripts\virtualenv.exe (
        pip install virtualenv
    )
    virtualenv venv
    .\venv\Scripts\activate
    pip install -r requirements.txt
) else (
    .\venv\Scripts\activate
)