from PIL import Image, ImageDraw, ImageFont

try:
    # Create a blank image
    img_width = 300
    img_height = 100
    img = Image.new('RGB', (img_width, img_height), color = (255, 255, 255)) # White background
    
    d = ImageDraw.Draw(img)
    
    # Try to use a common font, handle if not found
    text_to_draw = "Test OCR"
    try:
        # Attempt to load a truetype font. Common paths for Linux.
        # This might fail if no default font is found or if fontconfig is not set up.
        font = ImageFont.truetype("DejaVuSans.ttf", 40)
    except IOError:
        # If specific font not found, use a default bitmap font
        print("WARN: Default font not found. Using basic PIL font.")
        font = ImageFont.load_default()

    # Calculate text size and position
    # For Pillow versions before 10.0.0, use textsize
    if hasattr(d, "textbbox"): # Pillow 10.0.0+
        bbox = d.textbbox((0,0), text_to_draw, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
    else: # Older Pillow
        text_width, text_height = d.textsize(text_to_draw, font=font)

    x = (img_width - text_width) / 2
    y = (img_height - text_height) / 2
    
    d.text((x, y), text_to_draw, fill=(0,0,0), font=font) # Black text
    
    img.save("sample_files/dummy.png")
    print("SUCCESS: sample_files/dummy.png created.")

except ImportError:
    print("ERROR: Pillow (PIL) is not installed. Cannot create dummy PNG.")
except Exception as e:
    print(f"ERROR: Failed to create dummy PNG: {e}")
