import cv2
import numpy as np

# img = cv2.imread('test.jpg', 0)
img = cv2.imread('test.jpg')
kernel = np.ones((5,5),np.uint8)
# erosion = cv2.dilate(img,kernel,iterations = 1)
# erosion = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
erosion = cv2.morphologyEx(img, cv2.MORPH_GRADIENT, kernel)


cv2.imshow('image',erosion)
cv2.waitKey(0)
cv2.destroyAllWindows()
