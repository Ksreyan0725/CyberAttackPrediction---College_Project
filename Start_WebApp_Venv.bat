@echo off
setlocal
echo Starting the Web App (Main.py) using the .venv...
call .venv\Scripts\activate.bat
cd %~dp0CyberAttackPrediction

:: Heartbeat-Aware Smart Launch:
:: No .browser_lock needed anymore! The server (Main.py) will now dynamically 
:: check for open pulses before launching a new tab.
:: This is a much smoother and more professional experience.

:RESTART_LOOP
cls
echo ==========================================
echo    CyberShield AI Dashboard - STARTING
echo ==========================================

:: Run the server (let Main.py handle the smart browser launch)
python Main.py

echo.
echo ==========================================
echo    SERVER STOPPED OR CRASHED!
echo    Press any key to RESTART the server...
echo    Close this window to quit.
echo ==========================================
pause > nul
goto RESTART_LOOP
