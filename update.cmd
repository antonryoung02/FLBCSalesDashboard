@echo off
cd <path\to\your\github\repo>

echo Pulling the latest changes
git pull

echo Activating Environment
REM protects against conda not recognized
call <path\to\your_virtualenv\Scripts\activate>

conda activate <your_env_name>

echo Installing packages
pip install -r requirements.txt

echo Update complete! Latest changes and packages are installed.
pause