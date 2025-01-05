@echo off
cd C:\Users\info\OneDrive\Desktop\FLBC 1.1.1\Revenue and menu engineering data\FLBCSalesDashboard\

echo Pulling the latest changes
git pull

echo Activating Environment
REM protects against conda not recognized
call C:\Users\info\Miniconda3\envs\sales_dashboard

conda activate sales_dashboard

echo Installing packages
pip install -r requirements.txt

echo Update complete! Latest changes and packages are installed.
pause