![](https://github.com/zilliztech/phantoscope/blob/master/.github/logo.png)

![CI](https://github.com/zilliztech/phantoscope/workflows/CI/badge.svg?branch=master)
![GitHub](https://img.shields.io/github/license/zilliztech/phantoscope)
![GitHub top language](https://img.shields.io/github/languages/top/zilliztech/phantoscope)
![GitHub All Releases](https://img.shields.io/github/downloads/zilliztech/phantoscope/total)
![GitHub release (latest by date)](https://img.shields.io/github/v/release/zilliztech/phantoscope)
![GitHub commit activity](https://img.shields.io/github/commit-activity/w/zilliztech/phantoscope)
![Github realease data](https://img.shields.io/github/release-date/zilliztech/phantoscope)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/zilliztech/phantoscope.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/zilliztech/phantoscope/context:python)
[![codecov](https://codecov.io/gh/zilliztech/phantoscope/branch/master/graph/badge.svg)](https://codecov.io/gh/zilliztech/phantoscope)

Phantoscope 是一个基于 Milvus 与深度学习的云原生图片搜索引擎

**极快的搜索速度并可以处理十亿级别的图片**

**完全兼容 Tensorflow Pytorch TensorRT ONNX XGBoost 等框架**

**提供了丰富的扩展，也可以在五分钟内使用自己的模型创造一个自己的扩展**

**提供了 gui 快速的验证自己的扩展提供的效果并管理自己的数据**

**即将提供扩展仓库，在这里可以上传并与全世界的使用者分享你的扩展**

**即将提供扩展运行模式(extension runtime)，原生支持 docker 与 kubernetes**

中文版 | [英文版](README.md)

## Table of Contents

- [背景](#背景)
- [安装](#安装)
- [快速开始](#快速开始)
- [教程](#教程)
- [示例](#示例)
- [API](#API)
- [贡献者指南](#贡献者指南)
- [加入社区](#加入社区)
- [路线图](#路线图)
- [协议](#协议)


## 背景

人类的搜索不应该被局限在单词与短句。

随着音频、视频的数据所占比重越来越大，在未来还会有更多更高维度的数据出现在我们的日常生活当中。

人们需要搜索拥有更高密度信息的数据，目前的图片更复杂的数据。

搜索变成了一件复杂的事情。

单一的文本搜索无法满足维度日益增加的搜索需求。

然而多维度的搜索面临着问题---搜索的重心在哪里?

一张图片中包含的几十个单词构成的信息，不同人在不同条件下搜索的重心各不相同，针对不同场景的多维度搜索成为了重要功能。

人们无法覆盖到所有的使用场景，那么就需要根据不同的场景进行改动，

经过简单组装后即可以提供强大功能与效率的搜索引擎，这就是 Phantoscope。

## 安装
### 安装环境说明
1. docker >= 19.03
2. docker-compose >= 1.25.0
### 开始安装
```
$ git clone https://github.com/zilliztech/phantoscope.git && cd phantoscope
$ export LOCAL_ADDRESS=$(ip a | grep -Eo 'inet (addr:)?([0-9]*\.){3}[0-9]*' | grep -Eo '([0-9]*\.){3}[0-9]*' | grep -v '127.0.0.1'| head -n 1)
$ docker-compose up -d
```
执行 ```docker-compose ps``` 确认所有的容器状态均为 Up

## 快速开始
从[这里](./docs/site/zh-CN/quickstart)运行一个最小的 Phantoscope 应用,你可以使用它来上传与搜索图片。


## 教程

| Tutorials                                                                                              <img width=700/> | level  |
| ------------------------------------------------------------                                                            | ------ |
| [如何使用 phantoscope preview](./docs/site/zh-CN/tutorials/preview.md)                                                  | ⭐     |
| [什么是 operators](./docs/site/zh-CN/tutorials/operator.md)                                                             | ⭐⭐   |
| [什么是 pipeline](./docs/site/zh-CN/tutorials/pipeline.md)                                                              | ⭐⭐   |
| [什么是 application](./docs/site/zh-CN/tutorials/application.md)                                                        | ⭐⭐   |
| [如何开发一个 operator](./operators/HowToAddAOperator.md)                                                               | ⭐⭐⭐ |
## 示例
从 [这里](./docs/site/zh-CN/examples) 你可以看到 Phantoscope 在不同场景下的应用:

 - 根据图片中的人脸进行搜索![](./docs/site/zh-CN/examples/face.md)
 - 根据图片中的物体进行搜索![](./docs/site/zh-CN/examples/object.md)
## API
Phantoscope 使用 swagger 来编写与管理 API 文档，阅读 [这里](./docs/site/zh-CN/openapi/README.md) 获取详情。

## 贡献者指南
我们由衷欢迎您推送贡献。关于贡献流程的详细信息，请参阅 [贡献者指南](CONTRIBUTING.md)。

本项目遵循 Phatoscope [行为准则](CODE_OF_CONDUCT.md)。如果您希望参与本项目，请遵守该准则的内容。

我们使用 [GitHub issues](https://github.com/zilliztech/phantoscope/issues) 追踪问题和补丁。

若您希望提出问题或进行讨论，请加入我们的社区。



## 加入社区

- Slack [频道](https://join.slack.com/t/zillizworkplace/shared_invite/zt-enpvlmud-6gnqhPqQryhQLfj3BQhbew)这里可以进行沟通与咨询在使用过程中遇到的问题
- [公司主页](https://zilliz.com/) 这里可以了解到关于 zilliz 的更多资讯


## 路线图

您可以参考我们的[路线图](https://github.com/zilliztech/phantoscope/milestones)。

包括 Roadmap 在内，我们希望更多的人可以一起参与到 Pantoscope 的开发当中。

如果您有任何问题请随时联系我们 phantoscope@zilliz.com。


## 协议

Apache License 2.0
