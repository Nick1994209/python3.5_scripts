from pyimagesearch.transform import four_point_transform
import numpy as np
import cv2

args = {'image': 'images/example_03.png', 'coords': '[(63, 242), (291, 110), (361, 252), (78, 386)]'}
args = {'image': 'images/example_03.png', 'coords': '[(361, 252), (63, 242), (291, 110), (78, 386)]'}
image = cv2.imread(args["image"])
pts = np.array(eval(args["coords"]), dtype="float32")

# apply the four point tranform to obtain a "birds eye view" of
# the image
warped = four_point_transform(image, pts)

# show the original and warped images
cv2.imshow("Original", image)
cv2.imshow("Warped", warped)
cv2.waitKey(0)
