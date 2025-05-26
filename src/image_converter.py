from PIL import Image
import pytesseract

def image_to_text(image_path: str) -> str:
    """
    Extracts text from an image file (PNG, JPG) using OCR.

    Args:
        image_path: The path to the image file.

    Returns:
        A string containing the extracted text.
        Returns an empty string if the image cannot be processed or no text is found.
        Prints an error if Tesseract is not installed or found.
    """
    try:
        # You might need to tell pytesseract where Tesseract is installed,
        # e.g., pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'
        # This is often needed on Linux or macOS if not in PATH.
        # On Windows, it might be:
        # pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        # This path should be verified by the user or handled via configuration.
        
        img = Image.open(image_path)
        text_content = pytesseract.image_to_string(img)
        return text_content.strip()
    except FileNotFoundError:
        print(f"Error: Image file not found at {image_path}")
        return ""
    except pytesseract.TesseractNotFoundError:
        print("Error: Tesseract is not installed or not found in your PATH.")
        print("Please install Tesseract OCR engine and make sure it's accessible.")
        print("For Windows, you might need to set: pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'")
        print("For Linux/macOS, ensure tesseract is in your PATH or set the command path.")
        return "" # Or raise an exception
    except Exception as e:
        print(f"Error processing image file {image_path}: {e}")
        return ""

if __name__ == '__main__':
    # This block is for basic, manual testing.
    # To run this, you would need:
    # 1. Tesseract OCR engine installed and configured.
    # 2. A sample image file (e.g., 'sample.png' or 'sample.jpg').
    #    You can create one with some text using any image editor.

    # print("Ensure Tesseract OCR is installed and configured in your system PATH or via pytesseract.tesseract_cmd.")
    
    # Example of testing with a placeholder file path:
    # Ensure 'sample_files/test_image.png' exists or change the path.
    # sample_image_path = "sample_files/test_image.png" 
    # print(f"\nTesting with Image: {sample_image_path}")
    # extracted_text = image_to_text(sample_image_path)
    # if extracted_text:
    #     print("Extracted Text:\n", extracted_text)
    # else:
    #     print("No text could be extracted, or the file was not found, or Tesseract is not set up correctly.")
    pass # Keep the main block minimal for now
