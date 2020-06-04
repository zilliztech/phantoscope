# 识别图片中的人脸并根据人脸搜索

##  背景
提取图片中的人脸并进行搜索
##  使用到的模块

- **face embedding**  
- **MTCNN-face-detector**  
> 可以在 [Phantoscope operators](https://github.com/ReigenAraka/omnisearch-operators) 中找到这两个 operator 的描述。

##  准备数据
下载包含人脸的实验数据
```bash
curl http://host.robots.ox.ac.uk/pascal/VOC/voc2012/VOCtrainval_11-May-2012.tar -o /tmp/VOCtrainval_11-May-2012.tar
```

## 开始
1.运行 face-embedding 与 mtcnn-face-detector, 环境变量 ```LOCAL_ADDRESS``` 的值需要替换为本机局域网ip
```bash
export LOCAL_ADDRESS=$(ip a | grep -Eo 'inet (addr:)?([0-9]*\.){3}[0-9]*' | grep -Eo '([0-9]*\.){3}[0-9]*' | grep -v '127.0.0.1'| head -n 1)
docker run -d -p 50004:50004 -e OP_ENDPOINT=${LOCAL_ADDRESS}:50004 psoperator/face-encoder:latest
docker run -d -p 50005:50005 -e OP_ENDPOINT=${LOCAL_ADDRESS}:50005 psoperator/face-detector:latest
```

2.将 face-embedding 与 mtcnn-face-detector 加载到 Phantoscope 中

```bash
curl --location --request POST '127.0.0.1:5000/v1/operator/regist' \
--header 'Content-Type: application/json' \
--data-raw '{
    "endpoint": "${LOCAL_ADDRESS}:50004",
    "name": "face_embedding"
}'
	
curl --location --request POST '127.0.0.1:5000/v1/operator/regist' \
--header 'Content-Type: application/json' \
--data-raw '{
    "endpoint": "${LOCAL_ADDRESS}:50005",
    "name": "mtcnn_face_detector"
}'
```

3.创建一条 pipeline 用于提取人脸并将数据转化为向量
```bash
curl --location --request POST '127.0.0.1:5000/v1/pipeline/face' \
--header 'Content-Type: application/json' \
--data-raw '{
	"input": "image",
	"description": "face detect and encode",
	"processors": "mtcnn_face_detector",
	"encoder": "face_embedding",
	"indexFileSize": 1024
}'
```
4.创建一个 application 来准备运行 pipeline
```bash
curl --location --request POST '127.0.0.1:5000/v1/application/face-example' \
--header 'Content-Type: application/json' \
--data-raw '{
    "fields":{
        "face": {
            "type": "object",
            "pipeline": "face"
        }
    },
    "s3Buckets": "face"
}'
```
5.上传下载好的的数据
```bash
tar xvf /tmp/VOCtrainval_11-May-2012.tar -C /tmp
python3 load_data.py -d /tmp/VOCdevkit/ -a face-example -p face
```
6.开始进行搜索
```bash
curl --location --request POST '127.0.0.1:5000/v1/application/face-example/search' \
--header 'Content-Type: application/json' \
--data-raw '{
	"fields": {
        "face": {
            "url": "https://tse2-mm.cn.bing.net/th/id/OIP.d0Uth461I3nJDr28WXudhgHaHa?w=204&h=189&c=7&o=5&dpr=2&pid=1.7"
        }
    },
    "topk": 10,
    "nprobe": 20
}'
```
