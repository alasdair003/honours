import struct
import hashlib

# File paths
input_png = "MRI_brain.png"
output_png = "MRI_brain_stego.png"
hidden_data = b"Steganography Data Hidden Here"

def calculate_md5(file_path):
    """Calculates the MD5 checksum of a file."""
    with open(file_path, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()

def inject_png_chunk(input_file, output_file, custom_data):
    """Injects a custom ancillary chunk (oFFs) into a PNG file."""
    with open(input_file, "rb") as f:
        png_data = bytearray(f.read())

    # PNG signature validation
    if png_data[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("Not a valid PNG file.")

    # Find position before IEND chunk (end of PNG data)
    iend_offset = png_data.find(b'IEND')
    if iend_offset == -1:
        raise ValueError("Invalid PNG file. No IEND chunk found.")

    # Define our custom chunk (oFFs is ignored by most PNG readers)
    chunk_type = b'oFFs'  # Example: Offset chunk
    chunk_data = custom_data.ljust(8, b' ')  # Ensure fixed length
    chunk_length = struct.pack(">I", len(chunk_data))
    chunk_crc = struct.pack(">I", 0)  # Placeholder CRC

    # Construct PNG chunk
    new_chunk = chunk_length + chunk_type + chunk_data + chunk_crc

    # Insert chunk before IEND
    png_data = png_data[:iend_offset] + new_chunk + png_data[iend_offset:]

    # Save modified PNG
    with open(output_file, "wb") as f:
        f.write(png_data)

    print("Custom chunk injected successfully.")

# --- Run the script ---
original_md5 = calculate_md5(input_png)
print(f"Original MD5: {original_md5}")

inject_png_chunk(input_png, output_png, hidden_data)

new_md5 = calculate_md5(output_png)
print(f"New MD5: {new_md5}")

# Check if MD5 remains unchanged
if original_md5 == new_md5:
    print("Success. MD5 remains unchanged after chunk injection.")
else:
    print("MD5 changed. Further balancing needed.")
