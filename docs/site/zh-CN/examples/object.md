# 物体搜索

本篇文章会使用物体识别和物体编码的两个模型搭建一个 Phantoscope Application，该应用能够提取图片中的物体（支持 MSCOCO 数据集的 90 个分类）并对检测出的实体进行相似度搜索。


## 样例场景
本文着重以 MSCOCO 数据集中支持的几种动物演示该场景的实际功能。

## 依赖要求
- 本文档仅在 Ubuntu 系统进行过测试
- 请先安装 Phantoscope
- docker >= 19.03
- docker-compose >= 1.25.0

## 使用到的模块
- **ssd-object-detector**
- **xception**
> 可以在 [Phantoscope Operators](https://github.com/zilliztech/phantoscope/blob/master/operators/README.md) 中找到这两个 Operator 的描述。

## 准备数据
下载需要的 MSCOCO 动物图片数据集并解压。该数据集约 174M, 下载耗时取决于网络环境。
```bash
$ curl http://cs231n.stanford.edu/coco-animals.zip -o /tmp/coco-animals.zip
$ unzip /tmp/coco-animals.zip -d /tmp/
```
> 如果想尝试比较大的数据集，可以使用完整的 MSCOCO 图片数据集替换。

## 创建 Phantoscope 应用
1.使用 ssd-object-detector 与 xception 的镜像创建对应的容器。第一次运行需要从 Dockerhub 拉取镜像，需要等待一段时间。
```bash
$ export LOCAL_ADDRESS=$(ip a | grep -Eo 'inet (addr:)?([0-9]*\.){3}[0-9]*' | grep -Eo '([0-9]*\.){3}[0-9]*' | grep -v '127.0.0.1'| head -n 1)
$ docker run -d -p 50010:50010 -e OP_ENDPOINT=${LOCAL_ADDRESS}:50010 psoperator/ssd-detector:latest
$ docker run -d -p 50011:50011 -e OP_ENDPOINT=${LOCAL_ADDRESS}:50011 psoperator/xception-encoder:latest
```

通过 ```docker ps``` 命令查看容器的运行状态,确保 Operator 服务正确启动，正确的运行结果如下图所示：
![result1](/.github/example/object-example1.png)

2.将 ssd-object-detector 与 xception 注册到 Phantoscope 中。
此过程需要以 Operator 暴露的服务端口和一个自定义的 Operator 名称构造请求。关于 Operator 的详细描述请参考 [什么是 Operator](https://github.com/zilliztech/phantoscope/blob/master/docs/site/zh-CN/tutorials/operator.md)。
```bash
# register ssd-object-detector to phantoscope with exposed 50010 port and a self-defined name 'ssd_detector'
$ curl --location --request POST '127.0.0.1:5000/v1/operator/regist' \
--header 'Content-Type: application/json' \
--data-raw '{
    "endpoint": "'${LOCAL_ADDRESS}':50010",
    "name": "ssd_detector"
}'
# register xception-encoder to phantoscope with exposed 50011 port and a self-defined name 'xception'
$ curl --location --request POST '127.0.0.1:5000/v1/operator/regist' \
--header 'Content-Type: application/json' \
--data-raw '{
    "endpoint": "'${LOCAL_ADDRESS}':50011",
    "name": "xception"
}'
```
如下图所示，正确的运行结果会返回对应 Operator 的信息：
![result2](/.github/example/object-example2.png)

3.创建一条包含 ssd_detector 和 xception 的 Pipeline。关于 Pipeline 的详细描述请参考 [什么是Pipeline](https://github.com/zilliztech/phantoscope/blob/master/docs/site/zh-CN/tutorials/pipeline.md)。
```bash
# create a pipeline with necessary information
$ curl --location --request POST '127.0.0.1:5000/v1/pipeline/object' \
--header 'Content-Type: application/json' \
--data-raw '{
	"input": "image",
	"description": "object detect and encode",
	"processors": "ssd_detector",
	"encoder": "xception",
	"indexFileSize": 1024
}'
```
如下图所示，创建成功后会返回 Pipeline 的详细信息：
![result3](/.github/example/object-example3.png)

4.以步骤3创建的 Pipeline 构建完整的 Phantoscope Application。关于 Application 的详细描述请参考 [什么是Application](https://github.com/zilliztech/phantoscope/blob/master/docs/site/zh-CN/tutorials/application.md)
```bash
# create an application with a self-define field name assocatied with pipeline created in step3 
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
如下图所示，创建成功后会返回 Application 的详细信息：
![result4](/.github/example/object-example4.png)

如果一切顺利地运行到这里，一个完整的 Phantoscope 应用就创建完成了，接下来将演示如何使用该应用。

## 使用 Phantoscaope 应用 

1.在创建完成的 Phantoscope 应用中上传准备好的数据。请先切换到 ```Phantoscope``` 目录以执行导入命令。我们使用该数据集的训练集进行上传，该训练集包含800张图片，在CPU环境、并行度为4的实验条件下大约耗时 xxxxx s，实际上传时间取决于机器性能及并行配置参数。

```bash
python3 scripts/load_data.py -d /tmp/coco-animals/train -a object-example -p object
```
等待运行结束后，会显示上传过程的结果汇总，以下是一次正确上传的结果图。如果没有在上传的图片中检测出符合的实体，会出现上传失败的报错。
![result5](/.github/example/object-example5.png)

> 如果使用 MSCOCO 的全数据，可参考上述命令修改上传目录即可。

2.图片上传结束后，我们就可以开始使用 Phantoscope 应用进行搜索啦。
```bash
$ curl --location --request POST '127.0.0.1:5000/v1/application/object-example/search' \
--header 'Content-Type: application/json' \
--data-raw '{
	"fields": {
        "object": {
            "url": "https://ss2.bdstatic.com/70cFvnSh_Q1YnxGkpoWK1HF6hhy/it/u=3506601383,2488554559&fm=26&gp=0.jpg"
        }
    },
    "topk": 10,
    "nprobe": 20
}'
```
运行上述命令即可通过 RESTful API 进行搜索，正确的结果如下图所示：

![result6](/.github/example/object-example6.png)

3.也许你会觉得 RESTful API 的结果展示并不直观。使用[Phantoscope Preview](https://github.com/zilliztech/phantoscope/blob/master/docs/site/zh-CN/tutorials/preview.md)接入 Phantoscope 可以更直观地进行搜索。使用 Preview 的演示效果如下图所示：

![result7](/.github/example/object-example7.gif)


