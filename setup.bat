@echo off
REM Setup script for DOCin-Lite project

echo Creating directory structure...
mkdir tools 2>nul
mkdir src\core 2>nul
mkdir src\app_web 2>nul
mkdir tests 2>nul
mkdir data\inbox 2>nul
mkdir data\processed 2>nul

echo.
echo Directory structure created!
echo.
echo Next steps:
echo 1. Run: python create_files.py
echo 2. Run: python -m venv venv
echo 3. Run: venv\Scripts\activate
echo 4. Run: pip install streamlit pdfminer.six pytest anthropic
echo 5. Run: streamlit run src\app_web\app.py
echo.
pause
