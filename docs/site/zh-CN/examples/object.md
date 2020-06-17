
# 创建 Appication

本篇文章会使用 [ssd-object-detector](../tutorials/operator.md#ssd-object-detector) 和 [xception-encoder](../tutorials/operator.md#xception) 两个 Operator 创建一个 Phantoscope Application，用于检测图片中的物体（支持 MSCOCO 数据集的 90 个分类）并对检测出的物体进行相似度搜索。

> 本文所有命令仅在 Ubuntu 18.04 系统进行测试
## 目录
- [样例场景](#样例场景)
- [使用到的模块](#使用到的模块)
- [准备数据](#准备数据)
- [创建 Phantoscope Application](#创建-phantoscope-application)
- [使用 Phantoscope Application](#使用-phantoscope-application)


## 样例场景
本文着重以 MSCOCO 数据集中支持的几种动物为例演示场景。

## 使用到的模块
- ssd-object-detector
- xception-encoder
> 可以在 [Phantoscope Operators](https://github.com/zilliztech/phantoscope/blob/master/operators/README.md) 中找到这两个 Operator 的描述。

## 准备数据
下载 MSCOCO 动物图片数据集并解压。该数据集约 174M, 下载耗时取决于网络环境。
```bash
$ curl http://cs231n.stanford.edu/coco-animals.zip -o /tmp/coco-animals.zip
$ unzip /tmp/coco-animals.zip -d /tmp/
```
> 尝试更大的数据集？使用完整的 MSCOCO 图片数据集替换数据路径。

## 创建 Phantoscope Application
使用 ssd-object-detector 与 xception-encoder 的镜像创建容器。第一次运行会从 Dockerhub 拉取镜像，需要等待一段时间。
```bash
$ export LOCAL_ADDRESS=$(ip a | grep -Eo 'inet (addr:)?([0-9]*\.){3}[0-9]*' | grep -Eo '([0-9]*\.){3}[0-9]*' | grep -v '127.0.0.1'| head -n 1)
$ docker run -d -p 50010:50010 -e OP_ENDPOINT=${LOCAL_ADDRESS}:50010 psoperator/ssd-detector:latest
$ docker run -d -p 50011:50011 -e OP_ENDPOINT=${LOCAL_ADDRESS}:50011 psoperator/xception-encoder:latest
```

查看容器的运行状态。
```bash
$ docker ps                                                                                            
CONTAINER ID        IMAGE                                      COMMAND                  CREATED             STATUS              PORTS                                              NAMES
05e666f48f5f        psoperator/xception-encoder:latest         "python3 server.py"      9 seconds ago       Up 9 seconds        0.0.0.0:50011->50011/tcp, 50012/tcp                happy_ellis
c4dd13b3fc5d        psoperator/ssd-detector:latest             "python3 server.py"      15 seconds ago      Up 14 seconds       0.0.0.0:50010->50010/tcp, 51002/tcp                keen_leavitt
09bd2658493b        psoperator/vgg16:latest                    "python3 server.py"      23 seconds ago      Up 22 seconds       0.0.0.0:50001->50001/tcp                           omnisearch_vgg_1
0ce974dc8891        phantoscope/api-server:0.1.0               "/usr/bin/gunicorn3 …"   23 seconds ago      Up 22 seconds       0.0.0.0:5000->5000/tcp                             omnisearch_api_1
3bf49c362d79        daocloud.io/library/mysql:5.6              "docker-entrypoint.s…"   26 seconds ago      Up 24 seconds       0.0.0.0:3306->3306/tcp                             omnisearch_mysql_1
3f6f6750bc21        milvusdb/milvus:0.7.0-cpu-d031120-de409b   "/var/lib/milvus/doc…"   26 seconds ago      Up 23 seconds       0.0.0.0:8080->8080/tcp, 0.0.0.0:19530->19530/tcp   omnisearch_milvus_1
f5e387c6016b        minio/minio:latest                         "/usr/bin/docker-ent…"   26 seconds ago      Up 24 seconds       0.0.0.0:9000->9000/tcp                             omnisearch_minio_1
bedc9420d6d5        phantoscope/preview:latest                 "/bin/bash -c '/usr/…"   40 minutes ago      Up 40 minutes       0.0.0.0:8000->80/tcp                               brave_ellis
```

将 ssd-object-detector 与 xception-encoder 注册到 Phantoscope 中。

此过程需要以 Operator 暴露的服务端口和自定义的 Operator 名称构造请求。下面所列命令中，50010 和 50011 分别是两个 Operator 暴露的端口， ssd_detector 和 xception 为自定义的 Opertaor 名称。关于 Operator 的详细描述请参考 [什么是 Operator](https://github.com/zilliztech/phantoscope/blob/master/docs/site/zh-CN/tutorials/operator.md)。
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
正确的运行结果会返回对应 Operator 的信息：
```bash
{"_name": "ssd_detector", "_backend": "ssd", "_type": "processor", "_input": "image", "_output": "images", "_endpoint": "192.168.1.192:50010", "_metric_type": "-1", "_dimension": -1}%  

{"_name": "xception", "_backend": "xception", "_type": "encoder", "_input": "image", "_output": "vector", "_endpoint": "192.168.1.192:50011", "_metric_type": "L2", "_dimension": 2048}% 
```

创建一条包含 ssd_detector 和 xception 的 Pipeline。

下面所列命令中 object_pipeline 是自定义的 Pipeline 名称，ssd-detector 和 xception 是组成 Pipeline 的 Operator 的名称。关于 Pipeline 的详细描述请参考 [什么是Pipeline](https://github.com/zilliztech/phantoscope/blob/master/docs/site/zh-CN/tutorials/pipeline.md)。
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
成功创建后会返回 Pipeline 的详细信息：
```bash
{"_pipeline_name": "object_pipeline", "_input": "image", "_output": "vector", "_dimension": 2048, "_index_file_size": 1024, "_metric_type": "L2", "_pipeline_description": "object detect and encode", "_processors": ["ssd_detector"], "_encoder": "xception", "_description": "object detect and encode"}%
```

以 object_pipeline 构建一个 Phantoscope Application。

下面所列命令中 object-example 是自定义 Application 的名称，object_field 是自定义的字段名称，保存着 object_pipeline 处理后的结果，同时将图片存储在名为 object-s3 的 S3 bucket 中。关于 Application 的详细描述请参考 [什么是Application](https://github.com/zilliztech/phantoscope/blob/master/docs/site/zh-CN/tutorials/application.md)。
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
成功创建后会返回 Application 的详细信息：
```bash
{"_application_name": "object-example", "_fields": {"object_field": {"type": "object", "pipeline": "object_pipeline"}}, "_buckets": "object-s3"}%  
```

如果运行到这里一切顺利，代表着已经成功创建了一个完整的 Phantoscope Application，接下来将演示如何使用。

## 使用 Phantoscope Application 

### 导入图片
在创建完成的 Phantoscope Application 中上传准备好的数据。请先切换到 ```Phantoscope``` 目录以执行导入脚本。我们使用准备好的 COCO 动物训练集进行上传，约耗时 196 s。

```bash
$ pip3 install requests tqdm
$ python3 scripts/load_data.py -d /tmp/coco-animals/train -a object-example -p object_pipeline
```
等待运行结束，上传结果如下所示。
```bash
upload url is http://127.0.0.1:5000/v1/application/object-example/upload
allocate 4 processes to load data, each task including 200 images
Now begin to load image data and upload to phantoscope: ...
100%|████████████████████████████████████████████████████████████████████████████████| 800/800 [03:16<00:00,  4.07it/s]
upload 800 images cost: 196.832s 
All images has been uploaded: success 754, fail 46
Please read file 'path_to_error_log' to check upload_error log.
```
> 如果没有在导入的图片中检测出符合的物体，会触发导入失败的报错。
### 搜索图片
图片导入结束，使用 Phantoscope Application 进行搜索。

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
运行上述命令通过 RESTful API 进行搜索, 会得到最相似的 5 个记录，正确的结果经过 json 格式化如下所示：

```json
[
    {
        "_id": "1591788614578665000",
        "_app_name": "object-example",
        "_image_url": "http://192.168.1.192:9000/object-s3/object-example-efb4be8a38ac4297a1be1e9d589397f4",
        "_fields": {
            "object_field": {
                "type": "object",
                "pipeline": "object_pipeline"
            }
        }
    },
    {
        "_id": "1591788654504043000",
        "_app_name": "object-example",
        "_image_url": "http://192.168.1.192:9000/object-s3/object-example-5a3644c89da74ce28c2f42949180e066",
        "_fields": {
            "object_field": {
                "type": "object",
                "pipeline": "object_pipeline"
            }
        }
    },
    {
        "_id": "1591788654504043001",
        "_app_name": "object-example",
        "_image_url": "http://192.168.1.192:9000/object-s3/object-example-5a3644c89da74ce28c2f42949180e066",
        "_fields": {
            "object_field": {
                "type": "object",
                "pipeline": "object_pipeline"
            }
        }
    },
    {
        "_id": "1591788635868801000",
        "_app_name": "object-example",
        "_image_url": "http://192.168.1.192:9000/object-s3/object-example-2520010f066e4f9093d85f329d045fe4",
        "_fields": {
            "object_field": {
                "type": "object",
                "pipeline": "object_pipeline"
            }
        }
    },
    {
        "_id": "1591788680008488000",
        "_app_name": "object-example",
        "_image_url": "http://192.168.1.192:9000/object-s3/object-example-e2891d3d5252476cbe874e9d5239d3d6",
        "_fields": {
            "object_field": {
                "type": "object",
                "pipeline": "object_pipeline"
            }
        }
    }
]
```

3.使用 [Phantoscope Preview](https://github.com/zilliztech/phantoscope/blob/master/docs/site/zh-CN/tutorials/preview.md) 更直观地进行搜索。演示效果如下图所示：

![result](/.github/example/object-example.gif)

> 本文所使用 API 详见 [API 文档](https://app.swaggerhub.com/apis-docs/phantoscope/Phantoscope/0.1.0)。
