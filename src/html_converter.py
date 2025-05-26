from bs4 import BeautifulSoup

def html_to_text(html_path: str) -> str:
    """
    Extracts text content from an HTML file.

    Args:
        html_path: The path to the HTML file.

    Returns:
        A string containing all extracted text content.
        Returns an empty string if the HTML cannot be parsed or no text is found.
    """
    try:
        with open(html_path, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'html.parser')
        
        # Get all text from the body; you might want to refine this
        # depending on what text is considered relevant (e.g., ignore script/style tags)
        # BeautifulSoup's get_text() method is quite effective.
        text_content = soup.get_text(separator='\n', strip=True)
        return text_content
    except FileNotFoundError:
        print(f"Error: HTML file not found at {html_path}")
        return ""
    except Exception as e:
        print(f"Error processing HTML file {html_path}: {e}")
        return ""

if __name__ == '__main__':
    # This block is for basic, manual testing.
    # To run this, you would need a sample HTML file.
    # For example, create a dummy file named 'sample.html' in the root directory
    # or provide a path to an existing HTML file.

    # print("Attempting to create a dummy HTML for testing...")
    # dummy_html_content = """
    # <!DOCTYPE html>
    # <html>
    # <head>
    #     <title>Test Page</title>
    #     <style> body { font-family: sans-serif; } </style>
    # </head>
    # <body>
    #     <h1>Hello World!</h1>
    #     <p>This is a paragraph with <strong>strong</strong> text and also <em>emphasized</em> text.</p>
    #     <script> console.log("This should be ignored"); </script>
    #     <div>Another paragraph of text.</div>
    # </body>
    # </html>
    # """
    # try:
    #     with open("dummy_sample.html", "w", encoding="utf-8") as f:
    #         f.write(dummy_html_content)
    #     print("dummy_sample.html created successfully.")
        
    #     text_content = html_to_text("dummy_sample.html")
    #     if text_content:
    #         print("\n------ Extracted HTML Text ------")
    #         print(text_content)
    #     else:
    #         print("\nNo text extracted or error during extraction from dummy_sample.html.")
            
    # except Exception as e:
    #     print(f"Error during dummy HTML creation or processing: {e}")

    # Example of testing with a placeholder file path:
    # Ensure 'sample_files/test.html' exists or change the path.
    # sample_html_path = "sample_files/test.html" 
    # print(f"\nTesting with HTML: {sample_html_path}")
    # extracted_text = html_to_text(sample_html_path)
    # if extracted_text:
    # print("Extracted Text:\n", extracted_text)
    # else:
    # print("No text could be extracted or the file was not found/processed correctly.")
    pass # Keep the main block minimal for now
