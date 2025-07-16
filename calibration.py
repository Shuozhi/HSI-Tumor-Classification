import cv2
import numpy as np
import os
def Calibration(origin_img):
    white = cv2.imread('w.jpg', 0)
    black = cv2.imread('b.jpg', 0)



    np.seterr(divide='ignore', invalid='ignore')  # 消除被除数为0的警告
    bwCali_img = np.divide((origin_img - black), (white - black)) * 255
    #bwCali_img.astype("uint8")
    bwCali_img = np.array(bwCali_img, dtype='uint8')   # 要保存成图片一定要加这一句，  因为数组运算后数组的dtype类型就改变了。
    return bwCali_img




folder_path = "E:\\new\\1777452 ypz\\1777452_frames"
image_extensions = ('.jpg')

for root, dirs, files in os.walk(folder_path):
    for file in files:
        if file.lower().endswith(image_extensions):
            full_path = os.path.join(root, file)
            origin_img = cv2.imread(full_path,0)
            a = Calibration(origin_img)
            cv2.imwrite(os.path.join('E:\\new\\1777452 ypz\\cali', file),a)
