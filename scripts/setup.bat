@echo off
REM Setup script for Jail Custody Checker
REM Creates dedicated conda environment if needed

REM Change to repository root directory
cd /d "%~dp0.."

echo ============================================
echo Jail Custody Checker - Setup
echo ============================================
echo.

REM Check if conda is available
where conda >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: conda not found in PATH
    echo Please install Anaconda or Miniconda first
    echo https://docs.conda.io/en/latest/miniconda.html
    echo.
    pause
    exit /b 1
)

echo Checking for jail_checker environment...
conda env list | findstr /C:"jail_checker" >nul 2>&1

if %errorlevel% equ 0 (
    echo Found existing jail_checker environment
    echo.
) else (
    echo jail_checker environment not found
    echo Creating new conda environment with Python 3.11...
    echo.
    conda create -n jail_checker python=3.11 -y

    echo.
    echo Verifying environment was created...
    conda env list | findstr /C:"jail_checker" >nul 2>&1

    if %errorlevel% neq 0 (
        echo.
        echo ERROR: Failed to create conda environment
        echo The conda command completed but the environment was not found.
        echo Try running: conda create -n jail_checker python=3.11 -y
        pause
        exit /b 1
    )

    echo Environment created successfully!
    echo.
)

echo Activating jail_checker environment...
call conda activate jail_checker

if %errorlevel% neq 0 (
    echo.
    echo ERROR: Failed to activate environment
    echo Try running: conda activate jail_checker
    pause
    exit /b 1
)

echo.
echo Installing Python packages...
echo.
pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo.
    echo ERROR: Failed to install requirements
    pause
    exit /b 1
)

echo.
echo ============================================
echo Setup Complete!
echo ============================================
echo.
echo Environment: jail_checker (Python 3.11)
echo.
echo Next steps:
echo   1. Place defendant list in input\ folder
echo   2. Run: run_check.bat "input\your_file.csv"
echo.
echo Or test with sample files:
echo   run_check.bat "Active Cases By Assigned Personnel Detail.csv"
echo   run_check.bat "Prosecutor Worklist Report.pdf"
echo.

pause
