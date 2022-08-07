for %%I in (.) do set CurrDirName=%%~nxI
::echo %CurrDirName%

python -m pip install -U pyinstaller
pyinstaller --onefile -n %CurrDirName% main.py