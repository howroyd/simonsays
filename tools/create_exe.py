import pathlib
import platform

import PyInstaller.__main__

DIRPATH = pathlib.Path().absolute()
SEPARATOR = ";" if platform.platform().startswith("Windows") else ":"


def build() -> None:
    PyInstaller.__main__.run([
        f'{DIRPATH / "main.py"}',
        # '--clean',
        '-n', DIRPATH.name,
        '--onefile',
        '--noconfirm',
        '--log-level', 'WARN',
        '--hidden-import', 'pynput.keyboard._win32',
        '--hidden-import', 'pynput.mouse._win32',
        '--add-data', f'{DIRPATH / "README.md"}{SEPARATOR}.',
        '--add-data', f'{DIRPATH / "LICENSE"}{SEPARATOR}.',
        '--add-data', f'{DIRPATH / "CONTRIBUTING.md"}{SEPARATOR}.',
        '--add-data', f'{DIRPATH / "CODE_OF_CONDUCT.md"}{SEPARATOR}.',
        '--add-data', f'{DIRPATH / "assets" / "Green_tato_640.png"}{SEPARATOR}img',
        '-i', f'{DIRPATH / "assets" / "Green_tato_640.png"}',
        # '-n %CurrDirName%',
    ])


if __name__ == "__main__":
    build()
