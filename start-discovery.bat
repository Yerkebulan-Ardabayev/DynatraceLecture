@echo off
REM Запускает discovery crawl в отдельном окне.
REM Top-level routes Dynatrace SaaS, depth=1, ~20-50 страниц.

cd /d "%~dp0"
echo Starting Dynatrace discovery crawl...
echo Output: %CD%\output\
echo Logs:   %CD%\logs\
echo.
echo (Это окно можно сворачивать. Закрывать — НЕЛЬЗЯ, прервёт crawl.)
echo.

python crawler.py discovery > logs\discovery-stdout.log 2>&1

echo.
echo === DONE ===
echo See: logs\discovery-stdout.log
echo See: output\data\pages.jsonl
echo Run docs:  python crawler.py docs
pause
