# Manual Testing Checklist for Taabiib Converter v2 (GUI)

This checklist is for manually testing the Taabiib Converter v2 GUI application,
both when run from source and as a packaged executable.

## I. Setup Verification

-   [ ] **Running from Source:**
    -   [ ] Python virtual environment created and activated.
    -   [ ] All dependencies from `requirements.txt` installed successfully (`pip install -r requirements.txt`).
    -   [ ] Tesseract OCR engine installed and `tesseract --version` runs from the command line.
-   [ ] **Packaged Executable (Post-PyInstaller Build):**
    -   [ ] Tesseract OCR engine installed (as above) - this is external to the packaged app.

## II. GUI Application - Basic Functionality (Run from source `python src/app_ui.py` AND as packaged executable)

-   [ ] **Application Launch:**
    -   [ ] Application window opens without errors.
    -   [ ] Window title shows "Taabiib File Converter v0.2.0" (or current version).
    -   [ ] Initial status message is "Welcome! Select file, format, output dir (optional), then Convert."
-   [ ] **File Selection:**
    -   [ ] "Browse Input File" button opens a file dialog.
    -   [ ] File dialog filters for supported file types.
    -   [ ] Selecting a file updates the input file path field (read-only).
    -   [ ] Status message updates to "Selected: [filename]".
    -   [ ] If an output directory hasn't been chosen, selecting an input file automatically populates the output directory field with the input file's directory.
-   [ ] **Output Directory Selection:**
    -   [ ] "Browse Output Dir" button opens a directory selection dialog.
    -   [ ] Selecting a directory updates the output directory path field.
    -   [ ] User can manually type into the output directory field.
-   [ ] **Output Format Selection:**
    -   [ ] "JSON" is selected by default.
    -   [ ] User can switch between "JSON" and "CSV" radio buttons.
-   [ ] **"About" Dialog:**
    -   [ ] "About" button opens a dialog.
    -   [ ] Dialog shows correct app name, version, and description.
    -   [ ] Dialog can be closed.

## III. Conversion Logic (Test with various file types)

For each test, try both JSON and CSV output. Test with output directory specified and unspecified (should default to input file's dir).

-   [ ] **Text File (`.txt`):**
    -   [ ] Select a sample `.txt` file.
    -   [ ] Click "Convert File".
    -   [ ] Status updates to "Converting..." then "Success! Output saved to: [path_to_output_file]".
    -   [ ] Output file is created at the correct location (selected output dir or input dir).
    -   [ ] JSON output is valid and contains the text.
    -   [ ] CSV output is valid and contains the text.
-   [ ] **HTML File (`.html`):**
    -   [ ] Select a sample `.html` file (e.g., `sample_files/dummy.html`).
    -   [ ] Conversion successful.
    -   [ ] Output file created correctly.
    -   [ ] JSON/CSV output contains extracted text from HTML.
-   [ ] **PDF File (`.pdf`):**
    -   [ ] Select a sample `.pdf` file.
    -   [ ] Conversion successful.
    -   [ ] Output file created correctly.
    -   [ ] JSON/CSV output contains extracted text from PDF.
-   [ ] **Image File (`.png`, `.jpg`) - Tesseract Dependent:**
    -   [ ] **If Tesseract is installed correctly:**
        -   [ ] Select a sample image file with clear text.
        -   [ ] Conversion successful.
        -   [ ] Output file created correctly.
        -   [ ] JSON/CSV output contains OCR'd text from the image.
    -   [ ] **If Tesseract is NOT installed or configured correctly:**
        -   [ ] Select an image file.
        -   [ ] Conversion attempt.
        -   [ ] Status message shows an error like "Error: Could not extract text from image... Tesseract OCR engine might be missing..."
-   [ ] **Empty Input File:**
    -   [ ] Convert an empty `.txt` file.
    -   [ ] Status shows success (or warning about no text content).
    -   [ ] Output file is created (empty JSON object or CSV with headers only).
-   [ ] **File with No Extractable Text (e.g., PDF image without OCR layer, image with no text):**
    -   [ ] Conversion process completes.
    -   [ ] For images, if Tesseract is working, it should produce an empty text result.
    -   [ ] Status indicates success but output might be empty (e.g. `{"text": ""}`).

## IV. Error Handling (GUI)

-   [ ] **Convert without selecting input file:**
    -   [ ] Status shows "Error: Please select an input file first."
-   [ ] **Input file not found (e.g., path typed manually and incorrect):**
    -   [ ] (This case is harder to trigger if browse is always used) If possible to type a non-existent path and convert:
    -   [ ] Status shows "Error: Input file not found..."
-   [ ] **Unsupported file type (e.g., a `.zip` file selected by choosing "All files"):**
    -   [ ] Status shows "Error: Unsupported file type..."
-   [ ] **Output directory not writable / invalid (if typed manually):**
    -   [ ] Status shows an error related to creating/writing the output file or directory.

## V. Packaged Application Specifics (`dist/TaabiibConverter.exe`)

-   [ ] **Launch:** Application launches without needing Python installed separately.
-   [ ] **Performance:**
    -   [ ] Startup time (especially for `onefile` builds) is acceptable.
    -   [ ] Conversion speed is comparable to running from source.
-   [ ] **Dependencies:**
    -   [ ] All functionalities work, indicating Python dependencies were bundled correctly by PyInstaller (except Tesseract engine).
    -   [ ] `customtkinter` themes load correctly.

## VI. Unit Tests

-   [ ] Navigate to the project root in a terminal.
-   [ ] Activate virtual environment (if applicable).
-   [ ] Run `python -m unittest discover tests`.
-   [ ] All existing tests for core logic should pass (PDF/Image tests might be skipped if samples/dependencies are missing, as before).

This checklist provides a good basis for you to test the application.
