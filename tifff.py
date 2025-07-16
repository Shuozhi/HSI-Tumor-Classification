import os
import numpy as np
import cv2
from tifffile import imwrite,imread

# data = np.random.randint(0, 256,
#                         size=(16, 872, 584),  # 形状：(T, Z, Y, X)
#                         dtype=np.uint8)
'''
数据类型	适用灰度范围	典型应用场景
np.uint8	0-255	常规8位图像
np.uint16	0-65535	显微镜/医学影像
np.float32	0.0-1.0	归一化数据
'''

def downsampling(img):
   # 返回2个参数的和."
   # a = cv2.imread(path, 0)
   offset_x = 0                                                        # column offset
   offset_y = 0                                                        # row offset
   downsampled_img = np.empty([16, 584, 436], np.uint8)

   i_src = 0
   j_src = 0

   for k in range(16):
       for i in range(584):
           i_src = offset_y + k // 4 + 4 * i                           # 此句待改   k
           for j in range(436):
               j_src = offset_x + k % 4 + 4 * j
               #print(i_src,j_src)
               downsampled_img[k, i, j] = img[i_src, j_src]
   return downsampled_img


if __name__ == '__main__':
    data = np.random.randint(0, 256,
                             size=(16, 872, 584),  # 形状：(T, Z, Y, X)
                             dtype=np.uint8)
    folder_path = "G:\\zsyy\\new\\1776224 lwl_2\\1776224_80ms_frames"
    image_extensions = ('.jpg')
    print("开始啦")
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith(image_extensions):
                full_path = os.path.join(root, file)
                origin_img = cv2.imread(full_path, 0)
                a = downsampling(origin_img)

                base = os.path.splitext(file)[0]
                new_name = base + '.tif'
                print(new_name)
                add = os.path.join('G:\\zsyy\\new\\1776224 lwl_2\\tifff_80ms', new_name)
                imwrite(add,
                        a,
                        photometric='minisblack',
                        #imagej=True,  # 启用ImageJ元数据兼容模式
                        compression='zlib',
                        metadata={'axes': 'ZYX'}
                )

                # cv2.imwrite(os.path.join('G:\\zsyy\\new\\1577230 shn_3\\tifff', file), a)
                #print(file)
    print("已结束")
