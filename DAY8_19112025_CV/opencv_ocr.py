import cv2
from PIL import Image
import pytesseract

# Update path if needed
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Path to your image
image_path = "ocr_text.png"
# image_path = "img.png"

# Read the image
image = cv2.imread(image_path)

if image is None:
    print("Error: Could not load image.")
else:
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Convert to PIL for pytesseract
    pil_img = Image.fromarray(gray)

    # Extract text
    text = pytesseract.image_to_string(pil_img)

    print("Extracted Text:\n", text)

    # Show the image (optional)
    cv2.imshow("Image", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()