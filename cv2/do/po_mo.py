import numpy as np
# from matplotlib import pyplot as plt
import cv2
import collections
counter = collections.Counter()

# img = cv2.imread('captcha_big4.png')
img = cv2.imread('captcha_big6.jpg')

# img = cv2.imread('../test2.jpg')

width, heigh = img.shape[:2]

DETER = 50
BEAR = 0 

now_bear = 0
new_img_bit = []

def is_similar_color(base_color, color):
    global now_bear
    # sum_deter = 0
    # for index, c in enumerate(color):
    #     sum_deter += abs(int(c) - int(base_color[index]))
    # if sum_deter > DETER: 
    is_similar = True
    for index, c in enumerate(color):
        if base_color[index] - 30 < c < base_color[index] + 30: 
            continue
        else:
            is_similar = False
            
    if not is_similar: 
        if now_bear >= BEAR:
            now_bear = 0
            return False
        else:
            now_bear += 1
            return True
    else:
        now_bear = 0
    return True


def genrate_color(w, h):
    base_color_locates =[]
    if w == h == 0: 
        return tuple(img[0, 0])
    if h == 0:
        base_color_locates = [[w - 1, h]]
    elif w == 0:
        base_color_locates = [[w, h - 1]]
    else:
        base_color_locates = [[w, h - 1], [w - 1, h]]
    # else:
    #     if w == 0:
    #         base_color_locate = [w, h - 1]
    #     else:
    #         base_color_locate = [w - 1, h]
    now_color = img[w, h]
    now_color = tuple(now_color)
    for base_color_locate in base_color_locates:
        base_color = img[base_color_locate[0], base_color_locate[1]] 
        if is_similar_color(base_color, now_color): 
            return new_img_bit[base_color_locate[1]][base_color_locate[0]] 
    return now_color
        
def clear():
    global new_img_bit
    new_img_bit = []
    now_bear = 0

    for h in range(heigh):
        row = []
        new_img_bit.append(row)
        for w in range(width):
            color = genrate_color(w, h)
            counter[color] += 1
            row.append(color)
    
    

def deal_counter():
    #all_values = len(counter)
    #
    #large_frequent = int( all_values * 0.6)  
    #litte_frequent = int( all_values * 0.005)
    #print counter
    #litter = []
    #most = counter.most_common(1)[0][0]
    #
    #for item in counter.most_common():
    #    item = item[0]
    #    now_frequent = counter[item]
    #    if now_frequent < litte_frequent:
    #        litter.append(item)

    #
    #global new_img_bit
    #for h in range(heigh):
    #    for w in range(width):
    #        if sum(new_img_bit[h][w]) < 150 or sum(new_img_bit[h][w]) > 700:
    #            new_img_bit[h][w] = [0, 0, 0]
    #        else:
    #            new_img_bit[h][w] = most 
    #            # new_img_bit[h][w] = [255, 255, 255]
    #            
    #        # if new_img_bit[h][w] in litter:
    #        #     new_img_bit[h][w] = most 
    #        # else:
    #        #     new_img_bit[h][w] = [0, 0, 0]
    most = [item[0] for item in counter.most_common(2)]
    for h in range(heigh):
        for w in range(width):
            if new_img_bit[h][w] in most:
                new_img_bit[h][w] = [255, 255, 255]
                # new_img_bit[h][w] = [0, 0, 0]
            else:
                new_img_bit[h][w] = [0, 0, 0]
                # new_img_bit[h][w] = [255, 255, 255]

def draw():
    for h in range(heigh):
        for w in range(width):
            img[w, h] = new_img_bit[h][w]



if __name__ == '__main__':
    # clear(first_by='h')
    # clear(first_by='w')
    # deal_counter()
    # draw()
    # cv2.imshow('image',img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    # edges = cv2.Canny(img,100,200)
    #
    # plt.subplot(121),plt.imshow(img,cmap = 'gray')
    # plt.title('Original Image'), plt.xticks([]), plt.yticks([])
    # plt.subplot(122),plt.imshow(edges)
    # plt.title('Edge Image'), plt.xticks([]), plt.yticks([])
    #
    # plt.show()

    Z = img.reshape((-1,3))
    # convert to np.float32
    Z = np.float32(Z)
    # define criteria, number of clusters(K) and apply kmeans()
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    K = 3
    ret,label,center=cv2.kmeans(Z,K,None,criteria,10,cv2.KMEANS_RANDOM_CENTERS)
    # Now convert back into uint8, and make original image
    center = np.uint8(center)
    res = center[label.flatten()]
    res2 = res.reshape((img.shape))
    img = res2
    clear()
    # deal_counter()
    draw()
    # kernel = np.ones((5,5),np.uint8)
    # img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
    # img = cv2.erode(img,kernel,iterations = 1)
    # img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
    cv2.imshow('res2', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    cv2.imwrite('test11.png',img)
