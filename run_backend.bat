@echo off
title ECOSPHERE AI - Backend Service
echo ========================================================
echo        Starting ECOSPHERE AI Backend (FastAPI)
echo ========================================================
cd /d "%~dp0backend"
echo Installing/Verifying Python requirements...
python -m pip install -r ..\requirements.txt --quiet
echo.
echo Starting Uvicorn API Server...
echo   Backend API:   http://localhost:8000
echo   Swagger Docs:  http://localhost:8000/docs
echo.
echo NOTE: Keep this window open while using the website.
echo.
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
pause
