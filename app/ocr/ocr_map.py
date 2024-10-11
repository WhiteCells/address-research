from PIL import Image
import numpy as np
import paddlehub as hub
import os
import cv2
from app.config import OcrConfig, repeated_lines
from collections import defaultdict


# 设置最大图像像素数
Image.MAX_IMAGE_PIXELS = None
os.environ["OPENCV_IO_MAX_IMAGE_PIXELS"] = pow(2, 40).__str__()

# 加载 OCR 模型
ocr = hub.Module(name="chinese_ocr_db_crnn_server")

# 设置窗口和步长大小
window_size = (1024, 1024)
step_size = (512, 512)


def ocr_map(file_path):
    """
    OCR 识别单文件
    : file_path: 文件路径
    """
    line_cnt = 0
    
    # 按区间存储底边坐标和文本的映射，键为区间范围
    map = defaultdict(list)
    bucket_size = 100  # 设定区间大小
    
    # 打开图像
    pil_img = Image.open(file_path)
    width, height = pil_img.size
    
    # 计算滑动次数
    num_steps_width = (width - window_size[0]) // step_size[0] + 1 if width > window_size[0] else 1
    num_steps_height = (height - window_size[1]) // step_size[1] + 1 if height > window_size[1] else 1

    # 文件名（无后缀） map\15\高德_湖北省_武汉市_江夏区_15.png
    filename = os.path.basename(file_path).split('.')[0]
    rank = filename.split('_')[-1]
    
    # 创建 OCR 输出目录
    if not os.path.exists(f'{OcrConfig.OUTPUT_PATH}'):
        os.mkdir(f'{OcrConfig.OUTPUT_PATH}')
    
    if not os.path.exists(f'{OcrConfig.OUTPUT_PATH}/{rank}'):
        os.mkdir(f'{OcrConfig.OUTPUT_PATH}/{rank}')
    
    with open(f'{OcrConfig.OUTPUT_PATH}/{rank}/{filename}.txt', 'a', encoding="utf-8") as f:
        for i in range(num_steps_height):
            for j in range(num_steps_width):
                # 计算当前窗口的坐标
                left = j * step_size[0]
                top = i * step_size[1]
                right = min(left + window_size[0], width)
                bottom = min(top + window_size[1], height)

                # 裁剪当前窗口
                chunk_pil = pil_img.crop((left, top, right, bottom))
                chunk_cv = np.array(chunk_pil)
                if len(chunk_cv.shape) == 3:
                    if chunk_cv.shape[2] == 4:
                        chunk_cv = cv2.cvtColor(chunk_cv, cv2.COLOR_RGBA2BGR)
                    elif chunk_cv.shape[2] == 3:
                        chunk_cv = chunk_cv[:, :, ::-1]  # RGB to BGR

                # 使用 OCR 进行识别
                results = ocr.recognize_text(
                    images=[chunk_cv],
                    use_gpu=False,
                    output_dir='./res/ocr/chunk',
                    visualization=True,
                    box_thresh=0.5,
                    text_thresh=0.5
                )

                # 处理识别结果
                for result in results:
                    data = result['data']
                    for infomation in data:
                        # 获取新的文本框位置
                        new_text_box_position = [
                            [point[0] + j*step_size[0], point[1] + i*step_size[1]]
                            for point in infomation['text_box_position']
                        ]
                        infomation['text_box_position'] = new_text_box_position

                        # 提取四个角点的坐标
                        top_left_x = new_text_box_position[0][0]
                        top_left_y = new_text_box_position[0][1]
                        top_right_x = new_text_box_position[1][0]
                        top_right_y = new_text_box_position[1][1]
                        bottom_right_x = new_text_box_position[2][0]
                        bottom_right_y = new_text_box_position[2][1]
                        bottom_left_x = new_text_box_position[3][0]
                        bottom_left_y = new_text_box_position[3][1]
                        
                        print('text_box_position:', infomation['text_box_position'])
                        
                        line_ctn += 1

                        # 计算当前文本的区间
                        current_bucket = int(top_left_x // bucket_size)
                        matched = False
                        
                        # 仅在相邻的bucket进行匹配，减少比较次数
                        for bucket in [current_bucket - 1, current_bucket, current_bucket + 1]:
                            if bucket in map:
                                for (prev_bottom_left, prev_bottom_right, prev_text) in map[bucket]:
                                    # 匹配条件：顶边与底边的两个点坐标差在范围内
                                    if (abs(top_left_y - prev_bottom_left[1]) <= 2 and
                                        abs(top_right_y - prev_bottom_right[1]) <= 2 and
                                        abs(top_left_x - prev_bottom_left[0]) <= 100 and
                                        abs(top_right_x - prev_bottom_right[0]) <= 100):
                                        
                                        # 合并之前的文本和当前文本
                                        line = f"text: {prev_text} {infomation['text']}, " \
                                               f"confidence: {infomation['confidence']}, " \
                                               f"text_box_position: {infomation['text_box_position']}, " \
                                               f"line: {line_cnt}\n"
                                        f.write(line)
                                        matched = True
                                        repeated_lines.append(line_cnt)
                                        break
                            if matched:
                                break

                        if not matched:
                            # 如果未匹配到，则写入当前文本
                            line = f"text: {infomation['text']}, " \
                                   f"confidence: {infomation['confidence']}, " \
                                   f"text_box_position: {infomation['text_box_position']}, " \
                                   f"line: {line_ctn}\n"
                            f.write(line)

                        # 保存当前的底边两个点坐标和文本到 map 中，并根据 bucket 组织
                        bucket_index = int(bottom_left_x // bucket_size)
                        map[bucket_index].append(((bottom_left_x, bottom_left_y), 
                                                  (bottom_right_x, bottom_right_y), 
                                                  infomation['text']))


def process_map_dir():
    """
    处理配置 OcrConfig.INPUT_PATH 指定的地图目录
    """
    print('=> OCR INPUT_PATH: ', OcrConfig.INPUT_PATH)
    for root, dirs, files in os.walk(OcrConfig.INPUT_PATH):
        for file in files:
            if file.endswith(".png"):
                print('=> processing: ', os.path.join(root, file))
                ocr_map(os.path.join(root, file))