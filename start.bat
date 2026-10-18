@echo off
title AI Pilot Launcher
cd /d "%~dp0"
setlocal

REM Usage: start.bat [--no-flash] [--sim-only] [any other main.py flags]
set FLASH=1
set ARGS=
:parse
if "%~1"=="" goto parsed
if /I "%~1"=="--no-flash" ( set FLASH=0 ) else ( set ARGS=%ARGS% %~1 )
shift
goto parse
:parsed

echo ==== 1/5 Python environment
if not exist ".venv\Scripts\python.exe" (
  echo Creating .venv ...
  python -m venv .venv || goto fail
)
call ".venv\Scripts\activate.bat"
python -c "import jsbsim, serial, requests" 2>nul
if errorlevel 1 (
  echo Installing packages ...
  python -m pip install -q jsbsim pyserial requests || goto fail
)

echo ==== 2/5 Arduino firmware
for /f "tokens=1" %%p in ('python -c "import config; print(config.COM_PORT)"') do set PORT=%%p
echo Uno expected on %PORT%
if "%FLASH%"=="1" (
  where arduino-cli >nul 2>&1
  if errorlevel 1 (
    echo arduino-cli not found, skipping flash. Upload firmware\pilot_slider\pilot_slider.ino from the IDE.
  ) else (
    arduino-cli board list | findstr /I "%PORT%" >nul
    if errorlevel 1 (
      echo No board on %PORT%. Skipping flash; main.py will keep retrying the port.
    ) else (
      echo Flashing firmware to %PORT% ...
      arduino-cli compile --fqbn arduino:avr:uno firmware\pilot_slider >nul || goto fail
      arduino-cli upload -p %PORT% --fqbn arduino:avr:uno firmware\pilot_slider || goto fail
    )
  )
) else (
  echo Flash skipped ^(--no-flash^).
)

echo ==== 3/5 Ollama
for /f "tokens=1" %%m in ('python -c "import config; print(config.OLLAMA_MODEL)"') do set MODEL=%%m
set tries=0
curl -s http://localhost:11434/api/tags >nul 2>&1
if not errorlevel 1 (
  echo Ollama already running.
  goto ollamaup
)
echo Starting Ollama ...
start "Ollama" /min ollama serve
:waitollama
timeout /t 1 /nobreak >nul
curl -s http://localhost:11434/api/tags >nul 2>&1
if not errorlevel 1 goto ollamaup
set /a tries+=1
if %tries% lss 20 goto waitollama
echo Ollama did not start. Run "ollama serve" by hand.
goto fail
:ollamaup
ollama list | findstr /I "%MODEL%" >nul
if errorlevel 1 (
  echo Pulling %MODEL% ...
  ollama pull %MODEL% || goto fail
)

echo ==== 4/5 Captain warm-up
python -c "import captain, config; c = captain.Captain(config.CAPTAIN_BACKEND); c.warm_up()"

echo ==== 5/5 Pilot
echo Close the Arduino Serial Monitor and gui.py if they are open. Ctrl+C stops the pilot.
python main.py %ARGS%
echo.
echo Pilot stopped.
pause
exit /b 0

:fail
echo.
echo FAILED. See the message above.
pause
exit /b 1
