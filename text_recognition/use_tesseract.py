import pytesseract
from PIL import Image

file_name = 'text_example.jpg'

print(pytesseract.image_to_string(Image.open(file_name)))
