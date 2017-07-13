import cv2
from matplotlib import pyplot as plt

img_path = 'bird_with_python.jpg'
img = cv2.imread(img_path, 0)
plt.imshow(img, cmap='gray', interpolation='bicubic')
plt.xticks([]), plt.yticks([])  # to hide tick values on X and Y axis

plt.savefig('gray.png')
