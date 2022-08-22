for %%I in (.) do set CurrDirName=%%~nxI
::echo %CurrDirName%

python -m pip install -U pyinstaller Pillow

pyinstaller --noconfirm --log-level=WARN ^
    --onefile ^
    --hidden-import "pynput.keyboard._win32" ^
    --hidden-import "pynput.mouse._win32" ^
    --add-data="README.md;." ^
    --add-data="katatoRIOT.png;img" ^
    --i katatoRIOT.png ^
    -n %CurrDirName% ^
    main.py

::--hidden-import "win32api" ^
::pyinstaller --onefile -n %CurrDirName% -i katatoRIOT.png main.py