import os
from PIL import Image
from PIL import ImageEnhance
 
 
# def augument(image_path, parent):
#      #读取图片
#      image = Image.open(image_path)
 
#      image_name = os.path.split(image_path)[1]
#      name = os.path.splitext(image_name)[0]
#      #变亮
#      #亮度增强,增强因子为0.0将产生黑色图像；为1.0将保持原始图像。
#      enh_bri = ImageEnhance.Brightness(image)
#      brightness = 1.5
#      image_brightened1 = enh_bri.enhance(brightness)
#      image_brightened1.save(os.path.join(parent, '{}_bri1.png'.format(name)))
#      #变暗
#      enh_bri = ImageEnhance.Brightness(image)
#      brightness = 0.8
#      image_brightened2 = enh_bri.enhance(brightness)
#      image_brightened2.save(os.path.join(parent, '{}_bri2.png'.format(name)))
#      #色度,增强因子为1.0是原始图像(饱和度)
#      # 色度增强
#      enh_col = ImageEnhance.Color(image)
#      color = 1.5
#      image_colored1 = enh_col.enhance(color)
#      image_colored1.save(os.path.join(parent, '{}_col1.png'.format(name)))
#      # 色度减弱
#      enh_col = ImageEnhance.Color(image)
#      color = 0.8
#      image_colored1 = enh_col.enhance(color)
#      image_colored1.save(os.path.join(parent, '{}_col2.png'.format(name)))
#      #对比度，增强因子为1.0是原始图片
#      # 对比度增强
#      enh_con = ImageEnhance.Contrast(image)
#      contrast = 1.5
#      image_contrasted1 = enh_con.enhance(contrast)
#      image_contrasted1.save(os.path.join(parent, '{}_con1.png'.format(name)))
#      # 对比度减弱
#      enh_con = ImageEnhance.Contrast(image)
#      contrast = 0.8
#      image_contrasted2 = enh_con.enhance(contrast)
#      image_contrasted2.save(os.path.join(parent, '{}_con2.png'.format(name)))
#      # 锐度，增强因子为1.0是原始图片
#      # 锐度增强
#      enh_sha = ImageEnhance.Sharpness(image)
#      sharpness = 3.0
#      image_sharped1 = enh_sha.enhance(sharpness)
#      image_sharped1.save(os.path.join(parent, '{}_sha1.png'.format(name)))
#      # 锐度减弱
#      enh_sha = ImageEnhance.Sharpness(image)
#      sharpness = 0.8
#      image_sharped2 = enh_sha.enhance(sharpness)
#      image_sharped2.save(os.path.join(parent, '{}_sha2.png'.format(name)))

class VisualEffect_pil:
     """
     1、对比度：白色画面(最亮时)下的亮度除以黑色画面(最暗时)下的亮度；
     2、色彩饱和度：：彩度除以明度，指色彩的鲜艳程度，也称色彩的纯度；(饱和度)
     3、色调：向负方向调节会显现红色，正方向调节则增加黄色。适合对肤色对象进行微调；
     4、锐度：是反映图像平面清晰度和图像边缘锐利程度的一个指标。
     """
     def __init__(
        self,
        image,
        contrast_factor,
        brightness_delta,
        sharpness_delta,
        saturation_factor
        ):
        self.image = image
        self.contrast_factor = contrast_factor # 对比度
        self.brightness_delta = brightness_delta # 亮度
        self.sharpness_delta = sharpness_delta # 锐度
        self.saturation_factor = saturation_factor # 饱和度 色度
     
     def __call__(self):
        """
        将视觉效果应用到图片上
        """
        #读取图片
     #    image = Image.open(self.path)
        if self.contrast_factor:
            self.image = self.adjust_contrast(self.image, self.contrast_factor)

        if self.brightness_delta:
            self.image = self.adjust_brightness(self.image, self.brightness_delta)

        if self.saturation_factor:
            self.image = self.adjust_saturation(self.image, self.saturation_factor)
          
        if self.sharpness_delta:
            self.image = self.adjust_sharpness(self.image, self.sharpness_delta)

        return self.image
     
     def adjust_brightness(self, image, delta):
          #亮度增强,增强因子为0.0将产生黑色图像；为1.0将保持原始图像。
          enh_bri = ImageEnhance.Brightness(image)
          brightness = delta
          image = enh_bri.enhance(brightness)
          return image
     
     def adjust_contrast(self, image, factor):
          #对比度，增强因子为1.0是原始图片
          # 对比度增强
          enh_con = ImageEnhance.Contrast(image)
          contrast = factor
          image = enh_con.enhance(contrast)
          return image
     
     def adjust_saturation(self, image, factor):
          #色度,增强因子为1.0是原始图像(饱和度)
          enh_col = ImageEnhance.Color(image)
          color = factor
          image = enh_col.enhance(color)
          return image
     
     def adjust_sharpness(self, image, delta):
          # 锐度，增强因子为1.0是原始图片
          # 锐度增强
          enh_sha = ImageEnhance.Sharpness(image)
          sharpness = delta
          image = enh_sha.enhance(sharpness)
          return image
     

# if __name__ == "__main__":
#      path = '图像数据/demo1/role.png'
#      image = Image.open(path).convert('RGBA')
#      generate = VisualEffect_pil(image, 0.1, 0.1, 0.1, 0.1)
#      baseImg_origin = generate()
#      baseImg_origin.save('图像数据/demo1/role_result_1.png')

# dir = 'data'
# for parent, dirnames, filenames in os.walk(dir):
#      for filename in filenames:
#           fullpath = os.path.join(parent + '/', filename)
#           if 'png' in fullpath:
#                print(fullpath, parent)
#                augument(fullpath, parent)
