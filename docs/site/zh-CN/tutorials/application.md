# 什么是 Application
## Application 对应的是实际业务场景

例如对现在需要对人进行搜索,那么 Application 的定义可能是

```json
{
    "fields": {
        "face": {
            "type": "pipeline",
            "value": "face"
        },
        "name": {
            "type": "string"
        },
        "age": {
            "type": "int"
        }
    }
}
```
在这个 Application 的定义中有两种类型的数据: 结构化数据(name, age)与非结构化数据(face)

针对结构化的数据, Phantoscope 会将其存储起来,并且会在下一个版本中支持结构化数据与非结构化数据的混合查询

对与非结构化的数据, 这里定义了一个 Pipeline 来处理人脸的图片

当使用这个 Application 进行上传与搜索时,数据会按照这种方式进行保存与查找

不同的场景由于处理的流程(Pipeline)与数据各不相同，所以需要多个 Application。

## Application 支持多分支的 Pipeline 吗
在当前版本，Application 支持一条或多条 Pipeline 的上传与搜索，关于多 Pipeline 的搜索方案可以参考 [Score Function](./score_function.md)。

接下来的版本中, Application 会支持一条 Pipeline 中 存在多个分支的情况。


