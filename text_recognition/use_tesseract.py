from PIL import Image
import pytesseract


file_name = 'text_example.jpg'

print(pytesseract.image_to_string(Image.open(file_name)))
