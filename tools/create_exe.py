import os

import PyInstaller.__main__

DIRPATH = os.path.dirname(os.path.realpath(__file__))
DIRNAME = DIRPATH.split('\\')[-2]


def build() -> None:
    PyInstaller.__main__.run([
        f'{DIRPATH}\\main.py',
        # '--clean',
        '-n', DIRNAME,
        '--onefile',
        '--noconfirm',
        '--log-level', 'WARN',
        '--hidden-import', 'pynput.keyboard._win32',
        '--hidden-import', 'pynput.mouse._win32',
        '--add-data', f'{DIRPATH}\\README.md;.',
        '--add-data', f'{DIRPATH}\\LICENSE;.',
        '--add-data', f'{DIRPATH}\\CONTRIBUTING.md;.',
        '--add-data', f'{DIRPATH}\\CODE_OF_CONDUCT.md;.',
        '--add-data', f'{DIRPATH}\\assets\\Green_tato_640.png;img',
        '-i', f'{DIRPATH}\\assets\\Green_tato_640.png',
        # '-n %CurrDirName%',
    ])


if __name__ == "__main__":
    build()
