@echo off
chcp 65001 >nul
cd /d "%~dp0"

where uv >nul 2>nul
if errorlevel 1 (
  echo.
  echo   uv ist auf diesem Rechner nicht installiert.
  echo   Einmal einrichten: einrichten.bat doppelklicken.
  echo   Anleitung: docs\02_technik_setup.md
  echo.
  pause
  exit /b 1
)

echo   Umgebung wird geprueft ...
uv sync --quiet
uv run code/start.py
pause
