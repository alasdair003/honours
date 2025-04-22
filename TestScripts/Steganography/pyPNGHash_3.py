import hashlib

# File paths
input_png = "MRI_brain.png"
output_png = "MRI_brain_stego.png"
hidden_message = "PNG Metadata Hidden Data"

def calculate_md5(file_path):
    """Calculates the MD5 checksum of a file."""
    with open(file_path, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()

def modify_unused_header_space(input_file, output_file, message):
    """Modifies unused bytes in the PNG header without affecting the file size."""
    with open(input_file, "rb") as f:
        png_data = bytearray(f.read())

    # PNG magic header validation
    if png_data[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("Not a valid PNG file.")

    # Locate IHDR chunk
    ihdr_offset = png_data.find(b'IHDR')
    if ihdr_offset == -1:
        raise ValueError("Invalid PNG file, IHDR chunk missing.")

    # Unused padding space after IHDR chunk (typically between bytes 33-40)
    header_padding_start = ihdr_offset + 33
    header_padding_end = header_padding_start + 8  # Use 8 bytes max

    if header_padding_end > len(png_data):
        raise ValueError("Not enough space in the header for data storage.")

    # Encode the message to fit within this space
    message_bytes = message.encode('utf-8').ljust(header_padding_end - header_padding_start, b' ')[:header_padding_end - header_padding_start]

    # Overwrite unused space with hidden message
    png_data[header_padding_start:header_padding_end] = message_bytes

    # Save modified PNG
    with open(output_file, "wb") as f:
        f.write(png_data)

    print("Hidden message stored in unused header space.")

# --- Run the script ---
original_md5 = calculate_md5(input_png)
print(f"Original MD5: {original_md5}")

modify_unused_header_space(input_png, output_png, hidden_message)

new_md5 = calculate_md5(output_png)
print(f"New MD5: {new_md5}")

# Check if MD5 remains unchanged
if original_md5 == new_md5:
    print("Success. MD5 remains unchanged after modification.")
else:
    print("MD5 changed. Modification affected file integrity.")
