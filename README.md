# File Converter Utility

This utility converts various file types (PDF, Text, HTML, PNG, JPG) to JSON or CSV format.
It extracts text content from the input files and structures it into the chosen output format.

## Features

- Supported input formats:
    - `.txt` (Plain Text)
    - `.pdf` (Portable Document Format) - Text extraction only.
    - `.html`, `.htm` (HyperText Markup Language) - Extracts text content.
    - `.png` (Portable Network Graphics) - Extracts text using OCR.
    - `.jpg`, `.jpeg` (Joint Photographic Experts Group) - Extracts text using OCR.
- Output formats:
    - `.json` (JavaScript Object Notation)
    - `.csv` (Comma-Separated Values)

## Setup

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```

2.  **Create and activate a virtual environment (recommended):**
    ```bash
    python -m venv venv
    # On Windows
    venv\Scripts\activate
    # On macOS/Linux
    source venv/bin/activate
    ```

3.  **Install Python dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Install Tesseract OCR Engine:**
    This step is **required** for converting image files (`.png`, `.jpg`, `.jpeg`) to text. `pytesseract` (the Python library used for OCR) is a wrapper around Google's Tesseract OCR Engine.

    -   **Windows:**
        Download and run the Tesseract installer from the [official UB Mannheim page](https://github.com/UB-Mannheim/tesseract/wiki). Ensure you add Tesseract to your system PATH during installation, or note the installation path. You might need to specify the path to `tesseract.exe` in `src/image_converter.py` if it's not in PATH (e.g., `pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'`).
    -   **macOS:**
        Using Homebrew:
        ```bash
        brew install tesseract
        ```
    -   **Linux (Debian/Ubuntu):**
        ```bash
        sudo apt update
        sudo apt install tesseract-ocr
        ```
    -   **Other Systems:** Refer to the [Tesseract Installation Guide](https://tesseract-ocr.github.io/tessdoc/Installation.html).

    After installation, verify Tesseract is working by running `tesseract --version` in your terminal.

## Usage

The application is run via the command-line interface (`app.py`).

**Syntax:**
```bash
python app.py <input_file_path> <output_format>
```

**Arguments:**
-   `input_file_path`: The full or relative path to the file you want to convert.
-   `output_format`: The desired output format. Must be either `json` or `csv`.

**Examples:**

1.  **Convert a text file to JSON:**
    ```bash
    python app.py sample_files/sample.txt json
    ```
    This will create `sample_files/sample.json`.

2.  **Convert an HTML file to CSV:**
    ```bash
    python app.py sample_files/dummy.html csv
    ```
    This will create `sample_files/dummy.csv`.

3.  **Convert a PNG image to JSON (requires Tesseract):**
    ```bash
    # Assuming you have a sample.png in sample_files
    python app.py sample_files/sample.png json
    ```
    This will create `sample_files/sample.json` containing text extracted from the image.

## Running Tests

To run the unit tests:
1.  Ensure you have installed all dependencies from `requirements.txt`.
2.  For image conversion tests to pass fully, Tesseract OCR must be installed and correctly configured. Sample PDF and Image files (`dummy.pdf`, `dummy.png`) are also needed for their respective tests; currently, these tests might be skipped or show expected failures if these files/dependencies are not set up.
3.  Navigate to the root directory of the project.
4.  Run the following command:
    ```bash
    python -m unittest discover tests
    ```
    Or, to run a specific test file:
    ```bash
    python -m unittest tests.test_main_converter
    ```
