import hashlib
import struct

# File paths
input_png = "MRI_brain.png"
output_png = "MRI_brain_stego.png"
hidden_message = "Secret Steganography Data"

def calculate_md5(file_path):
    """Calculates the MD5 checksum of a file."""
    with open(file_path, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()

def insert_or_modify_text_chunk(input_file, output_file, message):
    """Finds or inserts a tEXt chunk in a PNG file to store hidden data."""
    with open(input_file, "rb") as f:
        png_data = bytearray(f.read())

    # PNG magic header validation
    if png_data[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("Not a valid PNG file.")

    # Look for 'tEXt' chunk
    offset = png_data.find(b'tEXt')

    if offset == -1:
        print("No tEXt chunk found. Adding one manually.")

        # Define a new tEXt chunk
        keyword = b"Comment\x00"  # PNG text chunk requires a keyword before the data
        message_bytes = message.encode('utf-8')
        new_text_chunk = keyword + message_bytes

        # PNG chunks follow: [length (4 bytes)] + [type (4 bytes)] + [data (var)] + [CRC (4 bytes)]
        chunk_length = struct.pack(">I", len(new_text_chunk))  # Big-endian length
        chunk_type = b"tEXt"
        chunk_crc = struct.pack(">I", 0)  # Placeholder CRC (optional)

        # Insert after IHDR chunk
        ihdr_offset = png_data.find(b'IHDR')
        if ihdr_offset == -1:
            raise ValueError("Invalid PNG structure, no IHDR chunk.")

        ihdr_end = ihdr_offset + 25  # IHDR length (fixed size)
        png_data = png_data[:ihdr_end] + chunk_length + chunk_type + new_text_chunk + chunk_crc + png_data[ihdr_end:]

        print("tEXt chunk added successfully.")

    else:
        print(f"Found existing tEXt chunk at offset {offset}, modifying it.")
        end_offset = png_data.find(b'\x00', offset)
        if end_offset == -1:
            raise ValueError("Invalid PNG tEXt chunk.")

        # Replace message within allocated space
        chunk_length = end_offset - offset
        message_bytes = message.encode('utf-8').ljust(chunk_length, b' ')

        png_data[offset:end_offset] = message_bytes

    # Save modified PNG
    with open(output_file, "wb") as f:
        f.write(png_data)

    print("Hidden message stored successfully.")

# --- Run the script ---
original_md5 = calculate_md5(input_png)
print(f"Original MD5: {original_md5}")

insert_or_modify_text_chunk(input_png, output_png, hidden_message)

new_md5 = calculate_md5(output_png)
print(f"New MD5: {new_md5}")

# Check if MD5 remains unchanged
if original_md5 == new_md5:
    print("Success. MD5 remains unchanged after metadata modification.")
else:
    print("MD5 changed. Modification affected file integrity.")
