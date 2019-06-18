import cv2
import imutils

project_path = '/Users/nvkorolkov/projects/python3.5_scripts/cv2_examples/crash_course/1_perspective_transform/'
image = cv2.imread(project_path + 'images/receipt.jpg')
image = imutils.resize(image, height=500)


def get_edges(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # perform Gaussian blurring to remove high frequency noise
    gaus_gray = cv2.GaussianBlur(gray, (5, 5), 0)
    return cv2.Canny(gaus_gray, 75, 200)


edged = get_edges(image)

# FIND COORDS

# find the contours in the edged image, keeping only the
# largest ones, and initialize the screen contour
contours = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
# We also handle the fact that OpenCV 2.4 and OpenCV 3 return contours differently
contours = contours[0] if imutils.is_cv2() else contours[1]

blue = (255, 0, 0)
cv2.drawContours(image, contours, -1, blue, 2)

count_big_counters = 7
big_contours = sorted(contours, key=cv2.contourArea, reverse=True)[:count_big_counters]
for c in big_contours:
    cv2.drawContours(image, c, -1, (0, 0, 255), 2)


# loop over the contours FOR GETTING bigger 4-th point polygon
for c in big_contours:
    # approximate the contour
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.02 * peri, True)

    # if our approximated contour has four points, then we
    # can assume that we have found our screen
    if len(approx) == 4:
        screenCnt = approx
        break

# show the contour (outline) of the piece of paper
green = (0, 255, 0)
cv2.drawContours(image, [screenCnt], -1, green, 1)
cv2.imshow("Outline", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
