@echo off
SET script=%~dp0

cd %script%
cd "../"

echo %CD%

rmdir /s /q "__pycache__"

echo .

pause