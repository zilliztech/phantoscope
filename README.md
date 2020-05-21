![](https://github.com/zilliztech/omnisearch/blob/master/.github/logo-fake.png)
创建完全贴合你自己的图片搜索引擎

Omnisearch is a cloud native image search engine powered by neural networks

 - 使用 omnisearch 提供的扩展可以快速组装一个图片搜索引擎无须写一行代码
 - 借助于 milvus omnisearch 拥有极快的搜索速度并可以处理十亿级别的数据
 - omnisearch 完全兼容 tensorflow pytorch TensorRT ONNX XGBoost 等框架
 - omnisearch 提供了丰富的扩展，也可以使用自己的模型创造一个自己的扩展
 - omnisearch 即将提供扩展仓库，在这里可以上传并与全世界的使用者分享你的扩展
 - omnisearch 提供了 dashboard 的图形界面，在 dashboard 中你可以直观快速的验证自己的扩展提供的效果
 - omnisearch 即将提供扩展运行模式(extension runtime)，原生支持 docker 与 kubernetes

## Table of Contents

 - [Background](https://github.com/zilliztech/omnisearch#Background)
 - [Install](https://github.com/zilliztech/omnisearch#Install)
 - [QuickStart](https://github.com/zilliztech/omnisearch#QuickStart)
 - [Examples](https://github.com/zilliztech/omnisearch#Examples)
 - [Contributing](https://github.com/zilliztech/omnisearch#Contributing)
 - [Community](https://github.com/zilliztech/omnisearch#Community)
 - [Roadmap](https://github.com/zilliztech/omnisearch#Roadmap)
 - [License](https://github.com/zilliztech/omnisearch#License)
## Background
音频、视频的数据会越来越多，搜索变成了一件复杂的事情

单一的文本搜索无法满足维度日益增加的搜索需求

一张图片中附带的信息量要大于一个单词附带的信息量

人们需要搜索拥有更高密度信息的数据，目前的图片、视频、音频，在未来还会有 3D 模型、VR 数据等等更复杂的数据

人类的搜索不应该被局限在单词与短句

然而多维度的搜索面临着问题---搜索的重心在哪里?

不同人在不同条件下搜索的重心各不相同，针对不同场景的多维度搜索成为了重要功能

人们无法覆盖到所有的使用场景，那么就需要根据不同的场景进行改动，

经过简单组装后即可以提供强大功能与效率的搜索引擎，这就是 omnisearch 

## Install

    wget https://github.com/zilliztech/omnisearch/blob/master/docker-compose.yml
    docker-compose up -d

## QuickStart
Run a example omnisearch application from [here](https://github.com/zilliztech/omnisearch/tree/master/docs/quickstart)

## Concepts
从[这里](https://github.com/zilliztech/omnisearch/tree/master/docs/example)你可以看到 omnisearch 在不同场景下的应用
从图片了解 omnisearch 中的概念

雨水与水厂的动图 10s 或者短视频
![](https://github.com/zilliztech/omnisearch/blob/master/.github/omnisearch-explain.png)
## Contributing
Read the omnisearch design principles from [here](https://github.com/zilliztech/omnisearch/tree/master/docs/design-principles)
### Build omnisearch from code

    make all
    
## Community

 - Slack Channel
 - Google group

## Roadmap
[GitHub milestones](https://github.com/zilliztech/omnisearch/milestones) lay out the path to the future improvements.

## License
Omnisearch is licensed under the Apache License, Version 2.0. [See LICENSE for the full license text.](https://github.com/zilliztech/omnisearch/blob/master/LICENSE)
