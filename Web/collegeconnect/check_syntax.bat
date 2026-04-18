@echo off
REM Quick validation script to check if views.py has syntax errors

echo Checking views.py for syntax errors...
python -m py_compile myapp\views.py

if %errorlevel% equ 0 (
    echo ^✓ views.py syntax is valid
) else (
    echo ^✗ Syntax errors found in views.py
    exit /b 1
)

echo.
echo Checking urls.py for syntax errors...
python -m py_compile collegeconnect\urls.py

if %errorlevel% equ 0 (
    echo ^✓ urls.py syntax is valid
) else (
    echo ^✗ Syntax errors found in urls.py
    exit /b 1
)

echo.
echo All syntax checks passed!
pause
