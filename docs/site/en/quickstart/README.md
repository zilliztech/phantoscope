# Phantoscope Quick Start
## Prerequisites
Ensure that all modules of Phantoscope are running properly: 

```bash
$ docker-compose ps
```

*If you see the following output, Phantoscope is running properly.*
```bash
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
$ chmod +x scripts/prepare.sh
$ ./scripts/prepare.sh
```

## Download Image Package
```bash
$ curl http://cs231n.stanford.edu/coco-animals.zip -o /tmp/coco-animals.zip
```

## Upload Image Package
```bash
$ unzip /tmp/coco-animals.zip -d /tmp/
$ pip3 install requests tqdm
$ python3 scripts/load_data.py -s $LOCAL_ADDRESS:5000 -a example_app -p example_pipeline -d /tmp/coco-animals
```

## Use Phantoscope Preview for an image search
```bash
$ docker run -d -e API_URL=http://$LOCAL_ADDRESS:5000 -p 8000:80 phantoscope/preview:0.2.0
```
Open 127.0.0.1:8000 with browser

![Phantoscope Preview Demonstration](../../../../.github/preview.gif)


## Use curl to import an image

Run the following command to import an image:

```bash
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
        "_id":"5f103b21f92bc0c90cc7f737",
        "_docs":{
            "example_field":{
                "ids":[
                    1594899233036739000
                ],
                "url":"http://192.168.1.192:9000/example-s3/example_app-33c5bf6ce2a0482593993140e83a6481"
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
        "_id":"5f103b21f92bc0c90cc7f737",
        "_docs":{
            "example_field":{
                "ids":[
                    1594899233036739000
                ],
                "url":"http://192.168.1.192:9000/example-s3/example_app-33c5bf6ce2a0482593993140e83a6481"
            }
        }
    },
    {
        "_id":"5f103b9faf56a7d8833f5597",
        "_docs":{
            "example_field":{
                "ids":[
                    1594899359173444000
                ],
                "url":"http://192.168.1.192:9000/example-s3/example_app-b20d796e8cda4a539201557bd418a89f"
            }
        }
    }
]
```
