@echo off
title ECOSPHERE AI - Frontend Application
echo ========================================================
echo        Starting ECOSPHERE AI Frontend (React + Vite)
echo ========================================================
cd /d "%~dp0frontend"
echo Starting Vite Development Server...
echo   Website: http://localhost:5173
echo.
echo NOTE: Keep this window open while using the website.
echo       The backend must also be running (run_backend.bat).
echo.
npm run dev
pause
