#!/bin/bash
# Quick validation script to check if views.py has syntax errors

echo "Checking views.py for syntax errors..."
python -m py_compile myapp/views.py

if [ $? -eq 0 ]; then
    echo "✓ views.py syntax is valid"
else
    echo "✗ Syntax errors found in views.py"
    exit 1
fi

echo ""
echo "Checking urls.py for syntax errors..."
python -m py_compile collegeconnect/urls.py

if [ $? -eq 0 ]; then
    echo "✓ urls.py syntax is valid"
else
    echo "✗ Syntax errors found in urls.py"
    exit 1
fi

echo ""
echo "All syntax checks passed!"
