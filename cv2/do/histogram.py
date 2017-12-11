import cv2
import numpy as np
from matplotlib import pyplot as plt

# img = cv2.imread('captcha2.png',0)
# plt.hist(img.ravel(),256,[0,256]); plt.show()

# plt.subplot(121),plt.imshow(img,cmap = 'gray')
# plt.title('Original Image'), plt.xticks([]), plt.yticks([])
# plt.subplot(122),plt.imshow(edges,cmap = 'gray')
# plt.title('Edge Image'), plt.xticks([]), plt.yticks([])
# 
# plt.show()

img = cv2.imread('captcha2.png')

color = ('b','g','r')
for i,col in enumerate(color):
    histr = cv2.calcHist([img],[i],None,[256],[0,256])
    plt.plot(histr,color = col)
    plt.xlim([0,256])
plt.show()
