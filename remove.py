"""
地图地址去重
@auther

@a
"""

import re
# 去重操作
# 读取文件，然后按行处理，使用字典来跟踪已看到的text值
seen_texts = set()
unique_lines = []
#去掉text属性中只有数字或英文的
def is_numeric_or_english(text):
     return bool(re.match(r'^[a-zA-Z0-9]+$', text))
with open('demo_z63.txt', 'r', encoding='utf-8') as file:
    for line in file:
        # 假设每行的第一个属性总是text，我们可以简单地通过分割来找到它
        parts = line.split(',', 1)  # 只分割一次，以找到text属性
        text = parts[0].split(':', 1)[1].strip()  # 提取text属性的值

        if text not in seen_texts :
            if not is_numeric_or_english(text):   #将这些行去掉 纯英文和数字的去掉
               seen_texts.add(text)
               unique_lines.append(line)

        # 现在将去重后的行写回文件或进行其他处理
with open('newdemo_z63.txt', 'w', encoding='utf-8') as file:
    for line in unique_lines:
        file.write(line)

