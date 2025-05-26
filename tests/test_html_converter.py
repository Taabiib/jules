import unittest
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, '..', 'src')
sys.path.insert(0, src_dir)
sample_files_dir = os.path.join(current_dir, '..', 'sample_files')

from html_converter import html_to_text

class TestHtmlConverter(unittest.TestCase):
    def setUp(self):
        self.dummy_html_path = os.path.join(sample_files_dir, "dummy.html")
        # Ensure dummy.html exists, otherwise skip
        if not os.path.exists(self.dummy_html_path):
            self.skipTest(f"Dummy HTML file not found at {self.dummy_html_path}")

    def test_html_to_text_extraction(self):
        extracted_text = html_to_text(self.dummy_html_path)
        # BeautifulSoup's get_text with separator='\n' and strip=True
        # on "<html><head><title>Test HTML</title></head><body><p>This is a dummy HTML file for testing.</p></body></html>"
        # should result in "Test HTML\nThis is a dummy HTML file for testing."
        expected_text = "Test HTML\nThis is a dummy HTML file for testing."
        self.assertEqual(extracted_text, expected_text)

    def test_html_file_not_found(self):
        extracted_text = html_to_text("non_existent_dummy.html")
        self.assertEqual(extracted_text, "")

if __name__ == '__main__':
    unittest.main()
