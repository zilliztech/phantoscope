# Omnisearch Quick Start
## Before you begin
Install Omnisearch
## Regist operators

    curl --location --request POST '127.0.0.1:5000/v1/operator/regist' \
    --header 'Content-Type: application/json' \
    --data-raw '{
	    "endpoint": "127.0.0.1:50001",
	    "name": "vgg_example"
    }'
## Create a pipeline

    curl --location --request POST '127.0.0.1:5000/v1/pipeline/vgg' \
    --header 'Content-Type: application/json' \
    --data-raw '{
    	"input": "image",
    	"description": "pipeline test",
    	"processors": "",
    	"encoder": "vgg_example",
    	"indexFileSize": 1024
    }'

## Create a application

    curl --location --request POST '127.0.0.1:5000/v1/application/example' \
    --header 'Content-Type: application/json' \
    --data-raw '{
    "fields":{
    	"full": {
    		"type": "object",
    		"pipeline": "vgg"
     	}
    },
    "s3Buckets": "example"
    }'

## Download image data

    curl http://www.vision.caltech.edu/Image_Datasets/Caltech256/256_ObjectCategories.tar -o /tmp/vgg-example.tar

## Upload image data
		tar xvf /tmp/vgg-example.tar
		python load_data.py
## Use application to search

    curl --location --request POST '127.0.0.1:5000/v1/application/example/search' \
    --header 'Content-Type: application/json' \
    --data-raw '{
    	"fields": {
            "full": {
                "url": "https://tse2-mm.cn.bing.net/th/id/OIP.C3pWPyFPhBMiBeWoncc24QHaCq?w=300&h=108&c=7&o=5&dpr=2&pid=1.7"
            }
        },
        "topk": 10,
        "nprobe": 20
    }'
