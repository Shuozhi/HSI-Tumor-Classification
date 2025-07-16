import tifffile
import cv2
import numpy as np
import record_data
# 全局变量存储图像和坐标
current_image = None
original_image = None
g_x = -1
g_y = -1

def mouse_callback(event, x, y, flags, param):
    global current_image, original_image
    global g_x
    global g_y

    # 单击左键时绘制 10x10 正方形
    if event == cv2.EVENT_LBUTTONDOWN:
        # 复制原始图像（避免叠加绘制）
        current_image = original_image.copy()

        # 计算正方形区域（防止越界）
        x0 = max(0, x)
        y0 = max(0, y)
        x1 = min(original_image.shape[1], x0 + 5)  # 宽度边界
        y1 = min(original_image.shape[0], y0 + 5)  # 高度边界

        # 绘制绿色方框
        cv2.rectangle(current_image, (x0, y0), (x1, y1), (0, 255,255), 1)

        # 显示更新后的图像
        cv2.imshow("Select 10x10 Square", current_image)

        # 输出坐标信息
        print(f"正方形左上角坐标: ({x0}, {y0})")
        g_x = x0
        g_y = y0



def read_and_show_layer(tiff_path, layer_index):
    global current_image, original_image

    # 读取指定层
    with tifffile.TiffFile(tiff_path) as tif:
        if layer_index >= len(tif.pages):
            raise ValueError("层索引超出范围")
        layer = tif.pages[layer_index].asarray()

    # 处理非8位图像
    if layer.dtype != np.uint8:
        layer = (layer - layer.min()) / (layer.max() - layer.min()) * 255
        layer = layer.astype(np.uint8)

    # 转换颜色空间（如果是RGB）
    if layer.ndim == 3 and layer.shape[-1] == 3:
        layer = cv2.cvtColor(layer, cv2.COLOR_RGB2BGR)

    # 保存原始图像和显示副本
    original_image = layer.copy()
    current_image = original_image.copy()



if __name__ == '__main__':
    # 替换为你的 TIFF 文件路径和层索引
    tiff_path = "G:\\zsyy\\new\\1771239 qxm_3\\tifff_20ms\\frame_004548.tif"
    layer_index = 2  # 选择第0层
    read_and_show_layer(tiff_path, layer_index)

    # 创建窗口并绑定回调
    cv2.namedWindow("Select 10x10 Square")
    cv2.setMouseCallback("Select 10x10 Square", mouse_callback)

    # 显示初始图像
    cv2.imshow("Select 10x10 Square", current_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    record_data.extract_gray_values(
        tiff_path=tiff_path,  #"G:\\zsyy\\new\\1577230_shn_3\\tifff\\frame_001942.tif",
        csv_path="output.csv",
        x=g_x,  # 水平坐标
        y=g_y,  # 垂直坐标
        nameee='qxm'  # 患者名字
    )












