import os
import PyInstaller.__main__

DIRPATH = os.path.dirname(os.path.realpath(__file__))
DIRNAME = DIRPATH.split('\\')[-1]

PyInstaller.__main__.run([
    f'{DIRPATH}\\main.py',
    '--clean',
    '-n', DIRNAME,
    '--onefile',
    '--noconfirm',
    '--log-level', 'WARN',
    '--hidden-import', 'pynput.keyboard._win32',
    '--hidden-import', 'pynput.mouse._win32',
    '--add-data', f'{DIRPATH}\\README.md;.',
    '--add-data', f'{DIRPATH}\\katatoRIOT.png;img',
    '-i', 'katatoRIOT.png',
    #'-n %CurrDirName%',
])


#usage: pyinstaller [-h] [-v] [-D] [-F] [--specpath DIR] [-n NAME] [--add-data <SRC;DEST or SRC:DEST>] [--add-binary <SRC;DEST or SRC:DEST>] [-p DIR]
#                   [--hidden-import MODULENAME] [--collect-submodules MODULENAME] [--collect-data MODULENAME] [--collect-binaries MODULENAME]
#                   [--collect-all MODULENAME] [--copy-metadata PACKAGENAME] [--recursive-copy-metadata PACKAGENAME] [--additional-hooks-dir HOOKSPATH]
#                   [--runtime-hook RUNTIME_HOOKS] [--exclude-module EXCLUDES] [--key KEY] [--splash IMAGE_FILE] [-d {all,imports,bootloader,noarchive}]
#                   [--python-option PYTHON_OPTION] [-s] [--noupx] [--upx-exclude FILE] [-c] [-w] [-i <FILE.ico or FILE.exe,ID or FILE.icns or Image or "NONE">]        
#                   [--disable-windowed-traceback] [--version-file FILE] [-m <FILE or XML>] [--no-embed-manifest] [-r RESOURCE] [--uac-admin] [--uac-uiaccess]
#                   [--win-private-assemblies] [--win-no-prefer-redirects] [--argv-emulation] [--osx-bundle-identifier BUNDLE_IDENTIFIER] [--target-architecture ARCH]  
#                   [--codesign-identity IDENTITY] [--osx-entitlements-file FILENAME] [--runtime-tmpdir PATH] [--bootloader-ignore-signals] [--distpath DIR]
#                   [--workpath WORKPATH] [-y] [--upx-dir UPX_DIR] [-a] [--clean] [--log-level LEVEL]
#                   scriptname [scriptname ...]