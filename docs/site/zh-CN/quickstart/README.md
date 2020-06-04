# Phantoscope 快速开始
## 在开始之前
确定 Phantoscope 正在运行。

## 准备环境
```bash
$ chmod +x scripts/prepare.sh
$ ./scripts/prepare.sh
```

## 下载图片数据
```bash
$ curl http://www.vision.caltech.edu/Image_Datasets/Caltech256/256_ObjectCategories.tar -o /tmp/vgg-example.tar
```

## 上传图片数据
```bash
$ tar xvf /tmp/vgg-example.tar -C /tmp
$ python3 load_data.py -s 127.0.0.1:5000 -a example -p example /tmp/256_ObjectCategories
```
上传图片根据机器性能不同,时间会有差异
## 使用 Preview 进行搜索
```bash
docker run -d -e API_URL=http://$LOCAL_ADDRESS:5000 -p 8000:80 phantoscope/preview:latest
```
浏览器打开 127.0.0.1:8000 选择图片进行搜索

## 使用 API 进行搜索
```bash
$ curl --location --request POST '127.0.0.1:5000/v1/application/example/search' \
--header 'Content-Type: application/json' \
--data-raw '{
    "fields": {
        "example": {
            "url": "https://tse2-mm.cn.bing.net/th/id/OIP.C3pWPyFPhBMiBeWoncc24QHaCq?w=300&h=108&c=7&o=5&dpr=2&pid=1.7"
        }
    },
    "topk": 10,
    "nprobe": 20
}'
```
