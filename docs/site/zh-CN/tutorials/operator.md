# 什么是 Operator
Operator 是 Phantoscope 中的工作单元

正是由于 operator 的多样性，Phantoscope 才可以完成不同的功能

同样您也可以根据文档实现自己的 operator 然后加入到 Phantoscope 中为您工作

Operator 根据工作不同分为两种 Processor 与 encoder

## Processor
processor 是 operator 当中最通用的一类，他们接受数据并处理数据然后将数据交给下一个 operator

通常来说 processor 处理的数据与发送的数据都是同一种类型的

例如:processor 接收了一张图片然后将图片中的人脸数据提取出来，然后将人脸的数据发送出去

procssor 只要进行接收、处理、发送

至于从哪里接收与发送到什么地方，processor 都不需要关心

## Encoder
encoder 可以看作特殊的 processor, encoder 与 processor 的最大区别在于

encoder 处理的数据与发送的数据类型并不一致

encoder 会将非结构化的数据转变成向量或者是标签

所以 encoder 是处理的最后一环

# Operator 的设计原则
Operator 应该是无状态的

Operator 设计上应该保持独立与可重入

Operator 独立工作并不依赖于外接存储
