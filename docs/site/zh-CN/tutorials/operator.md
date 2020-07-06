# 什么是 Operator
Operator 是 Phantoscope 中工作单元的抽象描述，根据 Operator 可以创建工作单元。

正是由于 Operator 的多样性，Phantoscope 才可以完成不同的功能

同样你也可以根据[文档](../../../../operators/HowToAddAnOperator.md)实现自己的 Operator 然后注册到 Phantoscope 中为你工作

Operator 根据工作不同分为两种: Processor 与 Encoder

## Processor
Processor 是 Operator 当中最通用的一类，它们接收数据，并将处理完成数据交给下一个 Operator

通常来说 Processor 处理的数据与发送的数据都是同一种类型的

例如:

Processor 接收了一张图片然后将图片中的人脸数据提取出来，然后将人脸的数据发送出去

Processor 只要进行接收、处理、发送

至于从哪里接收与发送到什么地方，Processor 都不需要关心

目前 Phantoscope 内置的 Processor 有以下几种。

- ###### MTCNN-face-detector
    - 镜像名： face-detector
    - 功能： 检测输入图片中的人脸
    - 接受： 一张图片
    - 返回： 检测出的一组人脸图片
    - 样例 Pipeline：mtcnn-face-detector -> face-encoder

> 以 [Facenet](https://github.com/davidsandberg/facenet.git) 实现。 

- ###### Mask-RCNN-object-detector
    - 镜像名： mask-rcnn-detector
    - 功能： 检测输入图片中的物体
    - 接受： 一张图片
    - 返回： 检测出的一组物体图片
    - 样例 Pipeline：mask-rcnn-object-detetcor -> vgg/xception

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

目前 Phantoscope 内置的 Encoder 有以下几种。

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

> 以 [Facenet](https://github.com/davidsandberg/facenet.git) 实现。

## 注册一个 Operator
Phantoscope 启动时是没有 Operator 的，在当前版本中，你可以使用以下命令注册一个 Operator。
其中 addr 是 Operator 拉取的地址，在下面的命令中可以理解为镜像地址。
```bash
curl --location --request POST '127.0.0.1:5000/v1/operator/register' \
--header 'Content-Type: application/json' \
--data '{
    "name": "face_detector",
    "addr": "psoperator/face-detector:latest",
    "author" :"phantoscope",
    "type":"processor",
    "description": "detect face in input images",
    "version": "0.1.0"
}'
```

## 创建一个 Operator Instance
已经注册成功一个 Operator 后，还需要根据该 Operator 创建一个 instance 作为 Phantoscope 实际的工作单元。
当前版本可以通过以下命令创建。

```bash
curl --location --request POST '127.0.0.1:5000/v1/operator/face_detector/instances' \
--header 'Content-Type: application/json' \
--data '{
    "instanceName": "face_detector1" 
}'
```

第一次创建可能会从远端拉取镜像。创建成功后本地机器上会出现一个该镜像的容器。

# Operator 的设计原则
Operator 应该是无状态的 

Operator 设计上应该保持独立与可重入

Operator 独立工作并不依赖于外接存储
