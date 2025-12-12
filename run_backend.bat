@echo off
REM Disable CUDA to avoid GPU crashes
set CUDA_VISIBLE_DEVICES=-1

REM Run the backend
python main.py
