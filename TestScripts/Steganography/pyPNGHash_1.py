import hashlib

# File paths
input_png = "MRI_brain.png"
output_png = "MRI_brain_stego.png"
hidden_message = "Secret information"

def calculate_md5(file_path):
    """Calculates the MD5 checksum of a file."""
    with open(file_path, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()

def modify_png_metadata(input_file, output_file, message):
    """Finds the tEXt metadata chunk and embeds a hidden message inside it."""
    with open(input_file, "rb") as f:
        png_data = bytearray(f.read())

    # PNG magic bytes (header must match PNG format)
    if png_data[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("Not a valid PNG file")

    # Look for 'tEXt' chunk
    offset = png_data.find(b'tEXt')
    if offset == -1:
        raise ValueError("No tEXt metadata chunk found in this PNG.")

    print(f"Found tEXt chunk at offset {offset}")

    # Find end of the text chunk (null-terminated)
    end_offset = png_data.find(b'\x00', offset)
    if end_offset == -1:
        raise ValueError("Invalid PNG tEXt chunk.")

    # Overwrite only the content within the allocated space
    message_bytes = message.encode('utf-8')
    chunk_length = end_offset - offset  # Keep original length

    if len(message_bytes) > chunk_length:
        raise ValueError("Message too long for existing tEXt chunk.")

    # Replace text data while keeping length unchanged
    png_data[offset:end_offset] = message_bytes.ljust(chunk_length, b' ')

    # Write modified PNG to new file
    with open(output_file, "wb") as f:
        f.write(png_data)

    print("Hidden message embedded in metadata.")

# --- Run the script ---
original_md5 = calculate_md5(input_png)
print(f"Original MD5: {original_md5}")

modify_png_metadata(input_png, output_png, hidden_message)

new_md5 = calculate_md5(output_png)
print(f"New MD5: {new_md5}")

# Check if MD5 remains unchanged
if original_md5 == new_md5:
    print("MD5 remains unchanged after metadata modification.")
else:
    print("Modification affected file integrity.")
