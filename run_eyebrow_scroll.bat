@echo off
echo Setting up Eyebrow Scroll...

if not exist .venv (
    echo Creating virtual environment...
    python -m venv .venv
)

echo Activating virtual environment...
call .venv\Scripts\activate

echo Installing requirements...
pip install -r requirements.txt

echo Starting Eyebrow Scroll...
python jm_eyebrow_scroll.py

pause
