@echo off
REM Quick run script for Jail Custody Checker
REM Uses jail_checker conda environment
REM Auto-detects most recent CSV/PDF in input folder if no argument provided

setlocal enabledelayedexpansion

REM Change to repository root directory
cd /d "%~dp0.."

echo ============================================
echo Jail Custody Checker
echo ============================================
echo.

REM Check for input file argument
if "%~1"=="" (
    echo No input file specified - auto-detecting...
    echo.

    REM Find most recent CSV or PDF in input folder
    set "LATEST_FILE="
    set "LATEST_TIME=0"

    REM Check CSV files
    for %%F in ("input\*.csv") do (
        set "LATEST_FILE=%%F"
    )

    REM Check PDF files
    for %%F in ("input\*.pdf") do (
        set "LATEST_FILE=%%F"
    )

    REM Use PowerShell to find file (prefers PDF over CSV for better data quality)
    for /f "delims=" %%i in ('powershell -Command "$pdf = Get-ChildItem '%CD%\input\*.pdf' -ErrorAction SilentlyContinue | Sort-Object LastWriteTime -Descending | Select-Object -First 1; $csv = Get-ChildItem '%CD%\input\*.csv' -ErrorAction SilentlyContinue | Sort-Object LastWriteTime -Descending | Select-Object -First 1; if ($pdf) { $pdf.Name } elseif ($csv) { $csv.Name }"') do (
        set "LATEST_FILE=input\%%i"
    )

    REM Check if we actually found a file (not just "input\" or empty)
    if "!LATEST_FILE!"=="" (
        echo ERROR: No CSV or PDF files found in input\ folder
        echo.
        echo Please place your defendant list in the input\ folder
        echo   - Supported formats: .csv or .pdf
        echo.
        echo Or specify a file manually:
        echo   run_check.bat "path\to\file.csv"
        echo.
        pause
        exit /b 1
    )

    REM Check if LATEST_FILE is just "input\" without a filename
    if "!LATEST_FILE!"=="input\" (
        echo ERROR: No CSV or PDF files found in input\ folder
        echo.
        echo Please place your defendant list in the input\ folder
        echo   - Supported formats: .csv or .pdf
        echo.
        echo Or specify a file manually:
        echo   run_check.bat "path\to\file.csv"
        echo.
        pause
        exit /b 1
    )

    REM Get file modification time for display
    for /f "delims=" %%i in ('powershell -Command "^(Get-Item '!LATEST_FILE!'^).LastWriteTime.ToString('MM/dd/yyyy hh:mm tt'^)"') do (
        set "FILE_TIME=%%i"
    )

    echo Found: !LATEST_FILE!
    echo Modified: !FILE_TIME!
    echo.
    echo Using most recent file from input folder
    echo.

    set "INPUT_FILE=!LATEST_FILE!"
) else (
    echo Using specified file: %~1
    echo.
    set "INPUT_FILE=%~1"
)

REM Check if conda is available
where conda >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: conda not found in PATH
    echo Please run setup.bat first
    echo.
    pause
    exit /b 1
)

REM Check if jail_checker environment exists
conda env list | findstr /C:"jail_checker" >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: jail_checker environment not found
    echo Please run setup.bat first to create the environment
    echo.
    pause
    exit /b 1
)

REM Activate the environment
call conda activate jail_checker
if %errorlevel% neq 0 (
    echo ERROR: Failed to activate jail_checker environment
    echo.
    pause
    exit /b 1
)

echo Checking custody status...
echo.

REM Run the checker
python src\main.py "!INPUT_FILE!"

if %errorlevel% neq 0 (
    echo.
    echo ERROR: Custody check failed
    echo Check the error messages above
    echo.
    pause
    exit /b 1
)

echo.
echo ============================================
echo Check Complete!
echo ============================================
echo.
echo Reports saved in output\ folder
echo   - JSON format (for web interface)
echo   - Excel format (for review)
echo.
echo Open the Excel file to see results with color coding:
echo   - RED = In custody
echo   - GREEN = Not in custody
echo   - YELLOW = Errors
echo.

pause
