import numpy as np
from PIL import Image

def embed_image(cover_path, hidden_path, output_path):
    # Use standard LSB again
    # Load images
    cover_img = Image.open(cover_path).convert("RGB")
    hidden_img = Image.open(hidden_path).convert("RGB")

    cover_array = np.array(cover_img)
    hidden_array = np.array(hidden_img)

    #CHECK HIDDEN IMAGE FITS INSIDE COVER IMAGE!!!
    if hidden_array.shape[0] > cover_array.shape[0] or hidden_array.shape[1] > cover_array.shape[1]:
        # Add error instead of crashing here
        raise ValueError("Hidden image dimensions must be smaller or equal to cover image.")

    # Resize hidden image to match the cover image if necessary
    if hidden_array.shape != cover_array.shape:
        hidden_img = hidden_img.resize((cover_array.shape[1], cover_array.shape[0]))
        hidden_array = np.array(hidden_img)
    #Maybne wrong?

    # Embed the hidden image using LSBs of cover image
    stego_array = cover_array.copy()
    stego_array[:, :, 0] = (cover_array[:, :, 0] & 0b11111100) | (hidden_array[:, :, 0] >> 6)
    stego_array[:, :, 1] = (cover_array[:, :, 1] & 0b11111100) | (hidden_array[:, :, 1] >> 6)
    stego_array[:, :, 2] = (cover_array[:, :, 2] & 0b11111100) | (hidden_array[:, :, 2] >> 6)

    # Save stego image
    stego_img = Image.fromarray(stego_array)
    stego_img.save(output_path, optimize=True)
    print(f"Hidden image embedded into {output_path}")

def extract_image(stego_path, output_path):
    """Extracts a hidden image from a stego image."""
    # Load stego image
    stego_img = Image.open(stego_path).convert("RGB")
    stego_array = np.array(stego_img)

    # Extract hidden image from LSBs
    extracted_array = np.zeros_like(stego_array)
    extracted_array[:, :, 0] = (stego_array[:, :, 0] & 0b00000011) << 6
    extracted_array[:, :, 1] = (stego_array[:, :, 1] & 0b00000011) << 6
    extracted_array[:, :, 2] = (stego_array[:, :, 2] & 0b00000011) << 6

    # Save extracted image
    extracted_img = Image.fromarray(extracted_array)
    extracted_img.save(output_path)
    print(f"Hidden image extracted and saved as {output_path}")

# File paths
cover_image = "MRI_brain.png"
hidden_image = "hidden_image.png"
stego_image = "MRI_brain_stego.png"
extracted_image = "extracted_hidden.png"

# Embed the hidden image
embed_image(cover_image, hidden_image, stego_image)

# Extract the hidden image
extract_image(stego_image, extracted_image)
