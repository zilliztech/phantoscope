# 什么是 Operator
Operator 是 Phantoscope 中的工作单元

正是由于 operator 的多样性，Phantoscope 才可以完成不同的功能

同样您也可以根据[文档](../../../../operators/HowToAddaOperator.md)实现自己的 operator 然后加入到 Phantoscope 中为您工作

Operator 根据工作不同分为两种 processor 与 encoder

## Processor
processor 是 operator 当中最通用的一类，他们接收数据并处理数据然后将数据交给下一个 operator

通常来说 processor 处理的数据与发送的数据都是同一种类型的

例如:

processor 接收了一张图片然后将图片中的人脸数据提取出来，然后将人脸的数据发送出去

procssor 只要进行接收、处理、发送

至于从哪里接收与发送到什么地方，processor 都不需要关心

## Encoder
encoder 可以看作特殊的 processor, encoder 与 processor 的最大区别在于

encoder 处理的数据与发送的数据类型并不一致

encoder 会将非结构化的数据转变成向量或者是标签

所以 encoder 是处理的最后一环

## Operator 是如何注册到 phantoscope 中的
当 phantosscope 启动时是没有 operator 的，在当前的版本中如果你想在 phantoscope 中发现并使用 operator 需要先将 operator 手动注册到 phantoscope 中。

在默认情况下 phantoscope 在启动时会启动一个 vgg16 的 operator 并监听本地的 50001 端口。

这时 vgg16 虽然已经启动但是还没有注册到 phantoscope 中。

通过向 ```/v1/operator/regist```这个 API 发送 

```json
{
    "endpoint": "LOCAL_HOST_IP:50001",
	"name": "vgg16_example"
}
```
将 vgg16 以 vgg16_example 的名字注册到 phantoscope 中

此处的 endpoint 会被 phantoscope 用来与 operator 进行通讯,故不能填写为 127.0.0.1,应该填写为 192 或 10 开头的内网地址，确保在 phantoscope 可以访问。
# Operator 的设计原则
Operator 应该是无状态的 

Operator 设计上应该保持独立与可重入

Operator 独立工作并不依赖于外接存储
