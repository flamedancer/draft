import numpy as np
import cv2

img = cv2.imread('test1.png')          # queryImage

img2 = img.copy()
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
template = cv2.imread('test11.png',0)
template = template[0:35,0:35]
w, h = template.shape[::-1]
# All the 6 methods for comparison in a list
methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
            'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']
for meth in methods:
    method = eval(meth)
    # Apply template Matching
    res = cv2.matchTemplate(img_gray,template,method)
    threshold = 0.8
    loc = np.where( res >= threshold)
    for pt in zip(*loc[::-1]):
        cv2.rectangle(img, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
    

    cv2.imshow('image',img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
