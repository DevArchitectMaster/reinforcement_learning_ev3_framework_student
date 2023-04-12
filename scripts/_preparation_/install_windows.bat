@echo off
SET script=%~dp0%~n0%~x0

%LocalAppData%\programs\python\python39\python.exe -m pip install --upgrade pip

pip install -r requirements.txt

echo .

pause