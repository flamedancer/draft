import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread('test11.png',0)
edges = img
# edges = cv2.Canny(img,100,200)
kernel = np.ones((3,3),np.uint8)
res = cv2.morphologyEx(edges, cv2.MORPH_OPEN, kernel)

# plt.subplot(121),plt.imshow(img,cmap = 'gray')
# plt.title('Original Image'), plt.xticks([]), plt.yticks([])
# plt.subplot(122),plt.imshow(edges, res)
# plt.title('Edge Image'), plt.xticks([]), plt.yticks([])
# 
# plt.show()

cv2.imshow('image', res)
cv2.waitKey(0)
cv2.destroyAllWindows()
# cv2.imwrite('tcolse1.png', res)



