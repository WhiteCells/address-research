import cv2
import paddlehub as hub

# 加载移动端预训练模型
# ocr = hub.Module(name="chinese_ocr_db_crnn_mobile")
# 服务端可以加载大模型，效果更好
ocr = hub.Module(name="chinese_ocr_db_crnn_server")

# 加载超大图像
image = cv2.imread('shiyan_z12.png')

# 设置滑动窗口大小
window_width = 512
window_height = 512

# 步长（窗口移动的像素数）
step_size = 256

# 获取图像尺寸
height, width, _ = image.shape

# 遍历图像
for y in range(0, height, step_size):
    for x in range(0, width, step_size):
        # 定义窗口的结束坐标
        end_x = min(x + window_width, width)
        end_y = min(y + window_height, height)

        # 提取窗口中的图像块
        window = image[y:end_y, x:end_x]

        # 使用 Tesseract 进行 OCR 识别
        # text = pytesseract.image_to_string(window)
        results = ocr.recognize_text(
            images=[window],  # 图片数据，ndarray.shape 为 [H, W, C]，BGR格式；
            use_gpu=False,  # 是否使用 GPU；若使用GPU，请先设置CUDA_VISIBLE_DEVICES环境变量
            output_dir='ocr_result',  # 图片的保存路径，默认设为 ocr_result；
            visualization=True,  # 是否将识别结果保存为图片文件；
            box_thresh=0.5,  # 检测文本框置信度的阈值；
            text_thresh=0.5)  # 识别中文文本置信度的阈值；

        # 输出识别结果
        for result in results:
            data = result['data']
            save_path = result['save_path']
            for infomation in data:
                print('text: ', infomation['text'], '\nconfidence: ', infomation['confidence'], '\ntext_box_position: ',
                      infomation['text_box_position'])
                with open('address.log', 'a', encoding="utf-8") as f:
                    f.write('text: ' + str(infomation['text']) + '\nconfidence: ' + str(infomation[
                        'confidence']) + '\ntext_box_position: ' + str(infomation['text_box_position']))
                f.close()

