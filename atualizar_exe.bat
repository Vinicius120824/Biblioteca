@echo off
cd /d "%~dp0"

call .venv\Scripts\activate.bat

python -m PyInstaller --clean --noconfirm Biblioteca.spec

echo.
echo Build finalizado.
pause