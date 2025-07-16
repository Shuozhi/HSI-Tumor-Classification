"""
@Time:  2022/6/9  10:00
@Auth:  李硕祉
@File:  downsampling.py
@DESCRIPTION:

黑白矫正
4*4  /  5*5  降采样

"""

import numpy as np
import cv2
import tifffile
from cor_array import cor
# from osgeo import gdal


# 白板拼接
def six_white (device_doc):

    w1 = cv2.imread(device_doc + '/w1.tif', 0)
    w2 = cv2.imread(device_doc + '/w2.tif', 0)
    w3 = cv2.imread(device_doc + '/w3.tif', 0)
    w4 = cv2.imread(device_doc + '/w4.tif', 0)
    w5 = cv2.imread(device_doc + '/w5.tif', 0)
    w6 = cv2.imread(device_doc + '/w6.tif', 0)
    w1 = w1[0:544, 0:682]
    w2 = w2[544:1088, 0:682]
    w3 = w3[0:544, 682:1364]
    w4 = w4[544:1088, 682:1364]
    w5 = w5[0:544, 1364:2048]
    w6 = w6[544:1088, 1364:2048]

    white = np.empty([1088, 2048], np.uint8)
    white[0:544, 0:682] = w1
    white[544:1088, 0:682] = w2
    white[0:544, 682:1364] = w3
    white[544:1088, 682:1364] = w4
    white[0:544, 1364:2048] = w5
    white[544:1088, 1364:2048] = w6

    cv2.imwrite(device_doc+'/white.tif',white)
    # cv2.imshow('ll',white)
    # cv2.waitKey(0)

    return white


# 降采样
def downsampling(img):
   # 返回2个参数的和."
   # a = cv2.imread(path, 0)
   offset_x = 0                                                        # column offset
   offset_y = 0                                                        # row offset
   downsampled_img = np.empty([217, 409, 25], np.float64)

   i_src = 0
   j_src = 0

   for k in range(25):
       for i in range(217):
           i_src = offset_y + k // 5 + 5 * i                           # 此句待改   k
           for j in range(409):
               j_src = offset_x + k % 5 + 5 * j
               downsampled_img[i, j, k] = img[i_src, j_src]
   return downsampled_img                                              # 是一个数组





if __name__ == '__main__':
    device_doc = '20220706'
    img_name ='Q255B_3_A_0_0_0_0_3.tif'
    six_white(device_doc)

    #
    # white_data = cv2.imread(device_doc + '/white.tif',0)
    # black_data = cv2.imread(device_doc + '/black.tif',0)
    # img_data = cv2.imread(device_doc + '/'+ img_name,0)
    # print('00000000')
    # # 黑白矫正
    # np.seterr(divide='ignore', invalid='ignore')  # 消除被除数为0的警告
    # normalization_result = np.divide((img_data - black_data), (white_data - black_data))
    # normalization_result = normalization_result*255
    # normalization_result = np.array(normalization_result, dtype='uint8')
    # tifffile.imwrite('correction/' + img_name, normalization_result)
    # print('1111111')


    # # 降采样  downsampled_data 是降采样后的三维数据
    # downsampled_data = downsampling(normalization_result)
    # real_data =  cor *downsampled_data
    # print(np.shape(real_data))



    #显示各层图片
    # n = 0
    # show = downsampled_data[:,:,n]
    # show = np.array(show,dtype='uint8')
    # cv2.imshow('0',show)
    # cv2.waitKey(0)

    ## gdal 方法
    # downsampled_data = np.array(downsampled_data, dtype='float32')
    # dst_ds = gdal.GetDriverByName('GTiff').Create("hello.tif", 217, 409, 25, gdal.GDT_CFloat32)
    # dst_ds.SetGeoTransform([1, 1, 1, 1, 1, 1])
    # # raster = np.zeros((217, 409, 25), dtype='unit8')
    # dst_ds.GetRasterBand(25).WriteArray(downsampled_data)
    # # Once we're done, close properly the dataset
    # dst_ds = None




    # write_img('downsampled/'+img_name,'',downsampled_data)
    # tifffile.imwrite('try.tif', res)


    print('eeeeeee')