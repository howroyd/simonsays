#!./.venv/bin/python3
import importlib.metadata
import pathlib
import platform

import PyInstaller.__main__ as pyinstaller

VERSION = importlib.metadata.version("simonsays-drgreengiant")
DIRPATH = pathlib.Path().absolute()
ENTRYPOINT = f'{DIRPATH / "main.py"}'
NAME = f"{DIRPATH.name}-{VERSION.replace('.', '_')}"

PYNPUT_KEYBOARD_IMPORTS = [
    "pynput.keyboard._base",
    "pynput.keyboard._darwin",
    "pynput.keyboard._uintput",
    "pynput.keyboard._win32",
    "pynput.keyboard._xorg",
]

PYNPUT_MOUSE_IMPORTS = [
    "pynput.mouse._base",
    "pynput.mouse._darwin",
    "pynput.mouse._win32",
    "pynput.mouse._xorg",
]

SEPARATOR = ";" if platform.platform().startswith("Windows") else ":"
DATAFILES = [
    f'{DIRPATH / ".env"}{SEPARATOR}.',
    f'{DIRPATH / "README.md"}{SEPARATOR}.',
    f'{DIRPATH / "LICENSE"}{SEPARATOR}.',
    f'{DIRPATH / "CONTRIBUTING.md"}{SEPARATOR}.',
    f'{DIRPATH / "CODE_OF_CONDUCT.md"}{SEPARATOR}.',
    f'{DIRPATH / "src" / "simonsays_drgreengiant" / "assets" / "Green_tato_640.png"}{SEPARATOR}assets',
]

ICON = f'{DIRPATH / "src" / "simonsays_drgreengiant" / "assets" / "Green_tato_640.png"}'


def build() -> None:
    """Build the executable"""
    envpath = DIRPATH / ".env"
    with open(envpath, "w") as f:
        f.write(f"VERSION={VERSION}\n")

    hidden_imports = (("--hidden-import", item) for item in PYNPUT_KEYBOARD_IMPORTS + PYNPUT_MOUSE_IMPORTS)
    hidden_imports = [item for tup in hidden_imports for item in tup]

    add_data = (("--add-data", item) for item in DATAFILES)
    add_data = [item for tup in add_data for item in tup]

    pyinstaller.run([
        ENTRYPOINT,
        # '--clean',
        '-n', NAME,
        '--onefile',
        '--noconfirm',
        '--log-level', 'WARN',
        *hidden_imports,
        *add_data,
        '-i', ICON,
    ])

    envpath.unlink()


if __name__ == "__main__":
    build()
