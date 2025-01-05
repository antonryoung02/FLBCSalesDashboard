@echo off
cd C:\Users\info\OneDrive\Desktop\FLBC 1.1.1\Revenue and menu engineering data\FLBCSalesDashboard\

set PYTHONPATH=%CD%

echo Activating virtual environment
call C:\\Users\info\Miniconda3\condabin\conda.bat activate sales_dashboard 

echo Running application
start cmd /k "streamlit run app\main.py"