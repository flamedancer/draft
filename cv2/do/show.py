import numpy as np
import cv2

img = cv2.imread('captcha_big2.png', 0)
img = cv2.imread('test11.png', 0)
img = img[:25, 35:55]

cv2.imshow('image',img)
cv2.waitKey(0)
cv2.destroyAllWindows()
