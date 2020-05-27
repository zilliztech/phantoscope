# 什么是 Pipeline
Pipeline 是 omnisearch 中用来组合 Operator 的，是对数据处理流程的抽象

负责将上一个 operator 的输出传送到下一个 operator 的输入

pipeline 主要的功能是控制数据的流向

在设计 Pipeline 时有一些设计原则需要遵守

1. 一个 Pipeline 有且仅有一个 encoder
2. 一个 Pipeline 可以没有 processor
3. Pipeline 必须要有 encoder
4. Pipeline 的输入必须满足第一个 operator 的输入要求
