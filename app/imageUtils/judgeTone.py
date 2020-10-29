# -*- coding: utf-8 -*-
import colorsys
from PIL import Image, ImageStat
import collections
import numpy as np
import cv2
import requests as req
from io import BytesIO

def get_dominant_color(image):
    # image = Image.open(image)
    # 要提取的主要颜色数量
    num_colors = 5
    small_image = image.resize((80, 80))
    result = small_image.convert('P', palette=Image.ADAPTIVE, colors=num_colors)   # image with 5 dominating colors
    
    result = result.convert('RGBA')
    # main_colors = result.getcolors(80*80)
    max_score = 0 #原来的代码此处为None
    dominant_color = 0
    for count, (r, g, b, a) in result.getcolors(80*80):
        # 跳过纯黑色
        if a == 0:
            continue
        if(max_score < count):
            max_score = count
            dominant_color = (r, g, b)
            dominant_color_hsv = rgb2hsv(r, g, b)
    
    print(dominant_color)
    return dominant_color_hsv
    # print(dominant_color)
    # print(dominant_color_hsv)
 
# # 显示提取的主要颜色
# for count, col in main_colors:
#     if count < 40:
#         continue
#     a = np.zeros((224,224,3))
#     a = a + np.array(col)
#     # print(a)
#     cv2.imshow('a',a.astype(np.uint8)[:,:,::-1])
#     cv2.waitKey()

# 获取一张图片的主要颜色
def get_dominant_color_2(image):
    #颜色模式转换，以便输出rgb颜色值
    image = image.convert('RGBA')

    #生成缩略图，减少计算量，减小cpu压力
    image.thumbnail((200, 200))

    max_score = 0 #原来的代码此处为None
    dominant_color = 0  #原来的代码此处为None，但运行出错，改为0以后 运行成功，原因在于在下面的 score > max_score的比较中，max_score的初始格式不定
    
    for count, (r, g, b, a) in image.getcolors(image.size[0] * image.size[1]):
        # 跳过纯黑色
        if a == 0:
            continue
        
        saturation = colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)[1]
       
        y = min(abs(r * 2104 + g * 4130 + b * 802 + 4096 + 131072) >> 13, 235)
       
        y = (y - 16.0) / (235 - 16)
        
        # 忽略高亮色
        if y > 0.9:
            continue
        
        # Calculate the score, preferring highly saturated colors.
        # Add 0.1 to the saturation so we don't completely ignore grayscale
        # colors by multiplying the count by zero, but still give them a low
        # weight.
        score = (saturation + 0.1) * count
        
        if score > max_score:
            max_score = score
            dominant_color = (r, g, b)
            # print(dominant_color)
            # dominant_color_hsv = colorsys.rgb_to_hsv(int(r / 255.0), int(g / 255.0), int(b / 255.0))
            dominant_color_hsv = rgb2hsv(r, g, b)
    
    # dominant_color_hsv = colorsys.rgb_to_hsv(int(r / 255), int(g / 255), int(b / 255))
    # return dominant_color, dominant_color_hsv
    # print(dominant_color_hsv)
    return dominant_color_hsv

def rgb2hsv(r, g, b):
    r, g, b = r/255.0, g/255.0, b/255.0
    mx = max(r, g, b)
    mn = min(r, g, b)
    m = mx-mn
    if mx == mn:
        h = 0
    elif mx == r:
        if g >= b:
            h = ((g-b)/m)*60
        else:
            h = ((g-b)/m)*60 + 360
    elif mx == g:
        h = ((b-r)/m)*60 + 120
    elif mx == b:
        h = ((r-g)/m)*60 + 240
    if mx == 0:
        s = 0
    else:
        s = m/mx
    v = mx
    H = int(h / 2)
    S = int(s * 255.0)
    V = int(v * 255.0)
    return [H, S, V]
    
#定义字典存放颜色分量上下限
#例如：{颜色: [min分量, max分量]}
#{'red': [array([160,  43,  46]), array([179, 255, 255])]}
 
def getColorList():
    dict = collections.defaultdict(list)
 
    # # 黑色
    # lower_black = np.array([0, 0, 0])
    # upper_black = np.array([180, 255, 46])
    # color_list = []
    # color_list.append(lower_black)
    # color_list.append(upper_black)
    # dict['black'] = color_list
 
    # # #灰色
    # lower_gray = np.array([0, 0, 46])
    # upper_gray = np.array([180, 43, 220])
    # color_list = []
    # color_list.append(lower_gray)
    # color_list.append(upper_gray)
    # dict['gray']=color_list
 
    # # 白色
    # lower_white = np.array([0, 0, 221])
    # upper_white = np.array([180, 30, 255])
    # color_list = []
    # color_list.append(lower_white)
    # color_list.append(upper_white)
    # dict['white'] = color_list
 
    #红色
    lower_red = np.array([156, 43, 46])
    upper_red = np.array([180, 255, 255])
    color_list = []
    color_list.append(lower_red)
    color_list.append(upper_red)
    dict['red']=color_list
 
    # 红色2
    # lower_red = np.array([0, 43, 46])
    # upper_red = np.array([10, 255, 255])
    # color_list = []
    # color_list.append(lower_red)
    # color_list.append(upper_red)
    # dict['red2'] = color_list
 
    #橙色 + 红2
    # lower_orange = np.array([11, 43, 46])
    # upper_orange = np.array([25, 255, 255])
    lower_orange = np.array([0, 43, 46])
    upper_orange = np.array([25, 255, 255])
    color_list = []
    color_list.append(lower_orange)
    color_list.append(upper_orange)
    dict['orange'] = color_list
 
    #黄色
    lower_yellow = np.array([26, 43, 46])
    upper_yellow = np.array([34, 255, 255])
    color_list = []
    color_list.append(lower_yellow)
    color_list.append(upper_yellow)
    dict['yellow'] = color_list
 
    #绿色
    lower_green = np.array([35, 43, 46])
    upper_green = np.array([77, 255, 255])
    color_list = []
    color_list.append(lower_green)
    color_list.append(upper_green)
    dict['green'] = color_list
 
    #青色
    lower_cyan = np.array([78, 43, 46])
    upper_cyan = np.array([99, 255, 255])
    color_list = []
    color_list.append(lower_cyan)
    color_list.append(upper_cyan)
    dict['cyan'] = color_list
 
    #蓝色
    lower_blue = np.array([100, 43, 46])
    upper_blue = np.array([124, 255, 255])
    color_list = []
    color_list.append(lower_blue)
    color_list.append(upper_blue)
    dict['blue'] = color_list
 
    # 紫色
    lower_purple = np.array([125, 43, 46])
    upper_purple = np.array([155, 255, 255])
    color_list = []
    color_list.append(lower_purple)
    color_list.append(upper_purple)
    dict['purple'] = color_list
 
    return dict
 

# 获取图像的亮度值
def get_image_light_mean(path):
    response = req.get(path)
    im = Image.open(BytesIO(response.content)).convert('L')
    stat = ImageStat.Stat(im)
    return stat.mean[0]

# 传入的是图片的路径数组 返回记录了图片的主要颜色hsv 和 其色调区域 的字典
def preprocess_image(images):
    if isinstance(images,list):
        mainColor_dict = {} # 用于存储主要颜色的字典
        for i in range(len(images)):
            mainColor_dict[i] = {}
            mainColor_dict[i]['hsv'] = get_dominant_color(images[i])
            mainColor_dict[i]['hue'] = from_hsv_to_range(mainColor_dict[i]['hsv'])
        print(mainColor_dict)
        return mainColor_dict
    else:
        print('传入参数不是列表')

# 返回色相的序号
def from_hsv_to_range(hsv):
    color_dict = getColorList()
    hueRange = ''
    for d in color_dict:
        if color_dict[d][0][0] <= hsv[0] and color_dict[d][1][0] >= hsv[0]:
            hueRange = d
            break
        else:
            continue
    return hueRange

#调整图像的色彩平衡
def balanceColors(image, args):
    """
    1、r： 增加数值 偏红； 减少数值 偏 青色
    2、g： 增加数值 偏绿色； 减少数值 偏洋红色
    3、b： 增加数值 偏蓝色； 减少数值 偏黄色
    """
     # 读入图片，转化为 RGB 色值
    # image = Image.open(images).convert('RGBA')
    image.load()
    r, g, b, a = image.split()
    result_r, result_g, result_b, result_a = [], [], [], []
    # 依次对每个像素点进行处理
    for pixel_r, pixel_g, pixel_b, pixel_a in zip(r.getdata(), g.getdata(), b.getdata(), a.getdata()):
        pixel_r = pixel_r + args[0]
        pixel_g = pixel_g + args[1]
        pixel_b = pixel_b + args[2]

        result_r.append(pixel_r)
        result_g.append(pixel_g)
        result_b.append(pixel_b)
        result_a.append(pixel_a)

    r.putdata(result_r)
    g.putdata(result_g)
    b.putdata(result_b)
    a.putdata(result_a)

    # 合并图片
    image = Image.merge('RGBA', (r, g, b, a))
    return image
