import os
from src.text_converter import text_to_json, text_to_csv
from src.pdf_converter import pdf_to_text
from src.html_converter import html_to_text
from src.image_converter import image_to_text

def convert_file(input_file_path: str, output_format: str, output_dir: str = None) -> tuple[bool, str]:
    """
    Converts a given file to the specified output format (JSON or CSV).

    Args:
        input_file_path: Path to the input file.
        output_format: Desired output format ('json' or 'csv').

    Returns:
        A tuple (success_status, message_or_output_path).
        success_status (bool): True if conversion was successful, False otherwise.
        message_or_output_path (str): Path to the output file if successful, 
                                      or an error message if not.
    """
    if not os.path.exists(input_file_path):
        return False, f"Error: Input file not found at {input_file_path}"

    file_name, file_ext = os.path.splitext(input_file_path)
    file_ext = file_ext.lower()

    text_content = None

    if file_ext == '.txt':
        try:
            with open(input_file_path, 'r', encoding='utf-8') as f:
                text_content = f.read()
        except Exception as e:
            return False, f"Error reading text file {input_file_path}: {e}"
    elif file_ext == '.pdf':
        text_content = pdf_to_text(input_file_path)
    elif file_ext == '.html' or file_ext == '.htm':
        text_content = html_to_text(input_file_path)
    elif file_ext in ['.png', '.jpg', '.jpeg']:
        text_content = image_to_text(input_file_path)
        if text_content is None: # image_to_text might return None on file not found, or "" on Tesseract error
             return False, f"Error processing image file {input_file_path}. File may be corrupted or unreadable."
        if not text_content.strip() and os.path.getsize(input_file_path) > 0: # Check if file has content but OCR yielded nothing
            # This is a heuristic. image_to_text prints specific Tesseract errors.
            # We're trying to give a more UI-friendly hint here.
            return False, f"Error: Could not extract text from image '{os.path.basename(input_file_path)}'. Tesseract OCR engine might be missing or not configured correctly. Please check README for Tesseract installation instructions."
    else:
        return False, f"Error: Unsupported file type '{file_ext}'. Supported types: .txt, .pdf, .html, .htm, .png, .jpg, .jpeg"

    # It's possible text_content is None from PDF/HTML converters if they had an internal unhandled error returning None
    if text_content is None: 
        return False, f"Error: Could not extract text content from {input_file_path}. The file might be corrupted or the specific converter failed."
    
    # If text_content is an empty string (but not None), it means extraction happened but found no text.
    # For non-image files, this is usually fine (e.g. empty txt or pdf).
    # For images, if it's empty and we didn't trigger the Tesseract specific error above, it might genuinely be an image with no text.
    if not text_content.strip() and file_ext not in ['.png', '.jpg', '.jpeg']: 
        print(f"Warning: No text content found in {input_file_path}. Output will be empty.")

    # Determine output path
    base_input_filename = os.path.basename(input_file_path)
    name_part, _ = os.path.splitext(base_input_filename)
    output_filename = f"{name_part}.{output_format}"

    if output_dir and os.path.isdir(output_dir):
        output_file_path = os.path.join(output_dir, output_filename)
    else:
        # Default to same directory as input if output_dir is not provided or invalid
        input_file_dir = os.path.dirname(input_file_path)
        output_file_path = os.path.join(input_file_dir, output_filename)
    
    # Ensure the chosen output directory actually exists before writing
    final_output_dir_for_file = os.path.dirname(output_file_path)
    if not os.path.exists(final_output_dir_for_file):
        try:
            os.makedirs(final_output_dir_for_file, exist_ok=True)
        except Exception as e:
            return False, f"Error: Could not create output directory {final_output_dir_for_file}: {e}"

    output_data = ""

    if output_format == 'json':
        output_data = text_to_json(text_content)
    elif output_format == 'csv':
        output_data = text_to_csv(text_content)
    else:
        return False, f"Error: Unsupported output format '{output_format}'. Supported: json, csv"

    try:
        with open(output_file_path, 'w', encoding='utf-8') as f:
            f.write(output_data)
        return True, output_file_path
    except Exception as e:
        return False, f"Error writing output file {output_file_path}: {e}"

if __name__ == '__main__':
    # This block is for manual testing.
    # You would need to:
    # 1. Create sample files in the root or 'sample_files' directory.
    #    - e.g., 'sample_files/test.txt', 'sample_files/test.pdf', etc.
    # 2. Ensure all dependencies (including Tesseract for images) are installed.
    
    print("Main Converter: Manual Testing Block")
    print("Ensure you have sample files in a 'sample_files' directory relative to the script location or root.")
    print("Also ensure all libraries and Tesseract (for images) are installed.")

    # Create dummy files for testing if they don't exist (basic versions)
    sample_dir = "sample_files_main_test"
    if not os.path.exists(sample_dir):
        os.makedirs(sample_dir)

    # Dummy TXT
    if not os.path.exists(os.path.join(sample_dir, "sample.txt")):
        with open(os.path.join(sample_dir, "sample.txt"), "w") as f:
            f.write("This is a test text file.")
    
    # Dummy HTML (very basic)
    if not os.path.exists(os.path.join(sample_dir, "sample.html")):
        with open(os.path.join(sample_dir, "sample.html"), "w") as f:
            f.write("<html><body><h1>Test HTML</h1><p>Some text.</p></body></html>")

    # Note: PDF and Image dummy creation is more complex and handled by their respective modules if needed.
    # For this test, assume they exist or skip them.

    test_files = [
        (os.path.join(sample_dir, "sample.txt"), "json"),
        (os.path.join(sample_dir, "sample.txt"), "csv"),
        (os.path.join(sample_dir, "sample.html"), "json"),
        # Add paths to actual PDF/Image files here for more thorough testing
        # (os.path.join(sample_dir, "sample.pdf"), "json"), 
        # (os.path.join(sample_dir, "sample.png"), "csv"),
    ]

    for file_path, out_format in test_files:
        print(f"\nConverting {file_path} to {out_format}...")
        if not os.path.exists(file_path):
            print(f"SKIPPING: {file_path} does not exist.")
            continue
        
        success, result = convert_file(file_path, out_format)
        if success:
            print(f"Successfully converted. Output at: {result}")
            # Optionally print content of small files
            # with open(result, 'r') as f:
            #     print("--- Output Content ---")
            #     print(f.read(200)) # Print first 200 chars
            #     print("----------------------")
        else:
            print(f"Conversion failed: {result}")
    
    # Clean up dummy files (optional)
    # import shutil
    # if os.path.exists(sample_dir):
    #     shutil.rmtree(sample_dir)
    #     print(f"Cleaned up {sample_dir}")
