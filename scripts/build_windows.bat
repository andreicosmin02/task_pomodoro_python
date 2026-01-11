@echo off
REM ============================================================================
REM TaskPomodoro Windows Build Script
REM ============================================================================
REM
REM This batch file builds TaskPomodoro into a Windows executable.
REM
REM Prerequisites:
REM   - Python 3.9+ installed and in PATH
REM   - pip installed
REM
REM Usage:
REM   build_windows.bat
REM
REM ============================================================================

echo.
echo ============================================
echo   TaskPomodoro Windows Build Script
echo ============================================
echo.

REM Change to project root directory
cd /d "%~dp0\.."
echo Project directory: %CD%
echo.

REM Check Python
echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found! Please install Python 3.9+ and add to PATH.
    pause
    exit /b 1
)

python --version
echo.

REM Install/upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip
echo.

REM Install PyInstaller
echo Installing PyInstaller...
python -m pip install pyinstaller
echo.

REM Clean previous builds
echo Cleaning previous builds...
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"
if exist "*.spec" del /q "*.spec"
echo.

REM Build executable
echo Building executable...
echo.

python -m PyInstaller ^
    --name=TaskPomodoro ^
    --onefile ^
    --windowed ^
    --clean ^
    --paths=. ^
    --paths=src ^
    --hidden-import=src.core ^
    --hidden-import=src.core.app ^
    --hidden-import=src.core.state ^
    --hidden-import=src.core.timer ^
    --hidden-import=src.core.notifications ^
    --hidden-import=src.ui ^
    --hidden-import=src.ui.theme ^
    --hidden-import=src.ui.widgets ^
    --hidden-import=src.ui.widgets.button ^
    --hidden-import=src.ui.widgets.checkbox ^
    --hidden-import=src.ui.widgets.clock_icon ^
    --hidden-import=src.ui.widgets.toast ^
    --hidden-import=src.ui.widgets.dialog ^
    --hidden-import=src.ui.pages ^
    --hidden-import=src.ui.pages.base_page ^
    --hidden-import=src.ui.pages.starting_page ^
    --hidden-import=src.ui.pages.working_page ^
    --hidden-import=src.ui.pages.resting_page ^
    --hidden-import=src.utils ^
    --hidden-import=src.utils.formatting ^
    src\main.py

if errorlevel 1 (
    echo.
    echo ============================================
    echo   BUILD FAILED!
    echo ============================================
    pause
    exit /b 1
)

echo.
echo ============================================
echo   BUILD SUCCESSFUL!
echo ============================================
echo.
echo Executable location: %CD%\dist\TaskPomodoro.exe
echo.
echo You can now distribute TaskPomodoro.exe!
echo.

pause