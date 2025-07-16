import cv2
import os


def video_to_frames(video_path, output_folder, frame_prefix='frame_', start_frame=0, end_frame=None, step=1):
    """
    将视频转换为图像序列

    参数:
        video_path: 输入视频文件路径
        output_folder: 输出图像保存目录
        frame_prefix: 输出图像前缀(默认'frame_')
        start_frame: 开始保存的帧号(默认0)
        end_frame: 结束保存的帧号(默认None表示到视频结束)
        step: 帧间隔(默认1表示每帧都保存)
    """
    # 创建输出目录(如果不存在)
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)      #os包常用函数

    # 打开视频文件
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"无法打开视频文件: {video_path}")
        return

    # 获取视频基本信息
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    print(f"视频信息: {fps} FPS, 总帧数: {total_frames}, 分辨率: {width}x{height}")

    # 设置结束帧(如果未指定)
    if end_frame is None or end_frame > total_frames:
        end_frame = total_frames

    # 设置当前帧位置
    cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

    frame_count = start_frame
    saved_count = 0

    while frame_count <= end_frame:
        ret, frame = cap.read()

        if not ret:
            print(f"读取帧 {frame_count} 失败，可能已到达视频末尾")
            break

        # 每隔step帧保存一次
        if frame_count % step == 0:
            # 构造输出文件名
            frame_number = str(saved_count).zfill(6)  # 用0填充到6位数
            output_path = os.path.join(output_folder, f"{frame_prefix}{frame_number}.jpg")

            # 保存帧为图像
            cv2.imwrite(output_path, frame)
            saved_count += 1

            # 打印进度
            if saved_count % 100 == 0:
                print(f"已保存 {saved_count} 帧...")

        frame_count += 1

    # 释放资源
    cap.release()
    print(f"转换完成! 共保存了 {saved_count} 帧图像到 {output_folder}")


# 使用示例
if __name__ == "__main__":
    video_file = "Video1776908 王爱娟.mp4"  # 替换为你的视频文件路径
    output_dir = "1776908_frames"  # 输出目录

    # 转换视频为帧序列(每帧都保存)
    video_to_frames(video_file, output_dir)

    # 如果需要间隔保存，可以设置step参数
    # 例如每5帧保存一次: video_to_frames(video_file, output_dir, step=5)
