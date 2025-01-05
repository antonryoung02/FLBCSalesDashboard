@echo off
cd C:\Users\info\OneDrive\Desktop\FLBC 1.1.1\Revenue and menu engineering data\FLBCSalesDashboard\

echo Activating virtual environment
conda activate sales_dashboard 

echo Running application
start cmd /k "conda activate sales_dashboard && streamlit run app\main.py"