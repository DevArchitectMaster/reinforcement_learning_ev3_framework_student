@echo off
SET script=%~dp0

cd %script%
cd "../../model_storage/"

for /D %%a in (".\*.*") do rd /q /s "%%a"

echo .

pause
exit