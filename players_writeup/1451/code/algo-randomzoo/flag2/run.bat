@echo off
for /l %%i in (6,1,100) do (
    echo Running python .\solver.py %%i
    python .\solver.py %%i
)
pause
