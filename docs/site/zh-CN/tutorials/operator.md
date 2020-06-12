# 什么是 Operator
Operator 是 Phantoscope 中的工作单元

正是由于 Operator 的多样性，Phantoscope 才可以完成不同的功能

同样您也可以根据[文档](../../../../operators/HowToAnddaOperator.md)实现自己的 Operator 然后加入到 Phantoscope 中为您工作

Operator 根据工作不同分为两种 Processor 与 Encoder

## Processor
Processor 是 Operator 当中最通用的一类，它们接收数据，并将处理完成数据交给下一个 Operator

通常来说 Processor 处理的数据与发送的数据都是同一种类型的

例如:

Processor 接收了一张图片然后将图片中的人脸数据提取出来，然后将人脸的数据发送出去

Processor 只要进行接收、处理、发送

至于从哪里接收与发送到什么地方，Processor 都不需要关心

- ###### MTCNN-face-detector
    - 镜像名： face-detector
    - 功能： 检测输入图片中的人脸
    - 接受： 一张图片
    - 返回： 检测出的一组人脸图片
    - 样例 Pipeline：mtcnn_detect_face -> face_embedding

> 以 [facenet](https://github.com/davidsandberg/facenet.git) 实现。 

- ###### Mask-RCNN-object-detector
    - 镜像名： mask-rcnn-detector
    - 功能： 检测输入图片中的物体
    - 接受： 一张图片
    - 返回： 检测出的一组物体图片
    - 样例 Pipeline：mask_rcnn -> vgg/xception

> 以 [Mask_RCNN](https://github.com/matterport/Mask_RCNN) 实现

- ###### SSD-object-detector
    - 镜像名： ssd-detector
    - 功能： 检测输入图片中的物体
    - 接受： 一张图片
    - 返回： 检测出的一组物体图片
    - 样例 Pipeline：ssd-object-detector -> vgg/xception

> 以 [Tensorflow SSD](https://github.com/scanner-research/scannertools/blob/master/scannertools/scannertools/object_detection.py) 模型实现

- ###### YOLOv3-object-detector
    - 镜像名：yolov3-detector
    - 功能： 检测输入图片中的物体
    - 接受： 一张图片
    - 返回： 检测出的一组物体图片
    - 样例 Pipeline：yolov3-object-detector -> vgg/xception

> 以 [Paddlepaddle Yolov3](https://github.com/PaddlePaddle/PaddleDetection) 模型实现

## Encoder
Encoder 可以看作特殊的 Processor, Encoder 与 Processor 的最大区别在于

Encoder 处理的数据与发送的数据类型并不一致

Encoder 会将非结构化的数据转变成向量或者是标签

所以 Encoder 是处理的最后一环

- ###### Vgg16
    - 镜像名： vgg16-encoder
    - 向量维度： 512
    - 功能： 对输入的图片进行 embedding，得到表征图片的特征向量

> 以 [Keras Vgg16](https://keras.io/zh/applications/) 实现。

- ###### Xception
    - 镜像名：xception-encoder
    - 向量维度： 2048
    - 功能： 对输入的图片进行 embedding，得到表征图片的特征向量

> 以 [Keras Xception](https://keras.io/zh/applications/) 实现。

- ###### Face-encoder
    - 镜像名：face-encoder
    - 向量维度： 128
    - 功能： 对检测出来的人脸图片进行 embedding，得到表征人脸特征的向量

> 以 [facenet](https://github.com/davidsandberg/facenet.git) 实现。

## 运行一个 Operator

```bash
$ export LOCAL_ADDRESS=$(ip a | grep -Eo 'inet (addr:)?([0-9]*\.){3}[0-9]*' | grep -Eo '([0-9]*\.){3}[0-9]*' | grep -v '127.0.0.1'| head -n 1)
# 拉取对应版本的 docker 镜像
$ docker pull psoperator/face-encoder:latest
# 以该镜像快速启动一个容器,同时设置容器配置:
# 1. 设置容器服务 endpoint 为 ${LOCAL_ADDRESS}:50004，并将容器的50004端口映射到本机
# 2. 将容器的 /app/tmp 目录映射到本机,以方便查看/调试 encoder 内部图片缓存
$ docker run -p 50004:50004 -e OP_ENDPOINT=${LOCAL_ADDRESS}:50004 -v `pwd`/tmp:/app/tmp -d psoperator/face-encoder:latest
```

## Operator 是如何注册到 Phantoscope 中的
当 Phantosscope 启动时是没有 Operator 的，在当前的版本中如果你想在 Phantoscope 中发现并使用 Operator 需要先将 Operator 手动注册到 phantoscope 中。

在默认情况下 Phantoscope 在启动时会启动一个 vgg16 的 Operator 并监听本地的 50001 端口。

这时 vgg16 虽然已经启动但是还没有注册到 Phantoscope 中。

通过向 ```/v1/operator/regist```这个 API 发送 

```json
{
    "endpoint": "LOCAL_HOST_IP:50001",
	"name": "vgg16_example"
}
```
将 vgg16 以 vgg16_example 的名字注册到 Phantoscope 中

此处的 endpoint 会被 Phantoscope 用来与 Operator 进行通讯,故不能填写为 127.0.0.1,应该填写为 192 或 10 开头的内网地址，确保在 phantoscope 可以访问。

# Operator 的设计原则
Operator 应该是无状态的 

Operator 设计上应该保持独立与可重入

Operator 独立工作并不依赖于外接存储
