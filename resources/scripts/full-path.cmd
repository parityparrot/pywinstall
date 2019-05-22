@echo off

:: https://stackoverflow.com/a/4488734

set REL_PATH=%~1
set ABS_PATH=

:: Save current directory and change to target directory
pushd %REL_PATH%

:: Save value of CD variable (current directory)
set ABS_PATH=%CD%

:: Restore original directory
popd
