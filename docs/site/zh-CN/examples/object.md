
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
在 Phantoscope 中注册 ssd-object-detector 与 xception-encoder 的信息
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

正确的运行结果会返回对应 Operator 的信息：
```bash
{"name": "ssd_detector", "addr": "psoperator/ssd-detector:latest", "author": "phantoscope", "version": "0.1.0", "type": "processor", "description": "detect object in input images", "runtime_client": "docker", "metadata": {"id": "392e6c41-f3d0-45dd-ae54-d39dae2e5415", "create_time": "2020-07-15 11:12:46.730796", "resource_type": "Operator", "state": "created"}}

{"name": "xception_encoder", "addr": "psoperator/xception-encoder:latest", "author": "phantoscope", "version": "0.1.0", "type": "encoder", "description": "embedding picture as vector", "runtime_client": "docker", "metadata": {"id": "9cd2ff3d-1901-4893-9d50-a9b012d5674b", "create_time": "2020-07-15 11:12:52.924378", "resource_type": "Operator", "state": "created"}}%
```

使用 Phantoscope runtime 接口根据 Opeator 信息以 docker container 的形式创建一个 Operator 实例。

```bash
$ curl --location --request POST ${LOCAL_ADDRESS}':5000/v1/operator/ssd_detector/instances/ssd_instance1' \
--header 'Content-Type: application/json' 
$ curl --location --request POST ${LOCAL_ADDRESS}':5000/v1/operator/xception_encoder/instances/xception_instance1' \
--header 'Content-Type: application/json'
```

查看容器的运行状态。
```bash
$ docker ps                                                                                            
CONTAINER ID        IMAGE                                       COMMAND                  CREATED             STATUS              PORTS                                                NAMES
694bba51b711        psoperator/xception-encoder:latest          "python3 server.py"      11 seconds ago      Up 10 seconds       0.0.0.0:32848->80/tcp                                phantoscope_xception_encoder_xception_instance1
7935fd491fab        psoperator/ssd-detector:latest              "python3 server.py"      20 seconds ago      Up 18 seconds       0.0.0.0:32847->80/tcp                                phantoscope_ssd_detector_ssd_instance1
385f9b06aeaf        phantoscope/api-server:49b82fe              "/usr/bin/gunicorn3 …"   3 minutes ago       Up 3 minutes        0.0.0.0:5000->5000/tcp                               omnisearch_api_1
dc51662b24b6        mongo                                       "docker-entrypoint.s…"   3 minutes ago       Up 3 minutes        0.0.0.0:27017->27017/tcp                             omnisearch_mongo_1
85f3b7d0aa2b        minio/minio:latest                          "/usr/bin/docker-ent…"   3 minutes ago       Up 3 minutes        0.0.0.0:9000->9000/tcp                               omnisearch_minio_1
b968dcf0ae8d        milvusdb/milvus:0.10.0-cpu-d061620-5f3c00   "/var/lib/milvus/doc…"   3 minutes ago       Up 3 minutes        0.0.0.0:19121->19121/tcp, 0.0.0.0:19530->19530/tcp   omnisearch_milvus_1
```

创建一条包含 ssd_detector 和 xception 的 Pipeline，因为 Operator 实例创建需要进行初始化，可能需要等待一段时间后服务初始化成功。

下面所列命令中 object_pipeline 是自定义的 Pipeline 名称，ssd-detector 和 xception 是组成 Pipeline 的 Operator 的名称。关于 Pipeline 的详细描述请参考 [什么是Pipeline](https://github.com/zilliztech/phantoscope/blob/master/docs/site/zh-CN/tutorials/pipeline.md)。
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
成功创建后会返回 Pipeline 的详细信息：
```bash
{"name": "object_pipeline", "input": null, "output": null, "processors": [{"operator": {"name": "ssd_detector", "addr": "psoperator/ssd-detector:latest", "author": "phantoscope", "version": "0.1.0", "type": "processor", "description": "detect object in input images", "runtime_client": "docker", "metadata": {"id": "392e6c41-f3d0-45dd-ae54-d39dae2e5415", "create_time": "2020-07-15 11:12:46.730796", "resource_type": "Operator", "state": "created"}}, "instance": {"id": "7935fd491f", "name": "phantoscope_ssd_detector_ssd_instance1", "status": "running", "ports": {"80/tcp": [{"HostIp": "0.0.0.0", "HostPort": "32847"}]}, "ip": "192.168.128.6", "endpoint": "192.168.128.6:80"}}], "encoder": {"operator": {"name": "xception_encoder", "addr": "psoperator/xception-encoder:latest", "author": "phantoscope", "version": "0.1.0", "type": "encoder", "description": "embedding picture as vector", "runtime_client": "docker", "metadata": {"id": "9cd2ff3d-1901-4893-9d50-a9b012d5674b", "create_time": "2020-07-15 11:12:52.924378", "resource_type": "Operator", "state": "created"}}, "instance": {"id": "694bba51b7", "name": "phantoscope_xception_encoder_xception_instance1", "status": "running", "ports": {"80/tcp": [{"HostIp": "0.0.0.0", "HostPort": "32848"}]}, "ip": "192.168.128.7", "endpoint": "192.168.128.7:80"}}, "description": "object detect and encode", "metadata": {"id": "9e1ef80a-8ba0-4160-a92a-c504da8f7432", "create_time": "2020-07-15 11:14:29.178369", "resource_type": "Pipeline", "state": "created"}}%
```

以 object_pipeline 构建一个 Phantoscope Application。

下面所列命令中 object_example 是自定义 Application 的名称，object_field 是自定义的字段名称，保存着 object_pipeline 处理后的结果，同时将图片存储在名为 object-s3 的 S3 bucket 中。关于 Application 的详细描述请参考 [什么是Application](https://github.com/zilliztech/phantoscope/blob/master/docs/site/zh-CN/tutorials/application.md)。
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
成功创建后会返回 Application 的详细信息：
```bash
{"name": "object_example", "fields": {"object_field": {"type": "pipeline", "value": "object_pipeline"}}, "bucket": "object-s3", "metadata": {"id": "cc389045-0bc1-4c08-8256-9ee806659907", "create_time": "2020-07-15 11:14:47.445727", "resource_type": "Application", "state": "created"}}%
```

如果运行到这里一切顺利，代表着已经成功创建了一个完整的 Phantoscope Application，接下来将演示如何使用。

## 使用 Phantoscope Application 

### 导入图片
在创建完成的 Phantoscope Application 中上传准备好的数据。请先切换到 ```Phantoscope``` 目录以执行导入脚本。我们使用准备好的 COCO 动物训练集进行上传，约耗时 196 s。

```bash
$ pip3 install requests tqdm
$ python3 scripts/load_data.py -d /tmp/coco-animals/train -a object_example -p object_pipeline
```
等待运行结束，上传结果如下所示。
```bash
upload url is http://127.0.0.1:5000/v1/application/object_example/upload
allocate 4 processes to load data, each task including 200 images
Now begin to load image data and upload to phantoscope: ...
100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 800/800 [03:57<00:00,  3.36it/s]
upload 800 images cost: 238.023s
All images has been uploaded: success 754, fail 46
Please read file '/path/to/phantoscope/scripts/upload_error.log' to check upload_error log.
```
> 如果没有在导入的图片中检测出符合的物体，会触发导入失败的报错。
### 搜索图片
图片导入结束，使用 Phantoscope Application 进行搜索。

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
运行上述命令通过 RESTful API 进行搜索, 会得到最相似的 3 个记录，正确的结果经过 json 格式化如下所示：

```json
[
    {
        "_id":"5f0ee6586fd2613c5dba8df3",
        "_docs":{
            "object_field":{
                "ids":[
                    1594811992054104000,
                    1594811992054104000
                ],
                "url":"http://192.168.1.192:9000/object-s3/object_example-964e0d00f6f74d4c954a8b1169ef1a54"
            }
        }
    },
    {
        "_id":"5f0ee6585504b60e17e871da",
        "_docs":{
            "object_field":{
                "ids":[
                    1594811992742535000
                ],
                "url":"http://192.168.1.192:9000/object-s3/object_example-6eb439958ad140c2ac30a81f22541f40"
            }
        }
    },
    {
        "_id":"5f0ee65a3bb092d03977675e",
        "_docs":{
            "object_field":{
                "ids":[
                    1594811994145456000,
                    1594811994145456000,
                    1594811994145456000
                ],
                "url":"http://192.168.1.192:9000/object-s3/object_example-234d0939b00f4d9ba4411b64eb8ee7aa"
            }
        }
    }
]
```

3.使用 [Phantoscope Preview](https://github.com/zilliztech/phantoscope/blob/master/docs/site/zh-CN/tutorials/preview.md) 更直观地进行搜索。演示效果如下图所示：
>  注意切换为 object_example 的 application。
![result](https://live.staticflickr.com/65535/50140138427_45c3193fd8_o.gif)

> 本文所使用 API 详见 [API 文档](https://app.swaggerhub.com/apis-docs/phantoscope/Phantoscope/0.2.0)。
