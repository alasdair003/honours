from PIL import Image
import numpy as np

def encode_image(image_path, message, output_path):
    """Hides a message in the least significant bits of an image."""
    with Image.open(image_path) as img:
        encoded = img.copy()

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

    if index < len(binary_message):
        print("Warning: Not enough space to encode the full message!")

    # Convert back to an image and save
    encoded_image = Image.fromarray(pixels)
    encoded_image.save(output_path, optimize=True, compress_level=9)
    print(f"Message successfully encoded in {output_path}")

def decode_image(image_path, max_chars=1000):
    """Extracts the hidden message from an image safely."""
    with Image.open(image_path) as img:
        pixels = np.array(img)

    binary_message = ""
    max_bits = max_chars * 8  # Maximum bits to extract
    count = 0

    print("Decoding started... Extracting binary data...")

    height, width, _ = pixels.shape

    for row in range(height):
        for col in range(width):
            for color in range(3):  # Read R, G, B values
                binary_message += str(pixels[row, col, color] & 1)
                count += 1
                if count >= max_bits:
                    break  

    print(f"Extracted {count} bits of binary data.")

    # Convert binary to text
    message = ""
    for i in range(0, len(binary_message), 8):
        char = chr(int(binary_message[i:i+8], 2))
        message += char
        print(f"Decoded char: {char}")

        if message.endswith("###END###"):
            message = message.replace("###END###", "")
            print("End marker found, stopping extraction.")
            break

    return message if message else "[No message found]"

def check_encoded_data(image_path, num_pixels=10):
    """Checks the first few pixels to verify if the message is encoded."""
    with Image.open(image_path) as img:
        pixels = np.array(img)

    print("First few pixels (R, G, B values):")
    for i in range(min(num_pixels, pixels.shape[0] * pixels.shape[1])):
        row = i // pixels.shape[1]
        col = i % pixels.shape[1]
        print(tuple(pixels[row, col]))

# Run the encoding function
input_image = "MRI_brain.png"
encoded_image = "MRI_brain_encoded.png"
secret_message = "Hidden message in LSB"

encode_image(input_image, secret_message, encoded_image)

# Check if encoding was successful
check_encoded_data(encoded_image)

# Decode the message
decoded_message = decode_image(encoded_image)
print(f"Decoded message: {decoded_message}")
