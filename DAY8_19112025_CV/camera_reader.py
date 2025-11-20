import cv2
from PIL import Image
import pytesseract

# Path to Tesseract executable (adjust if installed elsewhere)
pytesseract.pytesseract.tesseract_cmd = r"C:/Program Files/Tesseract-OCR/tesseract.exe"

# Open webcam
camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)



while True:
    ret, frame = camera.read()
    if not ret:
        break

    # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Apply thresholding for better OCR
    _, thresholded = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # OCR
    text = pytesseract.image_to_string(Image.fromarray(thresholded), config='--psm 11').strip()
    if text:
        print("Detected Text:", text)

    # Show camera feed
    cv2.imshow(' OCR', frame)

    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
camera.release()
cv2.destroyAllWindows()