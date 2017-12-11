import numpy as np
import cv2

img = cv2.imread('test.jpg', 0)
for i in range(10):
    reso = cv2.pyrDown(img)

for i in range(10):
    reso = cv2.pyrUp(img)
cv2.imshow('image',reso)
cv2.waitKey(0)
cv2.destroyAllWindows()
