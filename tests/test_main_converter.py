import unittest
import os
import sys
import json # For checking JSON content
import shutil # For cleaning up test output files/dirs

current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, '..', 'src')
sys.path.insert(0, src_dir)
sample_files_dir = os.path.join(current_dir, '..', 'sample_files') # For clarity

from main_converter import convert_file

class TestMainConverter(unittest.TestCase):
    def setUp(self):
        self.sample_txt_path = os.path.join(sample_files_dir, "sample.txt") # Created in previous step
        self.dummy_html_path = os.path.join(sample_files_dir, "dummy.html") # Created
        self.dummy_pdf_path = os.path.join(sample_files_dir, "dummy.pdf") # Not created
        self.dummy_png_path = os.path.join(sample_files_dir, "dummy.png") # Not created
        
        # Ensure base sample files exist for tests that rely on them
        if not os.path.exists(self.sample_txt_path):
             with open(self.sample_txt_path, "w", encoding="utf-8") as f: f.write("This is a test file.\nIt contains multiple lines.\nThe purpose is to test text extraction and conversion.")
             print(f"Warning: Fallback {self.sample_txt_path} created in setUp.")
        if not os.path.exists(self.dummy_html_path):
             with open(self.dummy_html_path, "w", encoding="utf-8") as f: f.write("<html><head><title>Test HTML</title></head><body><p>This is a dummy HTML file for testing.</p></body></html>")
             print(f"Warning: Fallback {self.dummy_html_path} created in setUp.")

        # Define a directory for test outputs from main_converter
        self.test_output_dir = os.path.join(current_dir, "test_outputs_main_converter")
        if os.path.exists(self.test_output_dir):
            shutil.rmtree(self.test_output_dir)
        os.makedirs(self.test_output_dir)
        self.original_cwd = os.getcwd()
        os.chdir(self.test_output_dir) # Change CWD so output files are here

    def tearDown(self):
        os.chdir(self.original_cwd) # Restore CWD
        if os.path.exists(self.test_output_dir):
            shutil.rmtree(self.test_output_dir)
        
        # Clean up any output files that might have been created in sample_files_dir by mistake
        # (convert_file creates output relative to input file's dir if not in CWD)
        # This is a safeguard; ideally, output path logic in main_converter should be robust.
        # The current main_converter.py creates output as "filename.format" in the CWD.
        # So this cleanup in sample_files_dir might not be strictly necessary if CWD is managed well.
        extensions_to_clean = ['.json', '.csv']
        # Base name of sample files without extension
        base_sample_txt = os.path.join(sample_files_dir, "sample")
        base_dummy_html = os.path.join(sample_files_dir, "dummy")

        files_to_clean_in_samples = []
        for ext in extensions_to_clean:
            files_to_clean_in_samples.append(base_sample_txt + ext)
            files_to_clean_in_samples.append(base_dummy_html + ext)
            # Add pdf/png if they were ever created
            if os.path.exists(self.dummy_pdf_path):
                 files_to_clean_in_samples.append(os.path.join(sample_files_dir, "dummy.pdf") + ext)
            if os.path.exists(self.dummy_png_path):
                 files_to_clean_in_samples.append(os.path.join(sample_files_dir, "dummy.png") + ext)


        for file_path in files_to_clean_in_samples:
            # Check if the path is absolute; if not, make it so relative to test_output_dir (where CWD was)
            # This part of teardown needs careful review of where files are actually written by convert_file
            # The current convert_file writes os.path.splitext(input_file_path)[0] + "." + output_format
            # So if input_file_path is absolute, output is in same dir as input.
            # If input_file_path is relative, output is relative to CWD.
            # The tests pass absolute paths to convert_file so outputs are next to inputs.
            if os.path.exists(file_path):
                 # print(f"DEBUG: Removing {file_path} from tearDown (safeguard).")
                 # os.remove(file_path)
                 pass # Output files should be in self.test_output_dir due to CWD change

    def test_txt_to_json(self):
        # convert_file expects absolute path for input if we want predictable output path
        abs_input_path = os.path.abspath(self.sample_txt_path)
        success, result = convert_file(abs_input_path, "json")
        self.assertTrue(success, f"Conversion failed: {result}")
        self.assertTrue(os.path.exists(result), f"Output file {result} not found.")
        with open(result, 'r', encoding='utf-8') as f:
            data = json.load(f)
        self.assertIn("text", data)
        self.assertEqual(data["text"], "This is a test file.\nIt contains multiple lines.\nThe purpose is to test text extraction and conversion.")
        if os.path.exists(result): os.remove(result) # Clean up specific output

    def test_txt_to_csv(self):
        abs_input_path = os.path.abspath(self.sample_txt_path)
        success, result = convert_file(abs_input_path, "csv")
        self.assertTrue(success, f"Conversion failed: {result}")
        self.assertTrue(os.path.exists(result))
        with open(result, 'r', encoding='utf-8') as f:
            content = f.read()
        self.assertIn("text", content) # header
        # CSV content from multi-line text is usually quoted
        self.assertIn("\"This is a test file.\\nIt contains multiple lines.\\nThe purpose is to test text extraction and conversion.\"", content)
        if os.path.exists(result): os.remove(result)


    def test_html_to_json(self):
        abs_input_path = os.path.abspath(self.dummy_html_path)
        success, result = convert_file(abs_input_path, "json")
        self.assertTrue(success, f"Conversion failed: {result}")
        self.assertTrue(os.path.exists(result))
        with open(result, 'r', encoding='utf-8') as f:
            data = json.load(f)
        self.assertIn("text", data)
        self.assertEqual(data["text"], "Test HTML\nThis is a dummy HTML file for testing.")
        if os.path.exists(result): os.remove(result)

    def test_html_to_csv(self):
        abs_input_path = os.path.abspath(self.dummy_html_path)
        success, result = convert_file(abs_input_path, "csv")
        self.assertTrue(success, f"Conversion failed: {result}")
        self.assertTrue(os.path.exists(result))
        with open(result, 'r', encoding='utf-8') as f:
            content = f.read()
        self.assertIn("text", content)
        # CSV content from multi-line text is usually quoted
        self.assertIn("\"Test HTML\\nThis is a dummy HTML file for testing.\"", content)
        if os.path.exists(result): os.remove(result)
    
    @unittest.skipIf(not os.path.exists(os.path.join(sample_files_dir, "dummy.pdf")), "dummy.pdf not found")
    def test_pdf_conversion_skipped(self):
        abs_input_path = os.path.abspath(self.dummy_pdf_path)
        success, result = convert_file(abs_input_path, "json")
        # Behavior depends on pdf_converter. If it returns empty string and main_converter proceeds,
        # this might pass or fail based on expected output.
        # Given dummy.pdf is not created, this test is skipped. If it were, we'd assert content.
        self.assertTrue(success) # Placeholder if file existed.

    @unittest.skipIf(not os.path.exists(os.path.join(sample_files_dir, "dummy.png")), "dummy.png not found")
    def test_image_conversion_skipped(self):
        abs_input_path = os.path.abspath(self.dummy_png_path)
        success, result = convert_file(abs_input_path, "json")
        # Similar to PDF, depends on image_converter and Tesseract.
        # Skipped if dummy.png not present.
        self.assertTrue(success) # Placeholder if file existed.


    def test_file_not_found(self):
        # Ensure CWD is back to original for this test, or use absolute path for non_existent_file
        # to avoid confusion about where it's looking.
        # convert_file prepends CWD if path is not absolute.
        # The main_converter.py's convert_file itself doesn't prepend os.getcwd().
        # It's app.py that does it.
        # So, for this test, providing a relative path is fine.
        non_existent_path = "non_existent_file.txt"
        if os.path.exists(non_existent_path): os.remove(non_existent_path) # ensure it doesn't exist
        
        success, message = convert_file(non_existent_path, "json")
        self.assertFalse(success)
        self.assertIn("Input file not found", message)

    def test_unsupported_file_type(self):
        # Create a dummy file with an unsupported extension in the test_output_dir
        unsupported_file_path = os.path.join(self.test_output_dir, "dummy.unsupported")
        with open(unsupported_file_path, "w", encoding="utf-8") as f:
            f.write("test")
        
        # Provide absolute path to convert_file to ensure it finds it
        abs_unsupported_path = os.path.abspath(unsupported_file_path)
        success, message = convert_file(abs_unsupported_path, "json")
        
        self.assertFalse(success)
        self.assertIn("Unsupported file type", message)
        # No need to os.remove(unsupported_file_path) as tearDown will remove self.test_output_dir

if __name__ == '__main__':
    # To run tests and ensure CWD is managed correctly for outputs,
    # it's better to run via 'python -m unittest discover tests' from project root,
    # or specific test file 'python tests/test_main_converter.py'
    unittest.main()
