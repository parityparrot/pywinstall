@echo off

set pypath=.\python37\
set pyscripts=.\python37\Scripts\

call add-path pypath
call add-path pyscripts

if not exist .\venv\ (
    :: Handle `Command "python setup.py egg_info" failed with error code 3221225781`
    pip install virtualenv pyinstaller sounddevice soundfile
    virtualenv venv
    .\venv\Scripts\activate
    pip install -r requirements.txt
) else (
    .\venv\Scripts\activate
)