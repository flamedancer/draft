import numpy as np
import cv2

img = cv2.imread('captcha2.png')

width, heigh = img.shape[:2]
print width, heigh 

DETER = 40
BEAR = 0 

now_bear = 0
new_img_bit = []

def is_similar_color(base_color, color):
    global now_bear
    sum_deter = 0
    for index, c in enumerate(color):
        sum_deter += abs(int(c) - int(base_color[index]))
    if sum_deter > DETER: 
        if now_bear >= BEAR:
            now_bear = 0
            return False
        else:
            now_bear += 1
            return True
    else:
        now_bear = 0
    return True


def genrate_color(w, h, first_by):
    base_color_locate = [0, 0]
    if w == h == 0: 
        return img[0, 0]
    if first_by == 'w':
        if h == 0:
            base_color_locate = [w - 1, h]
        else:
            base_color_locate = [w, h - 1]
    else:
        if w == 0:
            base_color_locate = [w, h - 1]
        else:
            base_color_locate = [w - 1, h]
    base_color = img[base_color_locate[0], base_color_locate[1]] 
    now_color = img[w, h]
    if is_similar_color(base_color, now_color): 
        return new_img_bit[base_color_locate[1]][base_color_locate[0]] 
    else:
        return list(now_color)
        
def clear(first_by='w'):
    global new_img_bit
    new_img_bit = []
    now_bear = 0

    for h in range(heigh):
        row = []
        new_img_bit.append(row)
        for w in range(width):
            row.append(genrate_color(w, h, first_by))
    
    
    for h in range(heigh):
        for w in range(width):
            img[w, h] = new_img_bit[h][w]

if __name__ == '__main__':
    # clear(first_by='h') 
    clear(first_by='w') 
    cv2.imshow('image',img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
