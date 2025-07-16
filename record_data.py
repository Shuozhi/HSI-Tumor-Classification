import tifffile
import csv
import os
import cv2
import numpy as np

def extract_gray_values(tiff_path, x, y, csv_path,nameee):
    """
    从多层 TIFF 文件中提取指定坐标的灰度值并写入 CSV 文件

    参数:
    tiff_path (str): TIFF 文件路径
    x (int): X 坐标 (水平方向)
    y (int): Y 坐标 (垂直方向)
    csv_path (str): 输出 CSV 文件路径
    """
    filename = os.path.basename(tiff_path)
    img_id = os.path.splitext(filename)[0]
    print('id是',img_id)
    # 验证坐标有效性
    if x < 0 or y < 0:
        raise ValueError("坐标不能为负数")

    # 创建 CSV 文件并写入表头
    file_exists = os.path.exists(csv_path)
    with open(csv_path, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)

        # 如果文件不存在，写入表头
        if not file_exists:
            writer.writerow(['people','img_id','Layer', 'X', 'Y', 'GrayValue'])

        # 读取 TIFF 文件
        with tifffile.TiffFile(tiff_path) as tif:
            for layer_idx, page in enumerate(tif.pages):
                try:
                    layer = page.asarray()


                    # 检查坐标是否越界
                    if y >= layer.shape[0] or x >= layer.shape[1]:
                        print(f"警告：层 {layer_idx} 坐标越界，已跳过")
                        continue

                    # 处理多通道图像 (取第一个通道)
                    if layer.ndim == 3:
                        roi = layer[y:y+5, x:x + 5,0]
                        gray_value = np.mean(roi)

                        #gray_value = layer[y, x, 0]
                    else:

                        roi = layer[y:y +5, x:x + 5]
                        gray_value = np.mean(roi)

                        #gray_value = layer[y, x]

                    # 写入 CSV 数据
                    writer.writerow([nameee, img_id, layer_idx, x, y, gray_value])

                except Exception as e:
                    print(f"处理层 {layer_idx} 时发生错误: {str(e)}")
                    continue


if __name__ == "__main__":
    print('竟然运行这里了')
    ## 使用示例
    # extract_gray_values(
    #     tiff_path="G:\\zsyy\\new\\1577230_shn_3\\tifff\\frame_001942.tif",
    #     csv_path="output.csv",
    #     x=160,  # 水平坐标
    #     y=295 , # 垂直坐标
    #     nameee = 'shn' #患者名字
    # )