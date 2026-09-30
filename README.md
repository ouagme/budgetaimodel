# BudgetAI v3 — Local MySQL/MariaDB Terminal Budget Manager

Local-first terminal finance assistant using a Flask API and MySQL/MariaDB on localhost.

## Architecture
Terminal CLI → Flask API (127.0.0.1:8000) → MySQL/MariaDB (127.0.0.1:3306), database budgetai.

## Features
Accounts, transactions, categories, budgets, recurring transactions, savings goals, monthly summaries, multi-currency support, JSON export.

## Requirements
- Python 3.10+
- MySQL or MariaDB running locally

## Install
1. Start MySQL/MariaDB (XAMPP/WAMP/Laragon/standalone).
2. Run setup_mysql.bat on Windows, or execute schema.sql in MySQL/MariaDB.
3. Copy .env.example to .env and set credentials.
4. Install packages: pip install -r requirements.txt
5. Start API: python api.py
6. In another terminal: python cli.py

Health check: http://127.0.0.1:8000/api/health

All financial data stays in the local MySQL/MariaDB database.