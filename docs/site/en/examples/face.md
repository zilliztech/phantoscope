# Detect Human Face from an Image and Search

##  Description
This article describe how to extract human face from an image and use it to conduct a face search. 
##  Operators to Use

- **face-embedding** 
- **mtcnn-face-detector**

>  You can find the these two operators from [Phantoscope operators](https://github.com/ReigenAraka/omnisearch-operators)

##  Prerequisite
Ensure that you have downloaded the following **.tar** package.
```bash
curl http://host.robots.ox.ac.uk/pascal/VOC/voc2012/VOCtrainval_11-May-2012.tar -o /tmp/VOCtrainval_11-May-2012.tar
```

## Steps
1. Run **face-embedding** and **mtcnn-face-detector**. Set the environment variable `LOCAL_ADDRESS` as your local intranet IP.  

```bash
export LOCAL_ADDRESS=$(ip a | grep -Eo 'inet (addr:)?([0-9]*\.){3}[0-9]*' | grep -Eo '([0-9]*\.){3}[0-9]*' | grep -v '127.0.0.1'| head -n 1)
docker run -d -p 50004:50004 -e OP_ENDPOINT=${LOCAL_ADDRESS}:50004 psoperator/face-encoder:latest
docker run -d -p 50005:50005 -e OP_ENDPOINT=${LOCAL_ADDRESS}:50005 psoperator/face-detector:latest
```

2. Load the **face-embedding** and **mtcnn-face-detector** to Phantoscope.

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

3. Create a pipeline for extracting human face and converting it to vector. 

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

4. Create an application for running the pipeline.

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

5. Upload the package you have downloaded. 

```bash
tar xvf /tmp/VOCtrainval_11-May-2012.tar -C /tmp
python3 load_data.py -d /tmp/VOCdevkit/ -a face-example -p face
```

6. Conduct a human face search. 

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
