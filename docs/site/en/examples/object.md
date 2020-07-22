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
1. Register **ssd-object-detector** and **xception** as Phantoscope Operator. 

```bash
$ export LOCAL_ADDRESS=$(ip a | grep -Eo 'inet (addr:)?([0-9]*\.){3}[0-9]*' | grep -Eo '([0-9]*\.){3}[0-9]*' | grep -v '127.0.0.1'| head -n 1)
$ curl --location --request POST ${LOCAL_ADDRESS}':5000/v1/operator/register' \
--header 'Content-Type: application/json' \
--data '{
    "name": "ssd_detector",
    "addr": "psoperator/ssd-detector:latest",
    "author" :"phantoscope",
    "type":"processor",
    "description": "detect object in input images",
    "version": "0.1.0"
}'
$ curl --location --request POST ${LOCAL_ADDRESS}':5000/v1/operator/register' \
--header 'Content-Type: application/json' \
--data '{
    "name": "xception_encoder",
    "addr": "psoperator/xception-encoder:latest",
    "author" :"phantoscope",
    "type":"encoder",
    "description": "embedding picture as vector",
    "version": "0.1.0"
}'
```

2. Create **ssd-object-detector** and **xception** Operator instance. 

```bash
$ curl --location --request POST ${LOCAL_ADDRESS}':5000/v1/operator/ssd_detector/instances/ssd_instance1' \
--header 'Content-Type: application/json' 
$ curl --location --request POST ${LOCAL_ADDRESS}':5000/v1/operator/xception_encoder/instances/xception_instance1' \
--header 'Content-Type: application/json'
```

3. Create a pipeline for extracting object and converting it to vector. 

```bash
# create a pipeline with necessary information
$ curl --location --request POST ${LOCAL_ADDRESS}':5000/v1/pipeline/object_pipeline' \
--header 'Content-Type: application/json' \
--data '{
	"description":"object detect and encode",
	"processors": [{
		"name": "ssd_detector",
		"instance":"ssd_instance1"
	}],
	"encoder": {
		"name": "xception_encoder",
		"instance":"xception_instance1"
	}
}'
```
4. Create an application for running the pipeline.

```bash
# create an application with a self-define field name assocatied with pipeline created in step3 
$ curl --location --request POST ${LOCAL_ADDRESS}':5000/v1/application/object_example' \
--header 'Content-Type: application/json' \
--data '{
    "fields":{
        "object_field": {
            "type": "pipeline",
            "value": "object_pipeline"
        }
    },
    "s3Bucket": "object-s3"
}'
```
5. Upload the package you have downloaded. 

```bash
$ pip3 install requests tqdm
$ python3 scripts/load_data.py -d /tmp/coco-animals/train -a object_example -p object_pipeline
```

6. Conduct an object search. 

```bash
$ curl --location --request POST ${LOCAL_ADDRESS}':5000/v1/application/object_example/search' \
--header 'Content-Type: application/json' \
--data '{
	"fields": {
        "object_field": {
            "url": "https://ss2.bdstatic.com/70cFvnSh_Q1YnxGkpoWK1HF6hhy/it/u=3506601383,2488554559&fm=26&gp=0.jpg"
        }
    },
    "topk": 3
}'
```
