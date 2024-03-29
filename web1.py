import sys, os
from PIL import Image
from PIL import Image, ImageDraw
from PIL import Image
import pytesseract

# 二值化变色
def test(path):
    img=Image.open(path)
    w,h=img.size
    for x in range(w):
        for y in range(h):
            r,g,b=img.getpixel((x,y))
            if 190<=r<=255 and 170<=g<=255 and 0<=b<=140:
                img.putpixel((x,y),(0,0,0))
            if 0<=r<=90 and 210<=g<=255 and 0<=b<=90:
                img.putpixel((x,y),(0,0,0))
    img=img.convert('L').point([0]*150+[1]*(256-150),'1')
    return img

#for i in range(1,14):
for i in range(1, 3):
    path = './jijia_check_node/Ex_test/' + str(i) + '.jpg'
    im = test(path)
#    path = path.replace('jpg','png').replace('./jijia_check_node/Ex_test/', 'Ex_img/')
    path = path.replace('jpg','png')
    im.save(path)

# 二值数组
t2val = {}

# 降噪
def twoValue(image, G):
    for y in range(0, image.size[1]):
        for x in range(0, image.size[0]):
            g = image.getpixel((x, y))
            if g > G:
                t2val[(x, y)] = 1
            else:
                t2val[(x, y)] = 0

# 根据一个点A的RGB值，与周围的8个点的RBG值比较，设定一个值N（0 <N <8），当A的RGB值与周围8个点的RGB相等数小于N时，此点为噪点
# G: Integer 图像二值化阀值
# N: Integer 降噪率 0 <N <8
# Z: Integer 降噪次数
# 输出
#  0：降噪成功
#  1：降噪失败
def clearNoise(image, N, Z):
    for i in range(0, Z):
        t2val[(0, 0)] = 1
        t2val[(image.size[0] - 1, image.size[1] - 1)] = 1

        for x in range(1, image.size[0] - 1):
            for y in range(1, image.size[1] - 1):
                nearDots = 0
                L = t2val[(x, y)]
                if L == t2val[(x - 1, y - 1)]:
                    nearDots += 1
                if L == t2val[(x - 1, y)]:
                    nearDots += 1
                if L == t2val[(x - 1, y + 1)]:
                    nearDots += 1
                if L == t2val[(x, y - 1)]:
                    nearDots += 1
                if L == t2val[(x, y + 1)]:
                    nearDots += 1
                if L == t2val[(x + 1, y - 1)]:
                    nearDots += 1
                if L == t2val[(x + 1, y)]:
                    nearDots += 1
                if L == t2val[(x + 1, y + 1)]:
                    nearDots += 1

                if nearDots < N:
                    t2val[(x, y)] = 1


def saveImage(filename, size):
    image = Image.new("1", size)
    draw = ImageDraw.Draw(image)

    for x in range(0, size[0]):
        for y in range(0, size[1]):
            draw.point((x, y), t2val[(x, y)])

    image.save(filename)
for i in range(1,12):
#    path =  './jijia_check_node/Ex_img/' + str(i) + ".png"
    path =  './jijia_check_node/Ex_test/' + str(i) + ".png"
    image = Image.open(path).convert("L")
    twoValue(image, 100)
    clearNoise(image, 3, 2)
#    path1 = './jijia_check_node/Ex_img/' + str(i) + ".jpeg"
    path1 = './jijia_check_node/Ex_test/' + str(i) + ".jpeg"
    saveImage(path1, image.size)
    
# 识别
def recognize_captcha(img_path):
    im = Image.open(img_path)
    # threshold = 140
    # table = []
    # for i in range(256):
    #     if i < threshold:
    #         table.append(0)
    #     else:
    #         table.append(1)
    #
    # out = im.point(table, '1')
    num = pytesseract.image_to_string(im)
    return num


if __name__ == '__main__':
    for i in range(1, 12):
#        img_path = './jijia_check_node/Ex_img/' + str(i) + ".jpeg"
        img_path = './jijia_check_node/Ex_test/' + str(i) + ".jpeg"
        res = recognize_captcha(img_path)
        strs = res.split("\n")
        if len(strs) >=1:
            print (strs[0])






























