![](https://github.com/zilliztech/phantoscope/blob/master/.github/phantoscope-logo-fake.png)

![CI](https://github.com/zilliztech/phantoscope/workflows/CI/badge.svg?branch=master)

Phantoscope is a cloud native image search engine powered by Milvus and neural networks

🚀 **极快的搜索速度并可以处理十亿级别的图片**

🎭 **完全兼容 Tensorflow Pytorch TensorRT ONNX XGBoost 等框架**

📝 **提供了丰富的扩展，也可以在五分钟内使用自己的模型创造一个自己的扩展**

📇 **提供了 gui 快速的验证自己的扩展提供的效果并管理自己的数据**

🏭 **即将提供扩展仓库，在这里可以上传并与全世界的使用者分享你的扩展**

🚢 **即将提供扩展运行模式(extension runtime)，原生支持 docker 与 kubernetes**

[Here need a gif show what phantoscope can do]()

## Table of Contents

 - [Background](#background)
 - [Install](#install)
 - [QuickStart](#quickStart)
 - [Concepts](#concepts)
 - [Contributing](#contributing)
 - [Community](#community)
 - [Roadmap](#roadmap)
 - [License](#license)

<a href=”#background”/>
## Background

人类的搜索不应该被局限在单词与短句。

随着音频、视频的数据所占比重越来越大，在未来还会有更多更高维度的数据出现在我们的日常生活当中。

人们需要搜索拥有更高密度信息的数据，目前的图片、视频、音频，在未来还会有 3D 模型、VR 数据等等更复杂的数据。

搜索变成了一件复杂的事情。

单一的文本搜索无法满足维度日益增加的搜索需求。

然而多维度的搜索面临着问题---搜索的重心在哪里?

一张图片中包含的几十个单词构成的信息，一个几秒钟的视频又包含了上百长的图片以及对应的音频，传统的搜索模式无法满足现有的场景。

不同人在不同条件下搜索的重心各不相同，针对不同场景的多维度搜索成为了重要功能。

人们无法覆盖到所有的使用场景，那么就需要根据不同的场景进行改动，

经过简单组装后即可以提供强大功能与效率的搜索引擎，这就是 Phantoscope。

<a href="#install"/>
## Install

    $ wget https://github.com/zilliztech/phantoscope/blob/master/docker-compose.yml
    $ export LOCAL_ADDRESS=$(ip a | grep -Eo 'inet (addr:)?([0-9]*\.){3}[0-9]*' | grep -Eo '([0-9]*\.){3}[0-9]*' | grep -v '127.0.0.1'| head -n 1)
    $ docker-compose up -d

## Build from code

	$ make all

<a href="#quickstart"/>

## QuickStart

Run an example phantoscope application from [here](./docs/site/zh-CN/quickstart)

这个example 创建了一个最小的 Application,你可以使用它来上传与搜索图片

<a href="#concepts"/>

## Concepts
从 [这里](./docs/site/zh-CN/examples) 你可以看到 Phantoscope 在不同场景下的应用:

 - 根据图片中的人脸进行搜索![](./docs/site/zh-CN/examples/face.md)
 - 根据图片中的物体进行搜索![](./docs/site/zh-CN/examples/object.md)

从下面了解 Phantoscope 中的概念

雨水与水厂的动图 10s 或者短视频
![](/.github/phantoscope-explain.png)

| Tutorials                                                                                              <img width=700/> | level  |
|-------------------------------------------------------------------------------------------------------------------------|--------|
| [What is operators](./docs/site/zh-CN/tutorials/operator.md)                    | simple |
| [What is pipeline](./docs/site/zh-CN/tutorials/pipeline.md)                     | simple |
| [What is application](./docs/site/zh-CN/tutorials/application.md)               | simple |

<a href="#contributing"/>
## Contributing

Contributions are welcomed and greatly appreciated. 

Please read our [contribution guidelines](CONTRIBUTING.md) for detailed contribution workflow.

We use [GitHub issues](https://github.com/zilliztech/phantoscope/issues) to track issues and bugs. 

For general questions and public discussions, please join our community.

<a href="#community"/>

## Community

- Slack Channel 这里可以进行沟通与咨询在使用过程中遇到的问题
- [公司主页](https://zilliz.com/) 这里可以了解到关于 zilliz 的更多资讯

<a href="#roadmap"/>

## Roadmap
[GitHub milestones](https://github.com/zilliztech/phantoscope/milestones) lay out the path to the future improvements.

包括 Roadmap 在内，我们希望更多的人可以一起参与到 operators 的开发当中

在 [这里](https://github.com/ReigenAraka/omnisearch-operators) 你可以找到如何开发一个 operator

如果您有任何问题请随时联系我们 phantoscope@zilliz.com

<a href="#license"/>

## License
Phantoscope is licensed under the Apache License, Version 2.0. 
