@echo off
python -m pip install -r requirements.txt
start "BudgetAI API" cmd /k python api.py
timeout /t 2 >nul
python cli.py
pause
