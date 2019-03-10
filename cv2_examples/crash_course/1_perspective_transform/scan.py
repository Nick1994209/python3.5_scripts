import logging

import cv2
import imutils
from skimage.filters import threshold_local

from pyimagesearch.transform import four_point_transform

log = logging.getLogger('scanner')


class Scanner:
    def __init__(self, img_path, default_size=500):
        self.orig = cv2.imread(img_path)

        self.ratio = self.orig.shape[0] / float(default_size)
        self.image = imutils.resize(self.orig, height=default_size)

    def save_scan(self, path):
        cv2.imwrite(path, self.get_scan())

    def get_scan(self):

        scan_coordinates = self.get_scan_cords()

        # apply the four point transform to obtain a top-down
        # view of the original image
        scanner = four_point_transform(self.orig, scan_coordinates.reshape(4, 2) * self.ratio)

        # convert the warped image to grayscale, then threshold it
        # to give it that 'black and white' paper effect
        scanner = cv2.cvtColor(scanner, cv2.COLOR_BGR2GRAY)
        T = threshold_local(scanner, 11, offset=10, method="gaussian")
        return (scanner > T).astype("uint8") * 255

    def get_scan_cords(self):
        log.info('get scan coords')

        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
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


if __name__ == '__main__':
    project_path = '/Users/nvkorolkov/projects/python3.5_scripts/cv2_examples/crash_course/1_perspective_transform/'
    img_path = project_path + 'images/page.jpg'

    img_path = project_path + 'images/my.jpg'
    scan = Scanner(img_path)

    # cv2.imshow("Scanned", imutils.resize(scan.get_scan(), height=650))
    cv2.drawContours(scan.orig, scan.get_scan_cords(), -1, (0, 0, 255), 2)
    cv2.imshow("Original", imutils.resize(scan.orig, height=650))
    cv2.imshow("Scanned", scan.get_scan())
    cv2.waitKey(0)


    img_path = project_path + 'images/my.jpg'
    img_to_path = project_path + 'images/my_transormed.jpg'
    scan = Scanner(img_path)
    scan.save_scan(img_to_path)