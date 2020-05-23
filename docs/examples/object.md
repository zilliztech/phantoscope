# 识别图片中的物体并根据物体搜索

##  背景
提取画面中的物体并进行搜索
##  使用到的模块
ssd-object-detector &&  xception in [omnisearch operators](https://github.com/ReigenAraka/omnisearch-operators)

##  准备数据
下载包含物体的实验数据
```bash
curl http://www.vision.caltech.edu/Image_Datasets/Caltech256/256_ObjectCategories.tar -o /tmp/256-object.tar
```

## 开始
1.运行 ssd-object-detector 与 xception, 环境变量 host_ip 的值需要替换为本机局域网ip
```bash
export host_ip=192.168.2.3
docker run -d -p 50010:50010 -e OP_ENDPOINT=${host_ip}:50010 milvus.io/om-operators/ssd-object-detector:v1 
docker run -d -p 50011:50011 -e OP_ENDPOINT=${host_ip}:50011 milvus.io/om-operators/xception:v1 
```
    
2.将 ssd-object-detector与 xception 加载到 omnisearch 中
```bash
curl --location --request POST '127.0.0.1:5000/v1/operator/regist' \
--header 'Content-Type: application/json' \
--data-raw '{
    "endpoint": "${host_ip}:50010",
    "name": "ssd_object"
}'
curl --location --request POST '127.0.0.1:5000/v1/operator/regist' \
--header 'Content-Type: application/json' \
--data-raw '{
    "endpoint": "${host_ip}:50011",
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
tar xvf /tmp/256-object.tar
python load_data.py -d /tmp/256_ObjectCategories -n object-example
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
