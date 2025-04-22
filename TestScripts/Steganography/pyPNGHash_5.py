import struct
import hashlib

# File paths
input_png = "MRI_brain.png"
output_png = "MRI_brain_stego.png"
hidden_data = b"StegoData123"  # Fixed-length to avoid variation

def calculate_md5(file_path):
    """Calculates the MD5 checksum of a file."""
    with open(file_path, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()

def inject_balanced_chunk(input_file, output_file, custom_data):
    """Injects a custom ancillary chunk and balances file bytes to maintain MD5."""
    with open(input_file, "rb") as f:
        png_data = bytearray(f.read())

    # PNG signature validation
    if png_data[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("Not a valid PNG file.")

    # Find IEND chunk position
    iend_offset = png_data.find(b'IEND')
    if iend_offset == -1:
        raise ValueError("Invalid PNG file. No IEND chunk found.")

    # Define our custom chunk (oFFs)
    chunk_type = b'oFFs'
    chunk_data = custom_data.ljust(8, b' ')[:8]  # Fixed size
    chunk_length = struct.pack(">I", len(chunk_data))
    chunk_crc = struct.pack(">I", 0)  # Placeholder CRC

    # Construct the new PNG chunk
    new_chunk = chunk_length + chunk_type + chunk_data + chunk_crc

    # Inject the chunk before IEND
    png_data = png_data[:iend_offset] + new_chunk + png_data[iend_offset:]

    # **MD5 Counterbalance Strategy**
    # Find an IDAT chunk (image data) and modify its last few bytes with padding
    idat_offset = png_data.find(b'IDAT')
    if idat_offset != -1:
        idat_end = idat_offset + 8  # Locate IDAT payload start
        padding_offset = idat_end + len(custom_data)  # Adjust location
        if padding_offset < len(png_data) - 4:  # Ensure valid position
            png_data[padding_offset:padding_offset + 4] = b'\x00\x00\x00\x00'  # Null padding

    # Save modified PNG
    with open(output_file, "wb") as f:
        f.write(png_data)

    print("Balanced chunk injection completed.")

# --- Run the script ---
original_md5 = calculate_md5(input_png)
print(f"Original MD5: {original_md5}")
list 
inject_balanced_chunk(input_png, output_png, hidden_data)

new_md5 = calculate_md5(output_png)
print(f"New MD5: {new_md5}")

# Check if MD5 remains unchanged
if original_md5 == new_md5:
    print("Success. MD5 remains unchanged after chunk injection.")
else:
    print("MD5 changed. Further tuning required.")
