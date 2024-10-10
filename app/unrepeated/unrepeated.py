import re
import os
from app.config import UnrepeatedConfig

# 去重操作
# 读取文件，然后按行处理，使用字典来跟踪已看到的text值
seen_texts = set()
unique_lines = []


#去掉text属性中只有数字或英文的
def is_numeric_or_english(text):
     return bool(re.match(r'^[a-zA-Z0-9]+$', text))


def unrepeated(file_path):
    """
    地址去重 todo
    : file_path: 需要去重的文件路径
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            # 假设每行的第一个属性总是text，我们可以简单地通过分割来找到它
            parts = line.split(',', 1)  # 只分割一次，以找到text属性
            text = parts[0].split(':', 1)[1].strip()  # 提取text属性的值

            if text not in seen_texts:
                if not is_numeric_or_english(text):   #将这些行去掉 纯英文和数字的去掉
                    seen_texts.add(text)
                    unique_lines.append(line)

    # 获取文件名（不包含后缀）
    filename = os.path.basename(file_path).split('.')[0]
    print('=> filename: ', filename)
    
    # 获取地图等级
    rank = filename.split('_')[-1]
    
    # 确保 res/unrepeated 目录存在
    if not os.path.exists(UnrepeatedConfig.OUTPUT_PATH):
        os.mkdir(UnrepeatedConfig.OUTPUT_PATH)
    
    # 确保 res/unrepeated/rank 目录存在
    if not os.path.exists(f'{UnrepeatedConfig.OUTPUT_PATH}/{rank}'):
        os.mkdir(f'{UnrepeatedConfig.OUTPUT_PATH}/{rank}')
    
    # 保存去重后的地址
    with open(f'{UnrepeatedConfig.OUTPUT_PATH}/{rank}/{filename}.txt', 'w', encoding='utf-8') as f:
        for line in unique_lines:
            f.write(line)


def process_res_ocr_dir():
    """
    去重 res/ocr 目录下的所有地址文件
    """
    for root, dirs, files in os.walk(UnrepeatedConfig.INPUT_PATH):
        for file in files:
            if file.endswith(".txt"):
                print('=> processing: ', os.path.join(root, file))
                unrepeated(os.path.join(root, file))