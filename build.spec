# build.spec for Taabiib Converter 2

import PyInstaller.utils.hooks

def get_customtkinter_datas():
    # Helper function to get customtkinter theme files
    import customtkinter
    import os
    datas = []
    customtkinter_path = os.path.dirname(customtkinter.__file__)
    # Add the 'assets' folder which contains themes, etc.
    assets_path = os.path.join(customtkinter_path, 'assets')
    if os.path.exists(assets_path):
        datas.append((assets_path, 'customtkinter/assets'))
    return datas

a = Analysis(
    ['src/app_ui.py'],
    pathex=['.'],  # Look for modules in the current directory (where build.spec is)
    binaries=[],
    datas=get_customtkinter_datas(), # Include customtkinter assets
    hiddenimports=[
        'tkinter', 'tkinter.filedialog', 'tkinter.messagebox', # Ensure tkinter modules are included
        'pdfplumber', 'PIL', 'pytesseract', 'pandas', 'bs4', # Core dependencies
        'customtkinter'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False
)

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='TaabiibConverter', # Name of the executable
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True, # UPX compression if available (makes executable smaller)
    console=False, # False for GUI applications, True for console applications
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    # icon='path/to/your/icon.ico' # Optional: specify an icon for the executable
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='TaabiibConverterApp' # Name of the folder in onedir mode (if not onefile)
)

# Note on onefile vs onedir:
# For 'onefile' mode, PyInstaller bundles everything into a single executable.
# This is convenient but can be slower to start and harder to debug.
# To use 'onefile' mode, you typically pass the --onefile flag to the pyinstaller command.
# The EXE call above is compatible with onefile mode.
#
# For 'onedir' mode (default if --onefile is not specified), PyInstaller creates a directory
# containing the executable and all its dependencies (DLLs, .pyc files, etc.).
# This starts faster and is easier to debug if something is missing.
# The `coll` object defines the collection for onedir mode.
#
# Command to build using this spec file:
# pyinstaller build.spec
#
# Or for onefile:
# pyinstaller --onefile build.spec
# (The spec file can also be configured to force onefile, but CLI flag is common)

# Handling pytesseract's 'tessdata':
# PyInstaller does NOT bundle the Tesseract OCR engine itself. Users must install it separately.
# PyInstaller *might* not automatically find pytesseract's required 'tessdata' path when bundled.
# If users report issues with OCR in the bundled app (e.g., "TesseractError: (1)"),
# you might need to explicitly tell pytesseract where to find Tesseract or bundle 'tessdata'
# if you are providing a portable Tesseract installation (which is advanced).
#
# A common approach for PyInstaller if pytesseract has issues:
# 1. Ensure TESSDATA_PREFIX environment variable is set on the user's system.
# 2. Or, in your Python code (app_ui.py or main_converter.py), before any pytesseract calls:
#    if getattr(sys, 'frozen', False): # If running in a PyInstaller bundle
#        pytesseract.pytesseract.tesseract_cmd = 'path_to_tesseract_in_bundle_or_system' # If you bundle tesseract
#        os.environ['TESSDATA_PREFIX'] = os.path.join(sys._MEIPASS, 'tessdata') # If you bundle tessdata
#
# For this basic spec, we are relying on the user having Tesseract installed and in PATH,
# and hoping PyInstaller picks up pytesseract's needs correctly or that pytesseract finds
# the system Tesseract.
