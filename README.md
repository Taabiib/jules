# Taabiib File Converter v2 (GUI Application)

This application provides a graphical user interface to convert various file types (PDF, Text, HTML, PNG, JPG) to JSON or CSV format.

## Features

- User-friendly GUI.
- Input file selection via a file browser.
- Output directory selection.
- Choice of output format (JSON/CSV).
- Status messages for ongoing operations and errors.
- Supported input formats:
    - `.txt` (Plain Text)
    - `.pdf` (Portable Document Format) - Text extraction only.
    - `.html`, `.htm` (HyperText Markup Language) - Extracts text content.
    - `.png` (Portable Network Graphics) - Extracts text using OCR.
    - `.jpg`, `.jpeg` (Joint Photographic Experts Group) - Extracts text using OCR.
- Output formats:
    - `.json` (JavaScript Object Notation)
    - `.csv` (Comma-Separated Values)

## IMPORTANT: Tesseract OCR Engine Prerequisite

For converting image files (`.png`, `.jpg`, `.jpeg`) to text, **Google's Tesseract OCR Engine must be installed on your system.** This application (even when packaged) uses `pytesseract` as a Python wrapper for Tesseract, but it does not bundle Tesseract itself.

**Please install Tesseract OCR before attempting to convert images:**

-   **Windows:**
    Download and run the Tesseract installer from the [official UB Mannheim page](https://github.com/UB-Mannheim/tesseract/wiki). **Ensure you add Tesseract to your system PATH during installation**, or note the installation path. If `pytesseract` cannot find Tesseract, you might need to configure its path within the application's code (not ideal for a distributed app) or ensure Tesseract's directory is in your PATH.
-   **macOS:**
    Using Homebrew: `brew install tesseract`
-   **Linux (Debian/Ubuntu):**
    `sudo apt update && sudo apt install tesseract-ocr`
-   **Other Systems:** Refer to the [Tesseract Installation Guide](https://tesseract-ocr.github.io/tessdoc/Installation.html).

After installation, verify Tesseract by running `tesseract --version` in your terminal. If this command works, the application should be able to use it.

## Setup and Running the Application

There are two ways to run the application:

**1. Running from Source Code (for development):**

    a.  **Clone the repository.**
    b.  **Create and activate a Python virtual environment:**
        ```bash
        python -m venv venv
        # Windows: venv\Scripts\activate
        # macOS/Linux: source venv/bin/activate
        ```
    c.  **Install dependencies:**
        ```bash
        pip install -r requirements.txt
        ```
    d.  **(Install Tesseract OCR as described above if you need image conversion.)**
    e.  **Run the UI application:**
        ```bash
        python src/app_ui.py
        ```

**2. Using the Packaged Executable (if provided):**

    a.  Download the `TaabiibConverter` executable (e.g., `TaabiibConverter.exe` on Windows) from the releases page or build it yourself (see below).
    b.  **(Install Tesseract OCR as described above if you need image conversion.)**
    c.  Run the executable. No Python installation is required on the user's machine for the packaged version.

## Building the Executable (using PyInstaller)

To package the application into a standalone executable:

1.  Ensure you have cloned the repository and set up the virtual environment.
2.  Install all dependencies, including `pyinstaller`:
    ```bash
    pip install -r requirements.txt 
    ```
3.  Navigate to the root directory of the project.
4.  Run PyInstaller with the provided spec file:
    ```bash
    pyinstaller build.spec
    ```
    Or, for a single-file executable (can be slower to start):
    ```bash
    pyinstaller --onefile build.spec
    ```
5.  The executable will be found in the `dist` directory (e.g., `dist/TaabiibConverter/TaabiibConverter.exe` or `dist/TaabiibConverter.exe`).

## Creating an Installer (e.g., for Windows)

The packaged executable from PyInstaller can be further bundled into a user-friendly installer.

-   **Windows:** Tools like [Inno Setup](https://jrsoftware.org/isinfo.php) or [NSIS](https://nsis.sourceforge.io/Main_Page) can be used. These tools take the output from PyInstaller (the `dist` folder) and create a `setup.exe` that guides users through installation, creates shortcuts, etc. Creating an Inno Setup script would involve:
    1.  Pointing it to the files in your PyInstaller `dist` folder.
    2.  Specifying application name, version, publisher.
    3.  Defining shortcuts.
    4.  **Crucially:** Reminding the user during installation (or via included documentation) to install Tesseract OCR separately if they need image conversion. It's complex to bundle Tesseract itself reliably within these installers for all user systems.

-   **macOS:** You can create `.dmg` disk images.
-   **Linux:** You might create `.deb` or `.rpm` packages or distribute as an AppImage.

**Note:** This project does not automatically create these installers. The focus is on providing the packaged application via PyInstaller.

## Developer & QA Testing

For detailed manual testing of all application features, including UI interactions, conversion processes, and error handling, please refer to the [MANUAL_TESTING_CHECKLIST.md](MANUAL_TESTING_CHECKLIST.md) file in this repository.

Unit tests for the core conversion logic can be run using:
```bash
python -m unittest discover tests
```

## Running Tests

(This section can be reviewed. The command above is now under "Developer & QA Testing". We can keep this as a more general note or merge fully.)

The primary method for running automated unit tests is described above.
Ensure Tesseract is installed if you expect image OCR tests to pass.
(Original note: Assuming tests from Taabiib Converter 1 are adapted/present)
