@echo off
echo =========================================
echo BudgetAI v3 - MySQL/MariaDB setup
echo =========================================
echo.
echo Make sure MySQL or MariaDB is running.
echo.
set /p DBUSER=Database username [root]:
if "%DBUSER%"=="" set DBUSER=root
set /p DBPASS=Database password [leave empty if none]:
echo.
echo Creating database...
if "%DBPASS%"=="" (
  mysql -u %DBUSER% < schema.sql
) else (
  mysql -u %DBUSER% -p%DBPASS% < schema.sql
)
if %errorlevel% neq 0 (
  echo.
  echo Could not connect to MySQL/MariaDB.
  echo Check that mysql.exe is in PATH and the server is running.
  pause
  exit /b 1
)
copy /Y .env.example .env >nul
echo.
echo Database budgetai created successfully.
echo Edit .env if your MySQL credentials are different.
pause
