# Phantoscope Quick Start
## Prerequisites
Ensure that all modules of Phantoscope are running properly: 

```bash 
$ docker-compose ps
```

*If you see the following output, Phantoscope is running properly.*
```
Name                      Command               State                        Ports
----------------------------------------------------------------------------------------------------------------
phantoscope_api_1      /usr/bin/gunicorn3 -w 4 -b ...   Up      0.0.0.0:5000->5000/tcp
phantoscope_milvus_1   /var/lib/milvus/docker-ent ...   Up      0.0.0.0:19530->19530/tcp, 0.0.0.0:8080->8080/tcp
phantoscope_minio_1    /usr/bin/docker-entrypoint ...   Up      0.0.0.0:9000->9000/tcp
phantoscope_mysql_1    docker-entrypoint.sh mysqld      Up      0.0.0.0:3306->3306/tcp
phantoscope_vgg_1      python3 server.py                Up      0.0.0.0:50001->50001/tcp
```

## Prepare Your Environment

Run **prepare.sh** under the **script** folder. This script register an operator, use it to create a pipeline, and then use the pipeline to create an application called **example_app**. 

```bash
$ chmod +x prepare.sh
$ ./prepare.sh
```

## Download Image Package
```bash
$ curl http://www.vision.caltech.edu/Image_Datasets/Caltech256/256_ObjectCategories.tar -o /tmp/vgg-example.tar
``` 

## Upload Image Package
```bash
$ tar xvf /tmp/vgg-example.tar -C /tmp
$ pip3 install requests tqdm
$ python3 scripts/load_data.py -s $LOCAL_ADDRESS:5000 -a example_app -p example_pipeline -d /tmp/256_ObjectCategories
```

## Use Phantoscope Preview for an image search
```bash
docker run -d -e API_URL=http://$LOCAL_ADDRESS:5000 -p 8000:80 phantoscope/preview:latest
```
Open $LOCAL_ADDRESS:5000 with browser

![Phantoscope Preview Demonstration](../../../../.github/preview.gif)


## Use curl to import an image

Run the following command to import an image:

``` bash
$ curl --location --request POST $LOCAL_ADDRESS':5000/v1/application/example_app/upload' \
--header 'Content-Type: application/json' \
--data "{
    \"fields\": {
        \"example_field\": {
            \"url\": \"https://tse2-mm.cn.bing.net/th/id/OIP.C3pWPyFPhBMiBeWoncc24QHaCq?w=300&h=108&c=7&o=5&dpr=2&pid=1.7\"
        }
    }
}"

```

*You are expected to see the following response:*
```json
[
    {
        "_id": 1591585583689787000,
        "_app_name": "example_app",
        "_image_url": "http://host:9000/example/example-19ef9e9ba7f745dd90b2d9373c1aed56",
        "_fields": {
            "example_field": {
                "type": "object",
                "pipeline": "example_pipeline"
            }
        }
    }
]
```

## Use curl for an image search
```bash
$ curl --location --request POST $LOCAL_ADDRESS':5000/v1/application/example_app/search' \
--header 'Content-Type: application/json' \
--data "{
    \"fields\": {
        \"example_field\": {
            \"url\": \"https://tse2-mm.cn.bing.net/th/id/OIP.C3pWPyFPhBMiBeWoncc24QHaCq?w=300&h=108&c=7&o=5&dpr=2&pid=1.7\"
        }
    },
    \"topk\": 2
}"
```

*You are expected to see the following response:*
```json
[
    {
        "_id": "1591584893762549000",
        "_app_name": "example_app",
        "_image_url": "http://host:9000/example/example-b26e52aa65df4c23bbd848e98df1f0a3",
        "_fields": {
            "example_field": {
                "type": "object",
                "pipeline": "example_pipeline"
            }
        }
    },
    {
        "_id": "1591584895837488000",
        "_app_name": "example_app",
        "_image_url": "http://host:9000/example/example-e53e7a233c814b7f825f7b58c2647501",
        "_fields": {
            "example_field": {
                "type": "object",
                "pipeline": "example_pipeline"
            }
        }
    }
]
```
