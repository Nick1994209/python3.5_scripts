import cv2
import imutils

project_path = '/Users/nvkorolkov/projects/python3.5_scripts/cv2_examples/crash_course/1_perspective_transform/'
# image = cv2.imread(project_path + 'images/page.jpg')
image = cv2.imread(project_path + 'images/receipt.jpg')

# load the image and compute the ratio of the old height
# to the new height, clone it, and resize it
image = imutils.resize(image, height=500)

# convert the image to grayscale, blur it, and find edges
# in the image
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# perform Gaussian blurring to remove high frequency noise
gaus_gray = cv2.GaussianBlur(gray, (5, 5), 0)
edged = cv2.Canny(gaus_gray, 75, 200)

# show the original image and the edge detected image
cv2.imshow("Image", image)
cv2.imshow("gray", gray)
cv2.imshow("gaussian blur", gaus_gray)
cv2.imshow("Edged", edged)
cv2.waitKey(0)
cv2.destroyAllWindows()
