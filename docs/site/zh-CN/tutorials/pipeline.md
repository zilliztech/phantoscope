# 什么是 Pipeline
Pipeline 是 Phantoscope 中用来组合 Operator 实例的，是对数据处理流程的抽象。

主要负责将上一个 Operator 实例的输出传送到下一个 Operator 实例的输入。

Pipeline 主要的功能是控制数据的流向。

## Pipeline 是如何工作的
Pipeline 从 application 中接收数据然后将数据交给第一个 Operator 实例, 等待第一个 Operator 实例的返回,
获取到返回值之后将返回值作为输入交给下一个 Operator 实例, 直到运行完最后一个 Operator 实例。

在最后一个 Operator 实例运行结束之后, Phantoscope 会将数据根据类型存储到不同的地方。

## Pipeline 的设计原则
一个 Pipeline 有且仅有一个 Encoder。

一个 Pipeline 可以没有 Processor。

Pipeline 必须要有 Encoder。

Pipeline 的输入必须满足第一个 Operator 实例的输入要求。
