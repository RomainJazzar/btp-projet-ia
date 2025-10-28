@echo off
echo ============================================================
echo   DOCin-Lite - Installation Complete
echo ============================================================
echo.

echo [1/5] Creation de la structure des dossiers...
mkdir tools 2>nul
mkdir src\core 2>nul
mkdir src\app_web 2>nul
mkdir tests 2>nul
mkdir data\inbox 2>nul
mkdir data\processed 2>nul
echo OK - Dossiers crees
echo.

echo [2/5] Creation des fichiers source...
python create_files.py
if errorlevel 1 (
    echo ERREUR - Verifiez que Python est installe
    pause
    exit /b 1
)
echo OK - Fichiers source crees
echo.

echo [3/5] Creation de l'environnement virtuel...
python -m venv venv
if errorlevel 1 (
    echo ERREUR - Impossible de creer venv
    pause
    exit /b 1
)
echo OK - Environnement virtuel cree
echo.

echo [4/5] Activation et installation des dependances...
call venv\Scripts\activate.bat
pip install --quiet streamlit pdfminer.six pytest anthropic
if errorlevel 1 (
    echo ERREUR - Installation des dependances echouee
    pause
    exit /b 1
)
echo OK - Dependances installees
echo.

echo [5/5] Verification avec les tests...
pytest -q
if errorlevel 1 (
    echo ATTENTION - Certains tests ont echoue
    echo Vous pouvez continuer, mais verifiez les erreurs
) else (
    echo OK - Tous les tests sont passes
)
echo.

echo ============================================================
echo   Installation terminee avec succes !
echo ============================================================
echo.
echo Pour lancer l'application :
echo   venv\Scripts\activate
echo   streamlit run src\app_web\app.py
echo.
echo Documentation :
echo   - QUICKSTART.txt  : Installation rapide
echo   - README.md       : Presentation du projet
echo   - INSTALL.md      : Guide complet
echo   - ARCHITECTURE.md : Architecture technique
echo   - SUMMARY.md      : Resume executif
echo.
echo Appuyez sur une touche pour lancer l'application...
pause >nul

echo.
echo Lancement de DOCin-Lite...
streamlit run src\app_web\app.py
