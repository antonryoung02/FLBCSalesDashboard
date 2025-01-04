@echo off
cd <path\to\your\streamlit\app>

echo Activating virtual environment
call <path\to\conda\Scripts\activate>

conda activate <your_env_name>

echo Running application
start cmd /k "conda activate <your_env_name> && streamlit run <main.py>"