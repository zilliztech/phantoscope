# 人脸搜索

##  样例场景
检测图片中的人脸并进行搜索，可以用于人脸识别并进行对比的实际场景，如打卡机等。

## 依赖要求
- 本文档仅在 Ubuntu 系统进行过测试
- 请先安装 Phantoscope
- docker >= 19.03
- docker-compose >= 1.25.0

##  使用到的模块
- **MTCNN-face-detector**  
- **face embedding**  
> 可以在 [Phantoscope operators](https://github.com/zilliztech/phantoscope/blob/master/operators/README.md) 中找到这两个 Operator 的描述。

##  准备数据
下载包含人脸的实验数据，该数据集约1.9G, 耗时取决于网络环境。

```bash
curl http://host.robots.ox.ac.uk/pascal/VOC/voc2012/VOCtrainval_11-May-2012.tar -o /tmp/VOCtrainval_11-May-2012.tar
```
> 注意该数据并不是人脸数据集，包含很多没有人脸信息的无效图片，会在实际导入过程中引发上传失败警告。

## 开始
1.使用 face-embedding 与 mtcnn-face-detector 的镜像创建对应的容器。如果是第一次运行需要从 dockerhub 拉取镜像，需要等待一段时间。
```bash
export LOCAL_ADDRESS=$(ip a | grep -Eo 'inet (addr:)?([0-9]*\.){3}[0-9]*' | grep -Eo '([0-9]*\.){3}[0-9]*' | grep -v '127.0.0.1'| head -n 1)
docker run -d -p 50004:50004 -e OP_ENDPOINT=${LOCAL_ADDRESS}:50004 psoperator/face-encoder:latest
docker run -d -p 50005:50005 -e OP_ENDPOINT=${LOCAL_ADDRESS}:50005 psoperator/face-detector:latest
```
通过 ```docker ps``` 命令查看容器的运行状态以确定是否正确启动 Operator 服务，正确的运行结果如下图所示：
![result1](/.github/example/face-example1.png)

2.将 face-embedding 与 mtcnn-face-detector 注册到 Phantoscope 中。此过程需要以 Operator 暴露的服务端口和一个自定义的 Operator 名称构造请求。
关于 Operator 的详细描述请参考 [什么是Operator](https://github.com/zilliztech/phantoscope/blob/master/docs/site/zh-CN/tutorials/operator.md)。
```bash
curl --location --request POST '127.0.0.1:5000/v1/operator/regist' \
--header 'Content-Type: application/json' \
--data-raw '{
    "endpoint": "'${LOCAL_ADDRESS}':50004",
    "name": "face_embedding"
}'
	
curl --location --request POST '127.0.0.1:5000/v1/operator/regist' \
--header 'Content-Type: application/json' \
--data-raw '{
    "endpoint": "'${LOCAL_ADDRESS}':50005",
    "name": "mtcnn_face_detector"
}'
```
如下图所示，正确的运行结果会返回对应 Operator 的信息：
![result2](/.github/example/face-example2.png)

3.创建一条 pipeline 用于提取人脸并将数据转化为向量，此 pipeline 包含了步骤二注册的两个 Operator。关于 pipeline 的详细描述请参考 [Pipeline101]()
```bash
curl --location --request POST '127.0.0.1:5000/v1/pipeline/face' \
--header 'Content-Type: application/json' \
--data-raw '{
	"input": "image",
	"description": "face detect and encode",
	"processors": "mtcnn_face_detector",
	"encoder": "face_embedding",
	"indexFileSize": 1024
}'
```
如下图所示，创建成功后会返回 Pipeline 的详细信息：
![result3](/.github/example/face-example3.png)

4.创建一个包含步骤三的 pipeline 的  application 用于构建完整的 Phantoscope 应用。关于 application 的详细描述请参考 [Application101]()
```bash
curl --location --request POST '127.0.0.1:5000/v1/application/face-example' \
--header 'Content-Type: application/json' \
--data-raw '{
    "fields":{
        "face": {
            "type": "object",
            "pipeline": "face"
        }
    },
    "s3Buckets": "face"
}'
```
如下图所示，创建成功后会返回 Application 的详细信息：：
![result4](/.github/example/face-example4.png)

如果一切顺利地运行到这里，一个完整的 Phantoscope 应用就创建完成了，接下来将演示如何使用该应用。

5.在创建完成的 Phantoscope 应用中上传准备好的数据。因为该数据集包含1万多图片，此过程会比较耗时，在CPU环境、并行度为4的实验条件下大约耗时xxx s，实际上传时间可能因为机器性能差别而存在差异。
```bash
tar xvf /tmp/VOCtrainval_11-May-2012.tar -C /tmp
python3 load_data.py -d /tmp/VOCdevkit/ -a face-example -p face
```
等待运行结束后，脚本会列出上传过程的结果汇总，以下是一次正确上传的结果汇总图。如果没有在上传的图片中检测出符合的实体，会产生上传
![result5](/.github/example/face-example5.png)
> 如果仅仅试用，可以选用自定义的数据集或者只上传一部分图片。

6.步骤5图片上传结束后，我们就可以开始使用该 Phantoscope 应用进行搜索啦。
```bash
curl --location --request POST '127.0.0.1:5000/v1/application/face-example/search' \
--header 'Content-Type: application/json' \
--data-raw '{
	"fields": {
        "face": {
            "url": "https://tse2-mm.cn.bing.net/th/id/OIP.d0Uth461I3nJDr28WXudhgHaHa?w=204&h=189&c=7&o=5&dpr=2&pid=1.7"
        }
    },
    "topk": 10,
    "nprobe": 20
}'
```
运行上述命令通过 RESTful API 进行搜索，如下图所示，运行该命令返回了10条搜索结果。

![result6](/.github/example/face-example6.png)

RESTful API 的结果展示并不直观，可以使用[Phantoscope Preview](https://github.com/zilliztech/phantoscope/blob/master/docs/site/zh-CN/tutorials/preview.md)接入 Phantoscope 进行搜索。
下图是演示的结果图：
![result7](/.github/example/face-example7.png)

