@echo off
title AI Pilot Launcher
cd /d "%~dp0"

if not exist ".venv\Scripts\activate.bat" (
  echo No virtual environment found. Run the setup in INSTRUCTION.md first.
  pause
  exit /b 1
)
call ".venv\Scripts\activate.bat"

REM Start Ollama only if it isn't already answering on port 11434
curl -s http://localhost:11434/api/tags >nul 2>&1
if errorlevel 1 (
  echo Starting Ollama...
  start "Ollama" /min ollama serve
  timeout /t 5 /nobreak >nul
) else (
  echo Ollama already running.
)

REM Port, backend, and SCALE come from config.py
python main.py
echo.
echo Pilot stopped.
pause