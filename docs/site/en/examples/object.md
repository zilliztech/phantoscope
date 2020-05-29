# Detect object from an Image and Search

##  Description
This article describe how to extract object from an image and use it to conduct an object search. 
##  Operators to Use
- **ssd-object-detector**
- **xception**
> You can find the these two operators from [Phantoscope operators](https://github.com/ReigenAraka/omnisearch-operators)

##  Prerequisite

Ensure that you have downloaded the following **.tar** package.

```bash
curl http://www.vision.caltech.edu/Image_Datasets/Caltech256/256_ObjectCategories.tar -o /tmp/256-object.tar
```

## Steps
1. Run **ssd-object-detector** and **xception**. Set the environment variable `host_ip` as your local Intranet IP.  

```bash
export host_ip=192.168.2.3
docker run -d -p 50010:50010 -e OP_ENDPOINT=${host_ip}:50010 milvus.io/om-operators/ssd-object-detector:v1 
docker run -d -p 50011:50011 -e OP_ENDPOINT=${host_ip}:50011 milvus.io/om-operators/xception:v1 
```

2. Load **ssd-object-detector** and **xception** to Phantoscope. 

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

3. Create a pipeline for extracting human face and converting it to vector. 

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
4. Create an application for running the pipeline.

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
5. Upload the package you have downloaded. 

```bash
tar xvf /tmp/256-object.tar
python load_data.py -d /tmp/256_ObjectCategories -n object-example
```

6. Conduct an object search. 

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
