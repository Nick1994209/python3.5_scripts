import cv2
import imutils
from skimage.filters import threshold_local

from pyimagesearch.transform import four_point_transform

project_path = '/Users/nvkorolkov/projects/python3.5_scripts/cv2_examples/crash_course/1_perspective_transform/'
image = cv2.imread(project_path + 'images/receipt.jpg')
ratio = image.shape[0] / 500.0
orig = image.copy()
image = imutils.resize(image, height=500)


def get_cords(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # perform Gaussian blurring to remove high frequency noise
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    # simple show objects on image
    edges = cv2.Canny(blur, 75, 200)

    contours = cv2.findContours(edges.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    # We also handle the fact that OpenCV 2.4 and OpenCV 3 return contours differently
    contours = contours[0] if imutils.is_cv2() else contours[1]
    count_big_counters = 5
    big_contours = sorted(contours, key=cv2.contourArea, reverse=True)[:count_big_counters]

    # loop over the contours FOR GETTING bigger 4-th point polygon
    for c in big_contours:
        # approximate the contour
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)

        # if our approximated contour has four points, then we
        # can assume that we have found our screen
        if len(approx) == 4:
            return approx

    raise Exception('Can not found coords')


screenCnt = get_cords(image)

# apply the four point transform to obtain a top-down
# view of the original image
warped = four_point_transform(orig, screenCnt.reshape(4, 2) * ratio)

# convert the warped image to grayscale, then threshold it
# to give it that 'black and white' paper effect
warped = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
T = threshold_local(warped, 11, offset=10, method="gaussian")
warped = (warped > T).astype("uint8") * 255

# show the original and scanned images
print("STEP 3: Apply perspective transform")
cv2.imshow("Original", imutils.resize(orig, height=650))
cv2.imshow("Scanned", imutils.resize(warped, height=650))
cv2.waitKey(0)
