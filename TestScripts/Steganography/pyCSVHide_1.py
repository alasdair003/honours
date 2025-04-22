import base64
import csv

# File paths
cover_csv = "Fake_Healthcare_Data.csv"
stego_csv = "stego_healthcare_data.csv"
hidden_image = "hidden_image.png"

def hide_image_in_csv(cover_file, output_file, image_file):
    """Embeds an image inside a CSV file as a Base64 string."""
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

    print(f"Image successfully hidden inside {output_file}")

# Run the function
hide_image_in_csv(cover_csv, stego_csv, hidden_image)
