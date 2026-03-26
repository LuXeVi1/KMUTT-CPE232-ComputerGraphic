#!/bin/bash
# CPE381 Computer Graphics - Exam Calculator

echo ""
echo " ╔══════════════════════════════════════════════╗"
echo " ║  CPE381 Computer Graphics Exam Calculator    ║"
echo " ╚══════════════════════════════════════════════╝"
echo ""

# Find Python
if command -v python3 &>/dev/null; then
    PYTHON=python3
elif command -v python &>/dev/null; then
    PYTHON=python
else
    echo " [ERROR] Python is not installed."
    echo " Please install Python 3.8+ first."
    exit 1
fi

PYVER=$($PYTHON --version 2>&1)
echo " [OK] $PYVER"
echo ""

# Check packages
PKGS=("numpy" "tabulate" "matplotlib")
MISSING=()

echo " Checking dependencies..."
for pkg in "${PKGS[@]}"; do
    if $PYTHON -c "import $pkg" &>/dev/null; then
        echo "   [✓] $pkg"
    else
        echo "   [✗] $pkg  (not found)"
        MISSING+=("$pkg")
    fi
done
echo ""

# Install missing
TOTAL=${#MISSING[@]}
if [ "$TOTAL" -eq 0 ]; then
    echo " [OK] All dependencies already installed!"
else
    echo " Installing $TOTAL missing package(s)..."
    echo ""

    $PYTHON -m pip install --quiet --upgrade pip &>/dev/null

    DONE=0
    for pkg in "${MISSING[@]}"; do
        DONE=$((DONE + 1))
        PCT=$((DONE * 100 / TOTAL))
        FILLED=$((PCT / 5))
        EMPTY=$((20 - FILLED))

        BAR=""
        for ((i=0; i<FILLED; i++)); do BAR+="█"; done
        for ((i=0; i<EMPTY; i++)); do BAR+="░"; done

        printf "\r  [%s] %3d%%  Installing %s...                " "$BAR" "$PCT" "$pkg"
        $PYTHON -m pip install --quiet "$pkg" &>/dev/null
    done

    printf "\r  [████████████████████] 100%%  Done!                       \n"
    echo ""
    echo " [OK] All packages installed successfully!"
fi

echo ""
echo " ╔══════════════════════════════════════════════╗"
echo " ║  Starting Exam Calculator...                 ║"
echo " ╚══════════════════════════════════════════════╝"
echo ""

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
$PYTHON -X utf8 "$SCRIPT_DIR/main.py"
