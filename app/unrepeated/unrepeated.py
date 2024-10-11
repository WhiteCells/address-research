import re
import os
from app.config import UnrepeatedConfig, repeated_lines


# 去重操作
# 读取文件，然后按行处理，使用字典来跟踪已看到的text值
seen_texts = set()


#去掉text属性中只有数字或英文的
def is_numeric_or_english(text):
     return bool(re.match(r'^[a-zA-Z0-9]+$', text))


# todo
# 去重单文字、xxx路 ...


def unrepeated(file_path):
    """
    地址去重 todo
    : file_path: 需要去重的文件路径
    """
    
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
    
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.split(',')
            
            line_num = parts[-1].split(':')[1].strip()
            
            if line_num in repeated_lines:
                continue
            
            text = parts[0].split(':')[1].strip()

            if text in seen_texts:
                continue

            if is_numeric_or_english(text):
                continue
            
            seen_texts.add(text)
            
            with open(f'{UnrepeatedConfig.OUTPUT_PATH}/{rank}/{filename}.txt', 'a', encoding='utf-8') as f:
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