import base64
import csv

# File paths
stego_csv = "stego_healthcare_data.csv"
extracted_image = "extracted_hidden_image.png"

def extract_image_from_csv(stego_file, output_image):
    """Extracts and reconstructs an image hidden in a CSV file."""
    with open(stego_file, "r", newline="", encoding="utf-8") as csvfile:
        csv_data = list(csv.reader(csvfile))

    # Find the last row (or column) containing hidden data
    for row in csv_data:
        if row and row[0] == "hidden_data":
            encoded_image = row[1]
            break
    else:
        raise ValueError("No hidden data found in CSV.")

    # Decode and save the image
    with open(output_image, "wb") as img_file:
        img_file.write(base64.b64decode(encoded_image))

    print(f"Hidden image extracted and saved as {output_image}")

# Run the function
extract_image_from_csv(stego_csv, extracted_image)
