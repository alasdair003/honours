import base64
import csv
import argparse
import os

# File paths
DEFAULT_CSV = "Fake_Healthcare_Data.csv"
STEGO_CSV = "stego_healthcare_data.csv"
HIDDEN_IMAGE = "hidden_image.png"
EXTRACTED_IMAGE = "extracted_hidden_image.png"

def hide_image_in_csv(cover_file, output_file, image_file):
    """Embeds an image inside a CSV file as a Base64 string."""
    if not os.path.exists(image_file):
        print(f"Error: Image file '{image_file}' not found.")
        return
    
    # Read the original CSV data
    with open(cover_file, "r", newline="", encoding="utf-8") as csvfile:
        csv_data = list(csv.reader(csvfile))

    # Read and encode the hidden image
    with open(image_file, "rb") as img_file:
        encoded_image = base64.b64encode(img_file.read()).decode("utf-8")

    # Insert the encoded image into the last row (or a new column)
    csv_data.append(["hidden_data", encoded_image])

    # Save the modified CSV
    with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(csv_data)

    print(f"Image successfully hidden inside '{output_file}'")

def extract_image_from_csv(stego_file, output_image):
    """Extracts and reconstructs an image hidden in a CSV file."""
    if not os.path.exists(stego_file):
        print(f"Error: Stego CSV file '{stego_file}' not found.")
        return
    
    with open(stego_file, "r", newline="", encoding="utf-8") as csvfile:
        csv_data = list(csv.reader(csvfile))

    # Find the row containing hidden data
    for row in csv_data:
        if row and row[0] == "hidden_data":
            encoded_image = row[1]
            break
    else:
        print("No hidden data found in CSV.")
        return

    # Decode and save the image
    with open(output_image, "wb") as img_file:
        img_file.write(base64.b64decode(encoded_image))

    print(f"Hidden image extracted and saved as '{output_image}'")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Hide or Extract an image in a CSV file")
    parser.add_argument("mode", choices=["hide", "extract"], help="Choose whether to hide or extract an image")
    
    args = parser.parse_args()

    if args.mode == "hide":
        hide_image_in_csv(DEFAULT_CSV, STEGO_CSV, HIDDEN_IMAGE)
    elif args.mode == "extract":
        extract_image_from_csv(STEGO_CSV, EXTRACTED_IMAGE)
