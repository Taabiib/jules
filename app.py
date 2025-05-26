import argparse
import os
from src.main_converter import convert_file

def main():
    parser = argparse.ArgumentParser(description="Convert files (pdf, text, html, png, jpg) to JSON or CSV.")
    parser.add_argument("input_file", help="Path to the input file.")
    parser.add_argument("output_format", 
                        choices=['json', 'csv'], 
                        help="Desired output format (json or csv).")

    args = parser.parse_args()

    input_file_path = args.input_file
    output_format = args.output_format.lower() # Ensure lowercase for consistency

    if not os.path.isabs(input_file_path):
        # If the path is not absolute, assume it's relative to the current working directory
        input_file_path = os.path.join(os.getcwd(), input_file_path)


    print(f"Processing {input_file_path} to {output_format}...")
    success, message = convert_file(input_file_path, output_format)

    if success:
        print(f"Successfully converted '{os.path.basename(input_file_path)}' to '{os.path.basename(message)}'.")
        print(f"Output saved to: {message}")
    else:
        print(f"Error: {message}")

if __name__ == "__main__":
    main()
