
@echo off
setlocal

:: Check if python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Python not found. Running installer...
    if exist redist\python-manager-25.2.msix (
        start /wait redist\python-manager-25.2.msix
    ) else (
        echo Python installer not found in redist folder.
        pause
        exit /b
    )
)

:: Install Pipenv if missing
pip show pipenv >nul 2>&1
if errorlevel 1 (
    echo Installing Pipenv...
    pip install pipenv
)

:: Install dependencies
echo Installing project dependencies...
pipenv install
pipenv run playwright install

:: Start the server
echo Starting ArtlistIO server...
pipenv run uvicorn app:app --reload

pause
