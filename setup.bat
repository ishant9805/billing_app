@echo off
set HOST=localhost
set USER=root
set PORT=3306
set "DB_PASSWORD="

set /p DB_PASSWORD="Enter MySQL database password: "

REM Check if password was provided
if not defined DB_PASSWORD (
    echo Error: Password cannot be empty
    pause
    exit /b 1
)

py app.py
set "DB_PASSWORD="
pause
