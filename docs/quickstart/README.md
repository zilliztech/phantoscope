# Omnisearch Quick Start
## Before you begin
make sure omnisearch is running
## Run operators

    docker-compose up -d 
## Regist operators
    
    curl --location --request POST '{{addr}}:5000/v1/operator/regist' \
    --data-raw '{
	    "endpoint": "192.168.1.10:50010",
	    "name": "face-detector"
    }'
    
    curl --location --request POST '{{addr}}:5000/v1/operator/regist' \
    --data-raw '{
	    "endpoint": "192.168.1.10:50011",
	    "name": "face-embedding"
	}'
## Create a pipeline

	curl --location --request POST '{{addr}}:5000/v1/pipeline/face' \
	--data-raw '{
	"input": "image",
	"description": "This is face detect pipeline",
	"processors": "face-detector",
	"encoder": "face-embedding",
	"indexFileSize":1024
	}'
## Create a application

	curl --location --request POST '{{addr}}:5000/v1/application/human' \
	--data-raw '{
	"fields":{
		"name":{
			"type": "string",
			"value": ""
		},
		"leight": {
			"type": "int",
			"value": 0
		},
		"face": {
			"type": "object",
			"pipeline": "face"
	 		}
 		
		},
	"s3Buckets": "app2"
	}'
## Download image data(Optional)
## Use application to upload

	curl --location --request POST '{{addr}}:5000/v1/application/app2/upload' \
	--data-raw '{
		"fields":{
			"name":{
				"value": "mike"
			},
			"leight":{
				"value": 196
			},
			"face": {
				"url": "image url"
			}
		},
		"targetFields":{
			"data": "base64 image data"
		}
## Use application to search

	curl --location --request POST '{{addr}}:5000/v1/application/app2/search' \
	--data-raw '{
		"topk": 10,
		"nprobe": 16,
		"fields":{
	 		"face": {
	 			"url": "imageurl"
	 		}
		}
	}'
