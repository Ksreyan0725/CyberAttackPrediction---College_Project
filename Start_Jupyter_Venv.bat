@echo off
echo Starting Jupyter Notebook using the .venv...
call .venv\Scripts\activate.bat
cd CyberAttackPrediction
jupyter notebook
pause
