# 什么是 Pipeline
Pipeline 是 phatoscope 中用来组合 Operator 的，是对数据处理流程的抽象。

主要负责将上一个 operator 的输出传送到下一个 operator 的输入。

pipeline 主要的功能是控制数据的流向。

## Pipeline 是如何工作的
pipeline 从 application 中接收数据然后将数据交给第一个 operator,等待第一个 operator 的返回,
获取到返回值之后将返回值作为输入交给下一个 operator,直到运行完最后一个 operator。

在最后一个 operator 运行结束之后, phantoscope 会将数据根据类型存储到不同的地方。

## Pipeline 的设计原则
一个 Pipeline 有且仅有一个 encoder。

一个 Pipeline 可以没有 processor。

Pipeline 必须要有 encoder。

Pipeline 的输入必须满足第一个 operator 的输入要求。
