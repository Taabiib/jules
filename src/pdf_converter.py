import pdfplumber

def pdf_to_text(pdf_path: str) -> str:
    """
    Extracts text from all pages of a PDF file.

    Args:
        pdf_path: The path to the PDF file.

    Returns:
        A string containing all extracted text.
        Returns an empty string if the PDF cannot be opened or no text is found.
    """
    full_text = []
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text: # Ensure text was extracted
                    full_text.append(page_text)
        return "\n".join(full_text)
    except Exception as e:
        print(f"Error processing PDF file {pdf_path}: {e}")
        return "" # Return empty string or raise a custom exception

if __name__ == '__main__':
    # This block is for basic, manual testing.
    # To run this, you would need a sample PDF file.
    # For example, create a dummy file named 'sample.pdf' in the root directory
    # or provide a path to an existing PDF.
    
    # print("Attempting to create a dummy PDF for testing (requires reportlab)...")
    # try:
    #     from reportlab.pdfgen import canvas
    #     from reportlab.lib.pagesizes import letter
    #     c = canvas.Canvas("dummy_sample.pdf", pagesize=letter)
    #     c.drawString(100, 750, "Hello World from ReportLab!")
    #     c.drawString(100, 730, "This is a test PDF document generated to test pdf_to_text function.")
    #     c.showPage()
    #     c.save()
    #     print("dummy_sample.pdf created successfully.")
    #     text_content = pdf_to_text("dummy_sample.pdf")
    #     if text_content:
    #         print("\n------ Extracted PDF Text ------")
    #         print(text_content)
    #     else:
    #         print("\nNo text extracted or error during extraction.")
    # except ImportError:
    #     print("\nReportLab not installed. Skipping dummy PDF creation.")
    #     print("Please place a sample PDF (e.g., 'sample.pdf') in the root directory and uncomment below to test:")
    
    # Example of testing with a placeholder file path:
    # Ensure 'sample_files/test.pdf' exists or change the path.
    # sample_pdf_path = "sample_files/test.pdf" 
    # print(f"\nTesting with PDF: {sample_pdf_path}")
    # extracted_text = pdf_to_text(sample_pdf_path)
    # if extracted_text:
    # print("Extracted Text:\n", extracted_text)
    # else:
    # print("No text could be extracted or the file was not found/processed correctly.")
    pass # Keep the main block minimal for now
