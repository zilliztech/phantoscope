# Phantoscope 快速开始
## 在开始之前
确定 Phantoscope 所有组件正常
```bash 
$ docker-compose ps
```

看到如下输出
```
Name                      Command               State                        Ports
----------------------------------------------------------------------------------------------------------------
phantoscope_api_1      /usr/bin/gunicorn3 -w 4 -b ...   Up      0.0.0.0:5000->5000/tcp
phantoscope_milvus_1   /var/lib/milvus/docker-ent ...   Up      0.0.0.0:19530->19530/tcp, 0.0.0.0:8080->8080/tcp
phantoscope_minio_1    /usr/bin/docker-entrypoint ...   Up      0.0.0.0:9000->9000/tcp
phantoscope_mysql_1    docker-entrypoint.sh mysqld      Up      0.0.0.0:3306->3306/tcp
phantoscope_vgg_1      python3 server.py                Up      0.0.0.0:50001->50001/tcp
```
即表示 phantoscope 正在运行

## 准备环境
```bash
$ chmod +x scripts/prepare.sh
$ ./scripts/prepare.sh
```

## 下载图片数据
```bash
$ curl http://www.vision.caltech.edu/Image_Datasets/Caltech256/256_ObjectCategories.tar -o /tmp/vgg-example.tar
```

## 上传图片数据
```bash
$ tar xvf /tmp/vgg-example.tar -C /tmp
$ python3 scripts/load_data.py -s 127.0.0.1:5000 -a example -p example -d /tmp/256_ObjectCategories
```
上传图片根据机器性能不同,时间会有差异。
> Phantoscope 因为传输协议限制，上传过大的图片会触发上传失败的报错。
## 使用 Preview 进行搜索
```bash
docker run -d -e API_URL=http://$LOCAL_ADDRESS:5000 -p 8000:80 phantoscope/preview:latest
```
![](../../../../.github/preview.gif)


## 使用 API 上传一张图片
``` bash
$ curl --location --request POST '127.0.0.1:5000/v1/application/example/upload' \
--header 'Content-Type: application/json' \
--data "{
    \"fields\": {
        \"example\": {
            \"url\": \"https://tse2-mm.cn.bing.net/th/id/OIP.C3pWPyFPhBMiBeWoncc24QHaCq?w=300&h=108&c=7&o=5&dpr=2&pid=1.7\"
        }
    },
    \"s3Buckets\": \"example\"
}"

```

在预期中会收到类似下方返回
```json
[
    {
        "_id": 1591585583689787000,
        "_app_name": "example",
        "_image_url": "http://host:9000/example/example-19ef9e9ba7f745dd90b2d9373c1aed56",
        "_fields": {
        "example": {
            "type": "object",
            "pipeline": "example"
            }
        }
    }
]
```

## 使用 API 进行搜索
```bash
$ curl --location --request POST '127.0.0.1:5000/v1/application/example/search' \
--header 'Content-Type: application/json' \
--data "{
    \"fields\": {
        \"example\": {
            \"url\": \"https://tse2-mm.cn.bing.net/th/id/OIP.C3pWPyFPhBMiBeWoncc24QHaCq?w=300&h=108&c=7&o=5&dpr=2&pid=1.7\"
        }
    },
    \"topk\": 10
}"
```

在预期中会收到类似下方返回
```json
[
    {
        "_id": "1591584893762549000",
        "_app_name": "example",
        "_image_url": "http://host:9000/example/example-b26e52aa65df4c23bbd848e98df1f0a3",
        "_fields": {
            "example": {
            "type": "object",
            "pipeline": "example"
            }
        }
    },
    ...
    {
        "_id": "1591584895837488000",
        "_app_name": "example",
        "_image_url": "http://host:9000/example/example-e53e7a233c814b7f825f7b58c2647501",
        "_fields": {
        "example": {
            "type": "object",
            "pipeline": "example"
            }
        }
    }
]
```
