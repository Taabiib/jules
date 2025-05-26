from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

try:
    c = canvas.Canvas("sample_files/dummy.pdf", pagesize=letter)
    c.drawString(100, 750, "Dummy PDF content for testing.")
    c.save()
    print("SUCCESS: sample_files/dummy.pdf created.")
except ImportError:
    print("ERROR: reportlab is not installed. Cannot create dummy PDF.")
except Exception as e:
    print(f"ERROR: Failed to create dummy PDF: {e}")
