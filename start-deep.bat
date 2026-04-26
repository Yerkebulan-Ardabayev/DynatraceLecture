@echo off
REM Запускает deep crawl по конкретному разделу.
REM Использование:  start-deep.bat settings
REM                 start-deep.bat settings/preferences

cd /d "%~dp0"
if "%~1"=="" (
  echo ERROR: укажи раздел.  Пример:  start-deep.bat settings
  exit /b 1
)

echo Deep crawl: %~1
echo Output: %CD%\output\
echo.

python crawler.py deep --section "%~1" > logs\deep-%~1-stdout.log 2>&1

echo.
echo === DONE ===
pause
