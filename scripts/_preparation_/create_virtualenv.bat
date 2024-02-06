@echo off
SET script=%~dp0%~n0%~x0

cd %~dp0%..\..

for %%I in (.) do set CurrDirName=%%~nxI

cd %~dp0%..\..\..

python -m venv %CurrDirName%

rem call "\Scripts\activate.bat"
rem call "\Scripts\__preparation_\install_windows.bat"

echo .

pause
exit