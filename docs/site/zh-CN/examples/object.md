# 识别图片中的物体并根据物体搜索

##  背景
提取画面中的物体并进行搜索
##  使用到的模块
- **ssd-object-detector**
- **xception**
> 可以在 [Phantoscope operators](https://github.com/ReigenAraka/omnisearch-operators) 中找到这两个 operator 的描述。

##  准备数据
下载包含物体的实验数据
```bash
curl http://www.vision.caltech.edu/Image_Datasets/Caltech256/256_ObjectCategories.tar -o /tmp/256-object.tar
```

## 开始
1.运行 ssd-object-detector 与 xception, 环境变量 ```LOCAL_ADDRESS``` 的值需要替换为本机局域网ip
```bash
export LOCAL_ADDRESS=LOCAL_ADDRESS=$(ip a | grep -Eo 'inet (addr:)?([0-9]*\.){3}[0-9]*' | grep -Eo '([0-9]*\.){3}[0-9]*' | grep -v '127.0.0.1'| head -n 1)
docker run -d -p 50010:50010 -e OP_ENDPOINT=${LOCAL_ADDRESS}:50010 fsoperator/ssd-detector:latest
docker run -d -p 50011:50011 -e OP_ENDPOINT=${LOCAL_ADDRESS}:50011 fsoperator/xception-encoder:latest
```

2.将 ssd-object-detector与 xception 加载到 Phantoscope 中

```bash
curl --location --request POST '127.0.0.1:5000/v1/operator/regist' \
--header 'Content-Type: application/json' \
--data-raw '{
    "endpoint": "${LOCAL_ADDRESS}:50010",
    "name": "ssd_object"
}'
curl --location --request POST '127.0.0.1:5000/v1/operator/regist' \
--header 'Content-Type: application/json' \
--data-raw '{
    "endpoint": "${LOCAL_ADDRESS}:50011",
    "name": "xception"
}'
```

3.创建一条 pipeline 用于提取物体并将数据转化为向量
```bash
curl --location --request POST '127.0.0.1:5000/v1/pipeline/object' \
--header 'Content-Type: application/json' \
--data-raw '{
	"input": "image",
	"description": "object detect and encode",
	"processors": "ssd_object",
	"encoder": "xception",
	"indexFileSize": 1024
}'
```
4.创建一个 application 来准备运行 pipeline
```bash
curl --location --request POST '127.0.0.1:5000/v1/application/object-example' \
--header 'Content-Type: application/json' \
--data-raw '{
    "fields":{
        "object": {
            "type": "object",
            "pipeline": "object"
        }
    },
    "s3Buckets": "object"
}'
```

5.上传下载好的的数据

```bash
tar xvf /tmp/256-object.tar -C /tmp
python3 load_data.py -d /tmp/256_ObjectCategories -a object-example -p object
```


6.开始进行搜索
```bash
curl --location --request POST '127.0.0.1:5000/v1/application/object-example/search' \
--header 'Content-Type: application/json' \
--data-raw '{
	"fields": {
        "object": {
            "url": "https://tse4-mm.cn.bing.net/th/id/OIP.RTFEnp5e4zb-CkbYvO1KfwHaHT?pid=Api&rs=1"
        }
    },
    "topk": 10,
    "nprobe": 20
}'
```
