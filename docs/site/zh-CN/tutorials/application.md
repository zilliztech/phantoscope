# 什么是 Application
Application 对应的是实际业务场景。

不同的场景由于处理的流程(pipeline)与数据各不相同，所以需要多个 Application。

Application 中可以根据需求创建不同的字段，字段对应的可以是 pipeline 也可以是结构化数据。

不同的 Application 之间的数据相互隔离。

一个 Application 至少需要有一条 pipeline，如果有多条 pipeline 则需要指定 scoreling function。


