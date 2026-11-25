@echo off
title ECOSPHERE AI - Unified Starter
echo ========================================================
echo        ECOSPHERE AI - Full Stack Platform Launcher
echo ========================================================
echo.
echo Launching Backend in a separate window...
start "ECOSPHERE AI Backend" "%~dp0run_backend.bat"
echo.
echo Waiting 3 seconds for backend initialization...
timeout /t 3 /nobreak >nul
echo.
echo Launching Frontend in a separate window...
start "ECOSPHERE AI Frontend" "%~dp0run_frontend.bat"
echo.
echo ========================================================
echo  Backend:  http://localhost:8000
echo  API Docs: http://localhost:8000/docs
echo  Frontend: http://localhost:5173
echo ========================================================
echo.
echo Both services are now running in separate console windows.
echo Press any key to exit this launcher window (services keep running).
pause >nul
