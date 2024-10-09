# 地址修复研究项目

### 安装依赖

```shell
pip install -r requestments.txt -i https://pypi.tuna.tsinghua.edu.cn/simple 
```

### 项目结构

```sh
├─app
│  ├─amp_api
│  │  └─res
│  ├─db
│  ├─ocr
│  │  ├─chunk
│  │  └─res
│  └─unrepeated
│     └─res
└──map
   ├─15
   └─16
```

- 代码复用

1. 下载地图
    - 地图根目录命名方式：<map>_<province>_<city>_<district>_<rank>
        - 例子：高德_湖南省_洛阳市_新安县_15
    - OCR 识别的路径：<map>_<province>_<city>_<district>_<rank>/tile-merge/z=<rank>.png
        - 例子：高德_湖南省_洛阳市_新安县_15/tile-merge/z=15.png

2. OCR 识别：
    - 输入：下载地图的路径
    - 输出：识别的保存路径，ocr/res/<map>_<province>_<city>_<district>_<rank>.txt
        - 例子：ocr_res/高德_湖南省_洛阳市_新安县_15.txt
 
3. 地址去重：
    - 输入：需要去重的地址文件的路径，OCR 识别的保存路径
    - 输出：去重结果的地址文件的保存路径，nurepeated/res/<map>_<province>_<city>_<district>_<rank>.txt

5. 高德验证地址：
    - 输入：需要验证的地址文件的路径，地址去重的路径
    - 输出：验证后的地址文件的保存路径，amp_api/res/<map>_<province>_<city>_<district>_<rank>.txt

4. 地址入库：
    - 输入：高德验证后的地址，按照文件名进行区分存放

---

### 其他地图验证

- 百度

- bing