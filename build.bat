@echo off
setlocal
if not defined EU5_PYTHON set "EU5_PYTHON=C:\Users\Hades\anaconda3\envs\eu5\python.exe"
"%EU5_PYTHON%" "%~dp0scripts\build.py" %*
exit /b %errorlevel%
