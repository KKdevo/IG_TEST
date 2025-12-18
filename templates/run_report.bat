@echo off
cd /d "%~dp0"

echo ===================================
echo   Social Media Report Generator
echo ===================================
echo.

REM Use the Python with python-docx installed
set PYTHON=C:\Python314\python.exe

REM Check if Python exists
if not exist "%PYTHON%" (
    echo Python not found at %PYTHON%
    echo Trying default python...
    set PYTHON=python
)

REM Use PowerShell to show file picker dialog
echo Select your Word document (.docx) file...
echo.

for /f "delims=" %%I in ('powershell -NoProfile -Command "Add-Type -AssemblyName System.Windows.Forms; $f = New-Object System.Windows.Forms.OpenFileDialog; $f.Title = 'Select Word Document for Report'; $f.Filter = 'Word Documents (*.docx)|*.docx|All Files (*.*)|*.*'; $f.InitialDirectory = '%cd%\Content_Schedule_INPUT'; if ($f.ShowDialog() -eq 'OK') { $f.FileName }"') do set INPUT_FILE=%%I

if "%INPUT_FILE%"=="" (
    echo No file selected. Exiting.
    pause
    exit /b 1
)

echo.
echo Selected: %INPUT_FILE%
echo.

REM Generate output filename based on input filename
for %%F in ("%INPUT_FILE%") do set BASENAME=%%~nF
set OUTPUT_FILE=Content_Schedule_OUTPUT\%BASENAME%_report.html

echo Output will be: %OUTPUT_FILE%
echo.
echo Generating report...
echo.

"%PYTHON%" generate_report.py "%INPUT_FILE%" "%OUTPUT_FILE%"

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ERROR: Failed to generate report
    echo.
    echo Check that python-docx is installed:
    echo   %PYTHON% -m pip install python-docx
    pause
    exit /b 1
)

echo.
echo ===================================
echo Report generated successfully!
echo ===================================
echo.
echo Opening in browser...
start "" "%OUTPUT_FILE%"

echo.
echo ===================================
echo.
set /p PUSH_CHOICE="Push to GitHub Pages? (y/n): "

if /i "%PUSH_CHOICE%"=="y" (
    echo.
    echo Pushing to GitHub Pages...
    echo.
    
    REM Add the output file and any assets
    git add Content_Schedule_OUTPUT\*.html
    git add Content_Schedule_OUTPUT\*.png 2>nul
    
    REM Commit with timestamp
    for /f "tokens=1-3 delims=/ " %%a in ('date /t') do set DATESTAMP=%%c-%%a-%%b
    for /f "tokens=1-2 delims=: " %%a in ('time /t') do set TIMESTAMP=%%a:%%b
    git commit -m "Update report - %DATESTAMP% %TIMESTAMP%"
    
    REM Push to origin (master branch)
    git push origin master
    
    if %ERRORLEVEL% EQU 0 (
        echo.
        echo ===================================
        echo Pushed to GitHub successfully!
        echo ===================================
        echo.
        echo Your report should be live at:
        echo https://kkdevo.github.io/IG_TEST/templates/Content_Schedule_OUTPUT/%BASENAME%_report.html
    ) else (
        echo.
        echo Push failed. You may need to run: git push origin master
    )
)

echo.
pause
