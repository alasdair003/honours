import numpy as np
from PIL import Image
import time

# Test image dimensions
IMAGE_WIDTH = 209
IMAGE_HEIGHT = 256
TOTAL_PIXELS = IMAGE_WIDTH * IMAGE_HEIGHT
MAX_BITS = TOTAL_PIXELS * 3  # RGB

# Take fixed random seed so that testing is consistent
def generate_seeded_indices(seed, message_length):
    np.random.seed(seed)  # Take fixed seed
    return np.random.choice(TOTAL_PIXELS, message_length * 8, replace=False)  # 8 bits per char
    # replace=False means earch pixel only used once

def encode_image(image_path, message, output_path, seed=42):
    with Image.open(image_path) as img:
        encoded = img.convert("RGB")

    message += "###END###"  # Marks the end

    # Convert to binary
    binary_message = ''.join(format(ord(char), '08b') for char in message)

    # Ensure message fits within the hardcoded limits, keeps crashing if not
    if len(binary_message) > MAX_BITS:
        raise ValueError(f"Message is too large. Max bits: {MAX_BITS}, Needed: {len(binary_message)}")

    # Convert image to a numpy array
    pixels = np.array(encoded)

    # Get random pixel locations
    indices = generate_seeded_indices(seed, len(binary_message))

    # Encode message in the pixels at those locations
    for i, bit in enumerate(binary_message):
        row, col = divmod(indices[i], IMAGE_WIDTH)
        channel = i % 3  # Cycle through RGB
        pixels[row, col, channel] = (pixels[row, col, channel] & 0xFE) | int(bit)  # Edit LSB

    # Save edited image
    encoded_image = Image.fromarray(pixels)
    encoded_image.save(output_path, optimize=True, compress_level=9)
    print(f"Message successfully encoded in {output_path}")

def decode_image(image_path, seed=42, max_chars=5000):
    with Image.open(image_path) as img:
        pixels = np.array(img)

    max_bits = min(max_chars * 8, MAX_BITS)  # Crashes if extracting more than available

    indices = generate_seeded_indices(seed, max_bits // 8)
    binary_message = ""

    print("Decoding started.")

    for i in range(len(indices)):
        row, col = divmod(indices[i], IMAGE_WIDTH)
        channel = i % 3  # Go through RGB again
        binary_message += str(pixels[row, col, channel] & 1)

    # Convert binary to text
    message = ""
    for i in range(0, len(binary_message), 8):
        try:
            char = chr(int(binary_message[i:i+8], 2))
        except ValueError:
            print("Invalid binary data detected, stopping decoding.")
            break

        message += char
        print(f"Decoded char: {char}")

        if message.endswith("###END###"):
            message = message.replace("###END###", "")
            print("End marker found, stopping extraction.")
            return message

    print("No valid end marker found, stopping decoding.")
    return "[No message found]"

def check_encoded_data(image_path, num_pixels=10):
    with Image.open(image_path) as img:
        pixels = np.array(img)

    np.random.seed(42)  # Ensure consistency
    sample_indices = np.random.choice(TOTAL_PIXELS, num_pixels, replace=False)

    print("First few encoded pixels (R, G, B values):")
    for i, index in enumerate(sample_indices):
        row, col = divmod(index, IMAGE_WIDTH)
        print(f"Pixel {i} at ({row},{col}): {tuple(pixels[row, col])}")

input_image = "MRI_brain.png"  # DOUBLE CHECK THE RESOLUTION
encoded_image = "MRI_brain_encoded.png"
secret_message = "Secret information"

try:
    encode_image(input_image, secret_message, encoded_image)
    check_encoded_data(encoded_image)

    start_time = time.time()
    decoded_message = decode_image(encoded_image)
    end_time = time.time()

    print(f"Decoded message: {decoded_message}")
    print(f"Decoding took {end_time - start_time:.4f} seconds")

except ValueError as e:
    print(f"Encoding Error: {e}")