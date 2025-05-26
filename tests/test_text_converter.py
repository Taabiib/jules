import unittest
import os
import sys
import json # For comparing JSON objects if string comparison is too brittle

# Add src directory to Python path to import modules from src
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, '..', 'src')
sys.path.insert(0, src_dir)

from text_converter import text_to_json, text_to_csv

class TestTextConverter(unittest.TestCase):
    def setUp(self):
        # Create sample files directory if it doesn't exist
        self.test_files_dir = os.path.join(current_dir, 'test_generated_files') # Store test-specific files separately
        if not os.path.exists(self.test_files_dir):
            os.makedirs(self.test_files_dir)
        
        self.sample_text_content = "Hello World\nSecond Line"
        self.sample_text_path = os.path.join(self.test_files_dir, "test_sample_for_text_converter.txt")
        with open(self.sample_text_path, "w", encoding="utf-8") as f:
            f.write(self.sample_text_content)

    def tearDown(self):
        # Clean up created files
        if os.path.exists(self.sample_text_path):
            os.remove(self.sample_text_path)
        if os.path.exists(self.test_files_dir):
            # Potentially remove other files or the directory itself if empty and safe
            if not os.listdir(self.test_files_dir): # Check if dir is empty
                 os.rmdir(self.test_files_dir)


    def test_text_to_json(self):
        content = "Hello World"
        # Comparing loaded JSON objects is more robust than string comparison
        # expected_json_obj = {"text": "Hello World"}
        # self.assertEqual(json.loads(text_to_json(content)), expected_json_obj)
        # However, the prompt asks for string comparison. Let's stick to that but be mindful of formatting.
        # The function text_to_json produces indent=4
        expected_json_str = '{\n    "text": "Hello World"\n}'
        self.assertEqual(text_to_json(content), expected_json_str)

    def test_text_to_csv(self):
        content = "Hello World"
        # Pandas to_csv by default includes a newline at the end.
        expected_csv = 'text\nHello World\n' 
        self.assertEqual(text_to_csv(content), expected_csv)
        
    def test_text_to_csv_multi_line(self):
        content = "Line1\nLine2"
        # When a field contains a newline, pandas quotes it.
        expected_csv = 'text\n"Line1\\nLine2"\n' # The \n within the string is literal here
        self.assertEqual(text_to_csv(content), expected_csv)

    def test_text_to_json_from_file_content(self):
        # Test with content read from the sample file created in setUp
        expected_json_obj = {"text": self.sample_text_content}
        self.assertEqual(json.loads(text_to_json(self.sample_text_content)), expected_json_obj)

    def test_text_to_csv_from_file_content(self):
        # Test with content read from the sample file
        # The content "Hello World\nSecond Line" should be quoted in CSV
        expected_csv = 'text\n"Hello World\\nSecond Line"\n'
        self.assertEqual(text_to_csv(self.sample_text_content), expected_csv)

if __name__ == '__main__':
    unittest.main()
