@echo off
REM Crawl по учебному плану.
REM   start-plan.bat              — все 5 дней
REM   start-plan.bat day-1        — только день 1
REM   start-plan.bat day-3-4      — дни 3-4

cd /d "%~dp0"

if "%~1"=="" (
  set DAY_ARG=
  set LOG_NAME=plan-all
) else (
  set DAY_ARG=--day %~1
  set LOG_NAME=plan-%~1
)

echo Plan crawl: %~1
echo Output: %CD%\output\
echo Log:    %CD%\logs\%LOG_NAME%-stdout.log
echo.

python plan_runner.py %DAY_ARG% > logs\%LOG_NAME%-stdout.log 2>&1

echo.
echo === DONE ===
echo Generating docs...
python plan_docs.py
echo.
echo Open: %CD%\output\docs\index.md
pause
