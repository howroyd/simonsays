import pathlib

import PyInstaller.__main__

DIRPATH = pathlib.Path().absolute()


def build() -> None:
    PyInstaller.__main__.run([
        f'{DIRPATH / "src" / "simonsays_drgreengiant" / "main.py"}',
        # '--clean',
        '-n', DIRPATH.name,
        '--onefile',
        '--noconfirm',
        '--log-level', 'WARN',
        '--hidden-import', 'pynput.keyboard._win32',
        '--hidden-import', 'pynput.mouse._win32',
        '--add-data', f'{DIRPATH / "README.md"};.',
        '--add-data', f'{DIRPATH / "LICENSE"};.',
        '--add-data', f'{DIRPATH / "CONTRIBUTING.md"};.',
        '--add-data', f'{DIRPATH / "CODE_OF_CONDUCT.md"};.',
        '--add-data', f'{DIRPATH / "assets" / "Green_tato_640.png"};img',
        '-i', f'{DIRPATH / "assets" / "Green_tato_640.png"}',
        # '-n %CurrDirName%',
    ])


if __name__ == "__main__":
    build()
