import time
import math
import cv2
from PIL import Image, ImageStat
import numpy as np
import os
import colorsys
import requests as req
from io import BytesIO
import shutil

import app.imageUtils.judgeTone as judgeTone
import app.imageUtils.pilexchange as pilexchange

from app.utils.uploadOSS.uploadOSS import UploadOSS

class AdjustImageToneMain():
    # 配置色相列表
    color_lists = ['red', 'orange', 'yellow', 'green', 'cyan', 'blue', 'purple']
    time = time.time()

    @staticmethod
    def main(self, baseImg, changeImg):
        print('测试')
        base_response = req.get(baseImg)
        change_response = req.get(changeImg)
        baseImg_origin =  Image.open(BytesIO(base_response.content)).convert('RGBA') # 参照处理的图片的数据
        changeImg_origin =  Image.open(BytesIO(change_response.content)).convert('RGBA') # 等待处理的图片的数据
        print(baseImg_origin)
        print(changeImg_origin)
        # baseImg 处理降低饱和度、对比度
        generate = pilexchange.VisualEffect_pil(baseImg_origin, 0.9, 0.9, 1.0, 0.9) 

        initConfig = judgeTone.preprocess_image([baseImg_origin, changeImg_origin])

        len_0 = self.color_lists.index(initConfig[0]['hue']) #参照物的色相值
        len_1 = self.color_lists.index(initConfig[1]['hue']) # 更改物的色相值

        changeNum = 0
        while abs(len_0 - len_1) > 3 :
            if(len_0 > 2):
                changeImg_origin = judgeTone.balanceColors(changeImg_origin, [-1, 1, 1])
            else:
                changeImg_origin = judgeTone.balanceColors(changeImg_origin, [1, -1, -1])
           

            initConfig = judgeTone.preprocess_image([baseImg_origin, changeImg_origin]) 
            len_1 = self.color_lists.index(initConfig[1]['hue'])
            if(changeNum > 8):
                break
            else:
                changeNum +=1

        if(judgeTone.get_image_light_mean(changeImg) > 180 or len_1 < 2):
            # 提高 图片对比度 亮度 饱和度
            generate = pilexchange.VisualEffect_pil(changeImg_origin, 1.05, 1.0, 1.0, 1.05)
        else:
            generate = pilexchange.VisualEffect_pil(changeImg_origin, 1.05, 1.05, 1.0, 1.05)
        
        changeImg_origin = generate() # 初步处理之后 的图片
        print('走到这里了')
        baseImg_origin.save('app/cacheImg/base_' + str(self.time) + '.png')
        changeImg_origin.save('app/cacheImg/change_' + str(self.time) + '.png')
        try:
            UploadOSS('base_' + str(self.time) + '.png', 'app/cacheImg/base_' + str(self.time) + '.png').startUpload()
            UploadOSS('change_' + str(self.time) + '.png', 'app/cacheImg/change_' + str(self.time) + '.png').startUpload()
        except Exception as r:
            print('----uploadErr-------', r)
        
        print('----------------完成-----------------')

        # 删除文件
        os.remove('app/cacheImg/base_' + str(self.time) + '.png')
        os.remove('app/cacheImg/change_' + str(self.time) + '.png')

        return {
            'baseImg': 'https://creative-tool.oss-cn-shenzhen.aliyuncs.com/adjustImg/' + 'base_' + str(self.time) + '.png',
            'changeImg': 'https://creative-tool.oss-cn-shenzhen.aliyuncs.com/adjustImg/' + 'change_' + str(self.time) + '.png'
        }
        