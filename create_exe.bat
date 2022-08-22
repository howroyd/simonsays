for %%I in (.) do set CurrDirName=%%~nxI
::echo %CurrDirName%

python -m pip install -U pyinstaller Pillow

pyinstaller --noconfirm --log-level=WARN ^
    --onefile ^
    --hidden-import "win32api" ^
    --add-data="README.md;." ^
    --add-data="katatoRIOT.png;img" ^
    --i katatoRIOT.png ^
    -n %CurrDirName% ^
    main.py

::pyinstaller --onefile -n %CurrDirName% -i katatoRIOT.png main.py