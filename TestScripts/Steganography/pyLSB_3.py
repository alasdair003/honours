import numpy as np
from PIL import Image
import time

def encode_image(image_path, message, output_path):
    """Hides a message in the least significant bits of an image."""
    with Image.open(image_path) as img:
        encoded = img.convert("RGB")  # Ensure it's in RGB mode
    
    message += "###END###"  # Delimiter to mark the end of the message
    binary_message = ''.join(format(ord(char), '08b') for char in message)

    pixels = np.array(encoded)
    height, width, _ = pixels.shape
    index = 0  # Track position in the binary message

    for row in range(height):
        for col in range(width):
            for color in range(3):  # Modify R, G, B values
                if index < len(binary_message):
                    pixels[row, col, color] = (pixels[row, col, color] & 0xFE) | int(binary_message[index])  # Modify LSB
                    index += 1
                else:
                    break

    if index < len(binary_message):
        print("Warning: Not enough space to encode the full message!")

    # Convert back to an image and save
    encoded_image = Image.fromarray(pixels)
    encoded_image.save(output_path, optimize=True, compress_level=9)
    print(f"Message successfully encoded in {output_path}")

def decode_image(image_path, max_chars=5000):
    """Extracts the hidden message from an image safely using NumPy."""
    with Image.open(image_path) as img:
        pixels = np.array(img)

    binary_message = ""

    print("Decoding started... Extracting binary data...")

    # Extract LSBs from all pixels at once (vectorized)
    lsb_array = pixels & 1
    binary_message = ''.join(str(bit) for bit in lsb_array.flatten())

    print(f"Extracted {len(binary_message)} bits of binary data.")

    # Convert binary to text
    message = ""
    for i in range(0, len(binary_message), 8):
        try:
            char = chr(int(binary_message[i:i+8], 2))
        except ValueError:
            print("Error: Invalid binary data detected, stopping decoding.")
            break

        message += char
        print(f"Decoded char: {char}")

        if message.endswith("###END###"):
            message = message.replace("###END###", "")
            print("End marker found, stopping extraction.")
            return message

    print("Warning: No valid end marker found, stopping decoding early.")
    return "[No message found]"

def check_encoded_data(image_path, num_pixels=10):
    """Checks the first few pixels to verify if the message is encoded."""
    with Image.open(image_path) as img:
        pixels = np.array(img)

    print("First few pixels (R, G, B values):")
    for i in range(min(num_pixels, pixels.shape[0] * pixels.shape[1])):
        row = i // pixels.shape[1]
        col = i % pixels.shape[1]
        print(f"Pixel {i} at ({row},{col}): {tuple(pixels[row, col])}")

# Run the encoding function
input_image = "MRI_brain.png"  # Ensure this is already a small enough image
encoded_image = "MRI_brain_encoded.png"
secret_message = "Hidden message in LSB"

encode_image(input_image, secret_message, encoded_image)

# Check if encoding was successful
check_encoded_data(encoded_image)

# Time decoding process
start_time = time.time()
decoded_message = decode_image(encoded_image)
end_time = time.time()

print(f"Decoded message: {decoded_message}")
print(f"Decoding took {end_time - start_time:.4f} seconds")
