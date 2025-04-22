import base64
import argparse
import re

# Default file paths
TARGET_SCRIPT = "stego_script.py"
HIDDEN_PAYLOAD = "MRI_brain.png"
EXTRACTED_FILE = "extracted_hidden_data.png"

def hide_data_in_py(script_file, hidden_file):
    """Encodes an image file into Base64 and hides it inside a Python comment."""
    with open(hidden_file, "rb") as f:
        encoded_data = base64.b64encode(f.read()).decode("utf-8")

    # Generate a fake docstring section with Base64 payload
    payload_comment = f'"""HIDDEN_DATA\n{encoded_data}\nEND_HIDDEN_DATA"""\n'

    # Append the payload at the end of the script
    with open(script_file, "a") as script:
        script.write("\n" + payload_comment)

    print(f"Hidden data added to '{script_file}'")

def extract_data_from_py(script_file, output_file):
    """Extracts and reconstructs the hidden image from a Python file."""
    with open(script_file, "r") as script:
        script_content = script.read()

    # Find the hidden Base64 string
    match = re.search(r'"""HIDDEN_DATA\n(.*?)\nEND_HIDDEN_DATA"""', script_content, re.DOTALL)
    
    if match:
        encoded_data = match.group(1)
        with open(output_file, "wb") as f:
            f.write(base64.b64decode(encoded_data))
        print(f"Extracted hidden data and saved as '{output_file}'")
    else:
        print("❌ No hidden data found in the script.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Hide or Extract data from a Python file")
    parser.add_argument("mode", choices=["hide", "extract"], help="Choose whether to hide or extract data")
    
    args = parser.parse_args()

    if args.mode == "hide":
        hide_data_in_py(TARGET_SCRIPT, HIDDEN_PAYLOAD)
    elif args.mode == "extract":
        extract_data_from_py(TARGET_SCRIPT, EXTRACTED_FILE)
