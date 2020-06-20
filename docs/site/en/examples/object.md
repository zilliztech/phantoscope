# Detect object from an Image and Search

##  Description
This article describe how to extract object from an image and use it to conduct an object search. 
##  Operators to Use
- **ssd-object-detector**
- **xception**
> You can find the these two operators from [Phantoscope operators](https://github.com/ReigenAraka/omnisearch-operators)

##  Prerequisite

Ensure that you have downloaded the following **.zip** package.

```bash
$ curl http://cs231n.stanford.edu/coco-animals.zip -o /tmp/coco-animals.zip
$ unzip /tmp/coco-animals.zip -d /tmp/
```

## Steps
1. Run **ssd-object-detector** and **xception**. 

```bash
$ export LOCAL_ADDRESS=$(ip a | grep -Eo 'inet (addr:)?([0-9]*\.){3}[0-9]*' | grep -Eo '([0-9]*\.){3}[0-9]*' | grep -v '127.0.0.1'| head -n 1)
$ docker run -d -p 50010:50010 -e OP_ENDPOINT=${LOCAL_ADDRESS}:50010 psoperator/ssd-detector:latest
$ docker run -d -p 50011:50011 -e OP_ENDPOINT=${LOCAL_ADDRESS}:50011 psoperator/xception-encoder:latest
```

2. Register **ssd-object-detector** and **xception** with Phantoscope. 

```bash
# register ssd-object-detector to phantoscope with exposed 50010 port and a self-defined name 'ssd_detector'
$ curl --location --request POST ${LOCAL_ADDRESS}':5000/v1/operator/regist' \
--header 'Content-Type: application/json' \
--data '{
    "endpoint": "'${LOCAL_ADDRESS}':50010",
    "name": "ssd_detector"
}'
# register xception-encoder to phantoscope with exposed 50011 port and a self-defined name 'xception'
$ curl --location --request POST ${LOCAL_ADDRESS}':5000/v1/operator/regist' \
--header 'Content-Type: application/json' \
--data '{
    "endpoint": "'${LOCAL_ADDRESS}':50011",
    "name": "xception"
}'
```

3. Create a pipeline for extracting object and converting it to vector. 

```bash
# create a pipeline with necessary information
$ curl --location --request POST ${LOCAL_ADDRESS}':5000/v1/pipeline/object_pipeline' \
--header 'Content-Type: application/json' \
--data '{
	"input": "image",
	"description": "object detect and encode",
	"processors": "ssd_detector",
	"encoder": "xception",
	"indexFileSize": 1024
}'
```
4. Create an application for running the pipeline.

```bash
# create an application with a self-define field name assocatied with pipeline created in step3 
$ curl --location --request POST ${LOCAL_ADDRESS}':5000/v1/application/object-example' \
--header 'Content-Type: application/json' \
--data '{
    "fields":{
        "object_field": {
            "type": "object",
            "pipeline": "object_pipeline"
        }
    },
    "s3Buckets": "object-s3"
}'
```
5. Upload the package you have downloaded. 

```bash
$ pip3 install requests tqdm
$ python3 scripts/load_data.py -d /tmp/coco-animals/train -a object-example -p object_pipeline
```

6. Conduct an object search. 

```bash
$ curl --location --request POST ${LOCAL_ADDRESS}':5000/v1/application/object-example/search' \
--header 'Content-Type: application/json' \
--data '{
	"fields": {
        "object_field": {
            "url": "https://ss2.bdstatic.com/70cFvnSh_Q1YnxGkpoWK1HF6hhy/it/u=3506601383,2488554559&fm=26&gp=0.jpg"
        }
    },
    "topk": 5
}'
```
