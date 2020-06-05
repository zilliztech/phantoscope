# 物体搜索

##  样例场景
提取图片中的物体（支持 MSCOCO）并进行搜索。

##  使用到的模块
- **ssd-object-detector**
- **xception**
> 可以在 [Phantoscope Operators](https://github.com/zilliztech/phantoscope/blob/master/operators/README.md) 中找到这两个 operator 的描述。

##  准备数据
下载包含物体的实验数据。
```bash
curl http://www.vision.caltech.edu/Image_Datasets/Caltech256/256_ObjectCategories.tar -o /tmp/256-object.tar
```

## 开始 
1.使用 ssd-object-detector 与 xception 的镜像创建对应的容器。如果是第一次运行需要从 dockerhub 拉取镜像，需要等待一段时间。
```bash
export LOCAL_ADDRESS=$(ip a | grep -Eo 'inet (addr:)?([0-9]*\.){3}[0-9]*' | grep -Eo '([0-9]*\.){3}[0-9]*' | grep -v '127.0.0.1'| head -n 1)
docker run -d -p 50010:50010 -e OP_ENDPOINT=${LOCAL_ADDRESS}:50010 psoperator/ssd-detector:latest
docker run -d -p 50011:50011 -e OP_ENDPOINT=${LOCAL_ADDRESS}:50011 psoperator/xception-encoder:latest
```
通过```docker ps``` 命令查看容器状态可以看到两个容器都启动成功
![result1](/.github/example/object-example1.png)

2.将 ssd-object-detector 与 xception 作为 Operator 注册到 Phantoscope 中。此过程所需要提供的仅仅是 Operator 暴露的服务端口和一个自定义的 Operator 名称。
关于 Operator 的详细描述请参考 [什么是Operator](https://github.com/zilliztech/phantoscope/blob/master/docs/site/zh-CN/tutorials/operator.md)
```bash
# register ssd-object-detector to phantoscope with exposed 50010 port and a self-defined name 'ssd_detector'
curl --location --request POST '127.0.0.1:5000/v1/operator/regist' \
--header 'Content-Type: application/json' \
--data-raw '{
    "endpoint": "'${LOCAL_ADDRESS}':50010",
    "name": "ssd_detector"
}'
# register xception-encoder to phantoscope with exposed 50011 port and a self-defined name 'xception'
curl --location --request POST '127.0.0.1:5000/v1/operator/regist' \
--header 'Content-Type: application/json' \
--data-raw '{
    "endpoint": "'${LOCAL_ADDRESS}':50011",
    "name": "xception"
}'
```
运行上面两条命令，运行结果如下图所示
![result2](/.github/example/object-example2.png)

3.创建一条 pipeline 用于提取物体并将数据转化为向量，此 pipeline 包含了步骤二注册的两个 Operator。关于 pipeline 的详细描述请参考 [什么是Pipeline](https://github.com/zilliztech/phantoscope/blob/master/docs/site/zh-CN/tutorials/pipeline.md)
```bash
# create a pipeline with necessary information
curl --location --request POST '127.0.0.1:5000/v1/pipeline/object' \
--header 'Content-Type: application/json' \
--data-raw '{
	"input": "image",
	"description": "object detect and encode",
	"processors": "ssd_detector",
	"encoder": "xception",
	"indexFileSize": 1024
}'
```
运行上述命令结果如下图所示
![result3](/.github/example/object-example3.png)

4.创建一个包含步骤三的 pipeline 的 application 用于构建完整的 Phantoscope 应用。关于 application 的详细描述请参考 [什么是Application](https://github.com/zilliztech/phantoscope/blob/master/docs/site/zh-CN/tutorials/application.md)
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
运行上述创建 application 的命令，正确结果如下图所示
![result4](/.github/example/object-example4.png)

5.在创建完成的 Phantoscope 应用中上传准备好的数据。因为该数据集包含3万多图片，此过程会比较耗时，在CPU环境、并行度为4的实验条件下大约耗时 4083.240s
 s，实际上传时间可能因为机器性能差别而存在差异。

```bash
tar xvf /tmp/256-object.tar -C /tmp
python3 load_data.py -d /tmp/256_ObjectCategories -a object-example -p object
```
![result5](/.github/example/object-example5.png)
> 如果仅仅试用，可以选用自定义的数据集或者只上传一部分图片。

6.步骤5图片上传结束后，我们就可以开始使用该 Phantoscope 应用进行搜索啦。
```bash
curl --location --request POST '127.0.0.1:5000/v1/application/object-example/search' \
--header 'Content-Type: application/json' \
--data-raw '{
	"fields": {
        "object": {
            "url": "https://tse4-mm.cn.bing.net/th/id/OIP.RTFEnp5e4zb-CkbYvO1KfwHaHT?pid=Api&rs=1"
        }
    },
    "topk": 10,
    "nprobe": 20
}'
```
运行上述命令通过 RESTful API 进行搜索，该图片并不存在于上传的底库。可以看到运行结果中包含了10条搜索结果。

![result6](/.github/example/object-example6.png)
如果觉得这样的结果并不直观， 可以尝试使用[]()进行搜索, Phantoscope preview 提供了演示的前端，使用它接入 Phantoscope 你可以直观地使用自己创建的 Phantoscope 应用作为预览。享受 Phantoscope 给图片搜索带来的便利吧。
```bash
docker run -d -e API_URL=http://$LOCAL_ADDRESS:5000 -p 8000:80 phantoscope/preview:latest
```

![result7](/.github/example/object-example7.png)

