@echo off

winget install 9NQ7512CXL7T -e --accept-package-agreements --accept-source-agreements

python -m venv .venv

.venv\Scripts\python.exe -m pip install --upgrade pip
.venv\Scripts\python.exe -m pip install sounddevice numpy

echo.
echo Installation complete.
pause
