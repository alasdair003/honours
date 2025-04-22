from PIL import Image

def encode_image(image_path, message, output_path):
    """Hides a message in the least significant bits of an image."""
    img = Image.open(image_path)
    encoded = img.copy() # Create a copy to modify
    
    message += "###END###"  # Delimiter to mark the end of the message
    binary_message = ''.join(format(ord(char), '08b') for char in message)
    
    # Convert message to binary
    pixels = list(encoded.getdata())
    new_pixels = [] # Store modified pixels here
    index = 0 #Fro current position

    # loopt hrough pixels
    for pixel in pixels:
        new_pixel = list(pixel)  # Convert tuple to list for modification
        for i in range(3):  # Modify R, G, B values
            if index < len(binary_message):
                new_pixel[i] = (new_pixel[i] & 0xFE) | int(binary_message[index])  # Modify LSB
                index += 1
        new_pixels.append(tuple(new_pixel))

    # Let user know if message is too big
    if index < len(binary_message):
        print("Warning: Not enough space to encode the full message!")

    # Save these to new image
    encoded.putdata(new_pixels)
    encoded.save(output_path)
    print(f"Message successfully encoded in {output_path}")

def decode_image(image_path, max_chars=100):
    """Extracts the hidden message from an image safely."""
    img = Image.open(image_path)
    pixels = list(img.getdata())
    binary_message = ""

    print("\nDecoding started... Extracting binary data...")

    count = 0  # Debug counter
    max_bits = max_chars * 8  # Maximum bits to extract

    for pixel in pixels:
        for i in range(3):  # Read R, G, B values
            binary_message += str(pixel[i] & 1)
            count += 1
            if count >= max_bits:  # Stop early if needed
                break  

    print(f"Extracted {count} bits of binary data.")

    # Convert binary to text
    message = ""
    for i in range(0, len(binary_message), 8):
        char = chr(int(binary_message[i:i+8], 2))
        message += char
        print(f"Decoded char: {char}")  # Debugging output

        if message.endswith("###END###"):
            message = message.replace("###END###", "")
            print("\n[End marker found, stopping extraction.]")
            break

    return message if message else "[No message found]"

def check_encoded_data(image_path, num_pixels=10):
    """Checks the first few pixels to verify if the message is encoded."""
    img = Image.open(image_path)
    pixels = list(img.getdata())

    print("\nFirst few pixels (R, G, B values):")
    for i in range(num_pixels):
        print(pixels[i])

# --- Run the Encoding Function ---
input_image = "MRI_brain.png"
encoded_image = "MRI_brain_encoded.png"
secret_message = "Hidden message in LSB"

encode_image(input_image, secret_message, encoded_image)

# --- Check If Encoding Was Successful ---
check_encoded_data(encoded_image)

# --- Decode the Message ---
decoded_message = decode_image(encoded_image)
print(f"\nDecoded message: {decoded_message}")
