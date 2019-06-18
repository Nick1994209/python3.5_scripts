import cv2

img_path = 'text_example.jpg'
use_threshold = 1
use_blur = 1

image = cv2.imread(img_path)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


if use_threshold:
    image_threshold = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    cv2.imwrite('threshold.png', image_threshold)

if use_blur:
    image_blur = cv2.medianBlur(gray, 3)
    cv2.imwrite('blur.png', image_blur)
