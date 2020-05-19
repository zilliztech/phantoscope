# 识别图片中的人脸并根据人脸搜索

##  背景
提取画面中的人脸并进行搜索
##  使用到的模块
face embedding && MTCNN-face-detector  in [omnisearch operators](https://github.com/ReigenAraka/omnisearch-operators)
##  准备数据
下载包含人脸的实验数据
```
curl http://host.robots.ox.ac.uk/pascal/VOC/voc2012/VOCtrainval_11-May-2012.tar -o /tmp/VOCtrainval_11-May-2012.tar
```


## 开始
1.运行 face-embedding 与 mtcnn-face-detector 

    docker run -d -p 50004:50004 milvus.io/om-operators/face-embedding:v1 -e OP_ENDPOINT=127.0.0.1:50004
    docker run -d -p 50005:50005 milvus.io/om-operators/mtcnn-face-detector:v1 -e OP_ENDPOINT=127.0.0.1:50005

2.将 face-embedding 与 mtcnn-face-detector 加载到 omnisearch 中


    curl --location --request POST '127.0.0.1:5000/v1/operator/regist' \
	--header 'Content-Type: application/json' \
	--data-raw '{
		"endpoint": "127.0.0.1:50004",
		"name": "face_embedding"
	}'
    curl --location --request POST '127.0.0.1:5000/v1/operator/regist' \
	--header 'Content-Type: application/json' \
	--data-raw '{
		"endpoint": "127.0.0.1:50005",
		"name": "mtcnn_face_detector"
    }'
3.创建一条 pipeline 用于提取人脸并将数据转化为向量
```
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
```
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
```
tar xvf /tmp/VOCtrainval_11-May-2012.tar
python load_data.py /tmp/VOCtrainval_11-May-2012.tar
```
6.开始进行搜索
```
curl --location --request POST '127.0.0.1:5000/v1/application/face-example/search' \
--header 'Content-Type: application/json' \
--data-raw '{
	"fields": {
        "full": {
            "url": "https://tse2-mm.cn.bing.net/th/id/OIP.d0Uth461I3nJDr28WXudhgHaHa?w=204&h=189&c=7&o=5&dpr=2&pid=1.7"
        }
    },
    "topk": 10,
    "nprobe": 20
}'
```
