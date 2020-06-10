# Phantoscope Operators

## 什么是 Operator

术语 Operator 是指在 Phantoscope 的一次查询中，对图片的一次操作。Operator 一般基于一个训练好的模型进行推理。Phantoscope 的 Operator 当前支持使用 TensorFlow/paddlepaddle 作为机器学习后端进行模型推理得到特征向量。

Phantoscope 当前内置了一些 Operator 可以完成最简单的使用。如果你想创建一个 Phantoscope 未支持的流程，你可以尝试自己编写一个 Operator，并且用来组合出自己的 search 流程。

根据输入和输出的不同进行划分，我们将 Operator 分成了两类，分别是 Processor 和 Encoder。Encoder 类 Operator 接收图片作为输入，经过内部的模型推理得到表征图片特征的信息作为输出，该信息目前支持特征向量和图片标签两种。Processor 类 Operator 接收图片作为输入，经过内部的模型推理，输出为一组图片，代表为各类Detector。如目标检测器，输入为一张图片，输出为原图片中的物体图片。

下面将会按 Processor 和 Encoder 的分类分别对内置 Operator 的详细介绍，

## Prcoessor
- ###### MTCNN-face-detector
    - 镜像名： face-detector
    - 功能： 识别输入图片中的人脸
    - 接受： image
    - 返回： 识别出的一组人脸图片
    - 样例 Pipeline：mtcnn_detect_face -> face_embedding

> 以 facenet 实现， [facenet github](https://github.com/davidsandberg/facenet.git)

- ###### Mask-RCNN-object-detector
    - 镜像名： mask-rcnn-detector
    - 功能： 识别输入图片中的物体
    - 接受： image
    - 返回： 识别出的一组物体图片
    - 样例 Pipeline：mask_rcnn -> vgg/xception

> [Mask_RCNN github](https://github.com/matterport/Mask_RCNN)

- ###### SSD-object-detector
    - 镜像名： ssd-detector
    - 功能： 识别输入图片中的物体
    - 接受： image
    - 返回： 识别出的一组物体图片
    - 样例 Pipeline：ssd -> vgg/xception

> [SSD github]()

- ###### YOLOv3-object-detector
    - 镜像名：yolov3-detector
    - 功能： 识别输入图片中的物体
    - 接受： image
    - 返回： 识别出的一组物体图片
    - 样例 Pipeline：yolo -> vgg/xception

> 以 paddlepaddle yolo v3 模型实现。 [PaddleDetection github](https://github.com/PaddlePaddle/PaddleDetection)

## Encoder
- ###### Vgg16
    - 镜像名： vgg16-encoder
    - 向量维度： 512
    - 计算方式： 需要测试
    - 使用场景：
    - 功能： 对输入的图片进行 embedding，得到表征图片的特征向量

> 以 Keras Application 中 Vgg16 实现该 encoder。
- ###### Xception
    - 镜像名：xception-encoder
    - 向量维度： 2048
    - 计算方式： 需要测试
    - 使用场景：
    - 功能： 对输入的图片进行 embedding，得到表征图片的特征向量

> 以 Keras Application 中 Xception 实现该 encoder。

- ###### Face-encoder
    - 镜像名：face-encoder
    - 向量维度： 128
    - 计算方式： 需要测试
    - 使用场景：
    - 功能： 对识别出来的人脸图片进行 embedding，得到表征人脸特征的向量

> 以 facenet 实现. [facenet github](https://github.com/davidsandberg/facenet.git)

- ###### SSD-encoder
    - 镜像名： ssd-encoder
    - 标签：MSCOCO 的90种类别
    - 计算方式： 结构化数据
    - 使用场景：
    - 功能： 对输出的图片进行物体检测，得到表征图片中的物品信息的标签。
> [SSD github]()


## 快速开始

```bash
$ export LOCAL_ADDRESS=$(ip a | grep -Eo 'inet (addr:)?([0-9]*\.){3}[0-9]*' | grep -Eo '([0-9]*\.){3}[0-9]*' | grep -v '127.0.0.1'| head -n 1)
# 拉取对应版本的 docker 镜像
$ docker pull psoperator/face-encoder:latest
# 以该镜像快速启动一个容器,同时设置容器配置:
# 1. 设置容器服务 endpoint 为 ${LOCAL_ADDRESS}:50004，并将容器的50004端口映射到本机
# 2. 将容器的 /app/tmp 目录映射到本机,以方便查看/调试 encoder 内部图片缓存
$ docker run -p 50004:50004 -e OP_ENDPOINT=${LOCAL_ADDRESS}:50004 -v `pwd`/tmp:/app/tmp -d psoperator/face-encoder:latest
```
更多的, 更详细的方式可参考[快速开始](./QuickStart.md)。

## 如何实现自定义的 Operator
Phantoscope 支持最大灵活度地接入自定义的 Operator，核心只要实现预定义的 ```rpc/rpc.proto``` 中的 grpc 接口。

以下列出的是实现定制化 Operator 推荐的必要事项，任何人都可以实现这些步骤接入 Phantoscope。

1. 准备模型。
2. 实现 rpc 目录下的 grpc 接口。
3. 编写必要的编译文件以便在多数环境下正常运行。（推荐编写 makefile、 dockerfile）

P.S. 更详细的定制化 Operator 以及 快速实现的样例可参考[如何添加自定义 Operator ](./HowToAddAOperator.md)

