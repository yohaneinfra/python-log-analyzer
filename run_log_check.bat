rem 文字コードを「UTF-8」に設定
chcp 65001

@echo off
cd /d C:\Users\User\python-infra
call venv\Scripts\activate
python log_check.py

REM If ERROR exists, write Windows Event Log
findstr "ERROR" result.log >nul
if %errorlevel% equ 0 (
    eventcreate /T ERROR /ID 100 /L APPLICATION /D "ログにERRORが検出されました"
)

pause