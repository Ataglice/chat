@echo off
echo Сборка проекта...

:: Переходим в папку desktop_client
cd /d %~dp0

:: Удаляем старые папки сборки
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist *.spec del /q *.spec

:: Явно указываем путь к pyinstaller внутри venv
..\.\.venv\Scripts\pyinstaller.exe --onefile --noconsole main.py

echo Сборка завершена. Файл находится в папке dist\
pause
