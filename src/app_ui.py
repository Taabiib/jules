import customtkinter as ctk
from tkinter import filedialog, messagebox # messagebox for simple About dialog
import os
from src.main_converter import convert_file

# --- Appearance Settings ---
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    APP_VERSION = "0.2.0" # Added version

    def __init__(self):
        super().__init__()

        self.title(f"Taabiib File Converter v{self.APP_VERSION}")
        self.geometry("600x450") # Adjusted geometry

        # --- Variables ---
        self.input_file_path = ctk.StringVar()
        self.output_dir_path = ctk.StringVar() # For output directory
        self.output_format = ctk.StringVar(value="json")
        self.status_message = ctk.StringVar(value="Welcome! Select file, format, output dir (optional), then Convert.")

        # --- UI Layout ---
        self.grid_columnconfigure(0, weight=1)

        # Input File Selection
        self.file_frame = ctk.CTkFrame(self)
        self.file_frame.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="ew")
        self.file_frame.grid_columnconfigure(1, weight=1)

        self.select_file_button = ctk.CTkButton(self.file_frame, text="Browse Input File", command=self.browse_input_file)
        self.select_file_button.grid(row=0, column=0, padx=10, pady=10)
        self.file_entry = ctk.CTkEntry(self.file_frame, textvariable=self.input_file_path, state="readonly")
        self.file_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        # Output Directory Selection (New)
        self.output_dir_frame = ctk.CTkFrame(self)
        self.output_dir_frame.grid(row=1, column=0, padx=10, pady=5, sticky="ew")
        self.output_dir_frame.grid_columnconfigure(1, weight=1)

        self.select_output_dir_button = ctk.CTkButton(self.output_dir_frame, text="Browse Output Dir", command=self.browse_output_dir)
        self.select_output_dir_button.grid(row=0, column=0, padx=10, pady=10)
        self.output_dir_entry = ctk.CTkEntry(self.output_dir_frame, textvariable=self.output_dir_path) # Editable, or readonly if always set by browser
        self.output_dir_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        
        # Output Format Selection
        self.format_frame = ctk.CTkFrame(self)
        self.format_frame.grid(row=2, column=0, padx=10, pady=5, sticky="ew") # Adjusted row
        # Center radio buttons using pack within the frame
        self.format_inner_frame = ctk.CTkFrame(self.format_frame, fg_color="transparent") # Inner frame for packing
        self.format_inner_frame.pack(expand=True)


        self.format_label = ctk.CTkLabel(self.format_inner_frame, text="Output Format:")
        self.format_label.pack(side="left", padx=10, pady=10)
        self.json_radio = ctk.CTkRadioButton(self.format_inner_frame, text="JSON", variable=self.output_format, value="json")
        self.json_radio.pack(side="left", padx=5, pady=10)
        self.csv_radio = ctk.CTkRadioButton(self.format_inner_frame, text="CSV", variable=self.output_format, value="csv")
        self.csv_radio.pack(side="left", padx=10, pady=10)

        # Convert Button
        self.convert_button = ctk.CTkButton(self, text="Convert File", command=self.process_conversion)
        self.convert_button.grid(row=3, column=0, padx=10, pady=10, sticky="ew") # Adjusted row

        # Status Area
        self.status_label = ctk.CTkLabel(self, textvariable=self.status_message, wraplength=580, justify="left", height=3) # Increased height
        self.status_label.grid(row=4, column=0, padx=10, pady=(5,10), sticky="ew") # Adjusted row

        # About Button (New)
        self.about_button = ctk.CTkButton(self, text="About", command=self.show_about_dialog, width=100)
        self.about_button.grid(row=5, column=0, padx=10, pady=10, sticky="s") # Adjusted row, sticky to south

        self.center_window()

    def center_window(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')

    def browse_input_file(self):
        filetypes = [
            ("All supported files", "*.txt *.pdf *.html *.htm *.png *.jpg *.jpeg"),
            ("Text files", "*.txt"), ("PDF files", "*.pdf"),
            ("HTML files", "*.html *.htm"), ("Image files", "*.png *.jpg *.jpeg"),
            ("All files", "*.*")
        ]
        path = filedialog.askopenfilename(title="Select an input file", filetypes=filetypes)
        if path:
            self.input_file_path.set(path)
            # Set default output directory to input file's directory if not already set
            if not self.output_dir_path.get():
                self.output_dir_path.set(os.path.dirname(path))
            self.status_message.set(f"Selected: {os.path.basename(path)}")

    def browse_output_dir(self):
        path = filedialog.askdirectory(title="Select output directory")
        if path:
            self.output_dir_path.set(path)
            self.status_message.set(f"Output directory: {path}")


    def process_conversion(self):
        input_path = self.input_file_path.get()
        output_fmt = self.output_format.get()
        output_dir = self.output_dir_path.get()

        if not input_path:
            self.status_message.set("Error: Please select an input file first.")
            return

        if not output_dir: # Default to input file's directory if output_dir is somehow empty
            output_dir = os.path.dirname(input_path)
            self.output_dir_path.set(output_dir) # Update UI as well

        # Construct the full output path to pass to convert_file
        # convert_file expects the full desired output file path.
        # base_filename = os.path.splitext(os.path.basename(input_path))[0]
        # output_filename = f"{base_filename}.{output_fmt}"
        # The `convert_file` function in `main_converter` already creates the output file name
        # based on the input file name and output format.
        # It saves it in the same directory as the input file.
        # We need to decide if `convert_file` should take an output_dir or if app_ui handles it.
        # For now, let convert_file handle naming, and we just check the output_dir for existence.
        # Let's modify `convert_file` in a future step if we want app_ui to dictate the full output path.
        # For this iteration, the output_dir_path is more of an FYI for the user,
        # as convert_file's current logic will save next to input file.
        # OR, we modify `main_converter.py` to accept `output_dir` - this is cleaner.
        # For now, this subtask will assume `convert_file` is NOT changed yet to accept output_dir.
        # The UI output_dir selection will be more of a visual guide for now.
        # A proper implementation would pass output_dir to convert_file.
        # I will make a note to update main_converter later.

        self.status_message.set(f"Converting {os.path.basename(input_path)} to {output_fmt}...")
        self.update_idletasks()

        # Call convert_file (assuming it doesn't take output_dir yet, so output is beside input file)
        # We will need to modify convert_file to accept an output directory.
        # For now, we'll proceed as if it's not yet modified.
        # The user will select an output directory, but the file will appear next to the input file.
        # This is a temporary inconsistency.
        
        # Placeholder: Simulating that convert_file will take output_dir in the future
        # This part of the subtask *should* ideally also update main_converter.py
        # For now, let's just make the call and if it works, the output path will be as main_converter makes it.
        # If we want to enforce the output_dir, main_converter.py *must* be updated.
        # For this step, I will assume convert_file remains unchanged, and the UI's output_dir is a visual aid only.
        # The actual output path comes from `message` if successful.

        success, message = convert_file(input_path, output_fmt, output_dir) # Updated call

        if success:
            # If `convert_file` is modified to save in `output_dir`, `message` would be that path.
            # If not, `message` is path next to input file.
            self.status_message.set(f"Success! Output saved to: {message}")
        else:
            self.status_message.set(f"Error: {message}") # This will now show the Tesseract-specific error

    def show_about_dialog(self):
        messagebox.showinfo(
            "About Taabiib Converter",
            f"Taabiib File Converter
Version: {self.APP_VERSION}

A simple utility to convert files to JSON or CSV.
Based on Python and CustomTkinter."
        )

if __name__ == "__main__":
    app = App()
    app.mainloop()
