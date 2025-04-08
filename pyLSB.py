import numpy as np
from PIL import Image
import time

def encode_image(image_path, message, output_path):
    with Image.open(image_path) as img:
        encoded = img.convert("RGB")  # Ensure RGB mode
        metadata = img.info  # Preserve metadata (EXIF, ICC, etc.)

    message += "###END###"  # End marker so we know where to decode
    binary_message = ''.join(format(ord(char), '08b') for char in message)

    pixels = np.array(encoded)
    height, width, _ = pixels.shape
    index = 0  # Position tracker

    for row in range(height):
        for col in range(width):
            for color in range(3):  # Modify RGB
                if index < len(binary_message):
                    pixels[row, col, color] = (pixels[row, col, color] & 0xFE) | int(binary_message[index])
                    index += 1 # ADD BREAK LATER
                else:
                    break

    # Save image with metadata preserved
    Image.fromarray(pixels).save(output_path, optimize=True, compress_level=9, **metadata)

# Add max chars in so I know if it breaks
def decode_image(image_path, max_chars=5000):
    with Image.open(image_path) as img:
        pixels = np.array(img)

    # Extract LSBs from all pixels at once
    binary_message = ''.join(str(bit) for bit in (pixels & 1).flatten())

    # Convert binary to text
    message = ''.join(chr(int(binary_message[i:i+8], 2)) for i in range(0, len(binary_message), 8))

    # Stop at end marker
    return message.split("###END###")[0] if "###END###" in message else "[No message found]"

# Encode and decode process
input_image = "MRI_brain.png"
encoded_image = "MRI_brain_encoded.png"
secret_message = "Hidden message in LSB"

encode_image(input_image, secret_message, encoded_image)

# Measure decoding time
start_time = time.time()
decoded_message = decode_image(encoded_image)
end_time = time.time()

# Show times, probably future comparison in pypy vs. cpython?
print(f"Decoded message: {decoded_message}")
print(f"Decoding took {end_time - start_time:.4f} seconds")