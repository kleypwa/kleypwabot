@echo off
cd /d "%~dp0"
call .venv\Scripts\activate
:loop
python main.py
echo Перезапуск через 5 секунд...
timeout /t 5 /nobreak >nul
goto loop

