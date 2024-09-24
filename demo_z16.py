from PIL import Image
import numpy as np
import paddlehub as hub
import os
import cv2

# 设置最大图像像素数
Image.MAX_IMAGE_PIXELS = None
os.environ["OPENCV_IO_MAX_IMAGE_PIXELS"] = pow(2, 40).__str__()

# 加载OCR模型
ocr = hub.Module(name="chinese_ocr_db_crnn_server")

# 打开图像
pil_img = Image.open('macheng_z10 (7).png')
width, height = pil_img.size


# 设置窗口和步长大小
window_size = (1024, 1024)
step_size = (512,512)

# 计算滑动次数
num_steps_width = (width - window_size[0]) // step_size[0] + 1 if width > window_size[0] else 1
num_steps_height = (height - window_size[1]) // step_size[1] + 1 if height > window_size[1] else 1

# 打开文件以写入识别结果
with open('demo_z64.txt', 'a', encoding="utf-8") as f:
    # 遍历每个滑动窗口
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

            # 使用OCR进行识别
            results = ocr.recognize_text(
                images=[chunk_cv],
                use_gpu=False,
                output_dir='ocr_res161',
                visualization=True,
                box_thresh=0.5,
                text_thresh=0.5
            )

            # 处理识别结果
            for result in results:
                data = result['data']
                for infomation in data:
                    new_text_box_position = [
                        [point[0] + j*step_size[0], point[1] + i*step_size[1]]  # 对每个点的坐标进行修改
                        for point in infomation['text_box_position']
                    ]
                    infomation['text_box_position'] = new_text_box_position
                    print('text:', infomation['text'])
                    print('confidence:', infomation['confidence'])
                    print('text_box_position:', infomation['text_box_position'])
                    f.write('text: ' + str(infomation['text']) + ',confidence: ' + str(
                        infomation['confidence']) + ',text_box_position: ' + str(
                        infomation['text_box_position']) + '\n')

