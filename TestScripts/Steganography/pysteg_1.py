from PIL import Image
import pysteg

# Load the image
image_path = "MRI_brain.jpg"
image = Image.open(image_path)

# Secret message
secret_message = "This is a hidden message."

# Encode the message into the image
encoded_image = pysteg.encode_text(image, secret_message)

# Save the encoded image
encoded_image_path = "MRI_brain_encoded.png"
encoded_image.save(encoded_image_path)
print(f"Encoded image saved as {encoded_image_path}")

# Load the encoded image and decode the message
encoded_image = Image.open(encoded_image_path)
decoded_message = pysteg.decode_text(encoded_image)

print(f"Decoded message: {decoded_message}")