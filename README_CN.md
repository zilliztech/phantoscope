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

Phantoscope 是一个基于 Milvus 与深度学习的云原生图像搜索引擎

**十亿级别的图像的高性能搜索**

**完全兼容 Tensorflow Pytorch TensorRT ONNX XGBoost 等主流深度学习框架**

**提供 GUI 展示搜索效果、管理 Phantoscope 资源**

**即将提供扩展仓库，在这里可以上传并与全世界的开发者分享你的扩展**

**原生支持 Docker 与 Kubernetes**

中文版 | [English](README.md)

## 目录

- [背景](#背景)
- [安装](#安装)
- [快速开始](#快速开始)
- [架构图](#架构图)
- [概念](#概念)
- [教程](#教程)
- [API](#API)
- [贡献者指南](#贡献者指南)
- [加入社区](#加入社区)
- [路线图](#路线图)
- [协议](#协议)

## 背景

人类的搜索不应该被局限在单词与短句。

随着图像、视频等数据所占人类生活的比重越来越大，原先的单一文本搜索已经越来越无法满足人们的需求。

一张图像包含了大量的信息，不同人站在不同的角度解读，会产生不同的结果。无论是现在的全文检索还是以图搜图的搜索引擎，都无法满足这种灵活多变的高维度搜索需求。

利用深度学习模型，灵活组合不同的图片处理技术，加上 Milvus 向量搜索引擎的强大赋能后，提供统一接口的高性能图像搜索引擎，这就是 Phantoscope。

## 安装

### 环境准备

- Docker >= 19.03
- Docker Compose >= 1.25.0
- Python >= 3.5

> Phantoscope 已经在 x86 平台下的 Ubuntu 16.04 和 CentOS 7.3 以上经过验证，在 macOS 与 Windows 下可能会存在未知问题。

### 开始安装


```bash
$ git clone https://github.com/zilliztech/phantoscope.git && cd phantoscope
$ export LOCAL_ADDRESS=$(ip a | grep -Eo 'inet (addr:)?([0-9]*\.){3}[0-9]*' | grep -Eo '([0-9]*\.){3}[0-9]*' | grep -v '127.0.0.1'| head -n 1)
$ docker-compose up -d
```

检查所有容器状态：
``` bash
$ docker-compose ps
``` 

*预期得到如下输出：*
```
Name                   Command                          State   Ports
----------------------------------------------------------------------------------------------------------------
phantoscope_api_1      /usr/bin/gunicorn3 -w 4 -b ...   Up      0.0.0.0:5000->5000/tcp
phantoscope_milvus_1   /var/lib/milvus/docker-ent ...   Up      0.0.0.0:19530->19530/tcp, 0.0.0.0:8080->8080/tcp
phantoscope_minio_1    /usr/bin/docker-entrypoint ...   Up      0.0.0.0:9000->9000/tcp
phantoscope_mysql_1    docker-entrypoint.sh mysqld      Up      0.0.0.0:3306->3306/tcp
phantoscope_vgg_1      python3 server.py                Up      0.0.0.0:50001->50001/tcp
```

## 快速开始

从[这里](./docs/site/zh-CN/quickstart) 运行一个最小的 Phantoscope 应用,你可以使用它来上传与搜索图像。

## 架构图

![](./.github/ps-architecture.png)
![](./.github/phantoscope.png)
## 基本概念
                                                  
- [什么是 Operator？](./docs/site/zh-CN/tutorials/operator.md)                                                      
- [什么是 Pipeline？](./docs/site/zh-CN/tutorials/pipeline.md)                                                         
- [什么是 Application？](./docs/site/zh-CN/tutorials/application.md)                                                    


## 教程

- [如何使用 Phantoscope Preview？](./docs/site/zh-CN/tutorials/preview.md)
- [如何创建一个 Application？](./docs/site/zh-CN/examples/object.md)
- [如何开发一个 Operator？](./operators/HowToAddAnOperator.md)                                           

 
## API 参考

点击 [这里](https://app.swaggerhub.com/apis-docs/phantoscope/Phantoscope/0.1.0) 阅读详细 RESTful API 文档。

## 贡献者指南

我们由衷欢迎你的贡献。关于贡献流程的详细信息，请参阅 [贡献者指南](CONTRIBUTING.md)。

本项目遵循 Phantoscope [行为准则](CODE_OF_CONDUCT.md)。如果你希望参与本项目，请遵守该准则的内容。

我们使用 [GitHub issues](https://github.com/zilliztech/phantoscope/issues) 追踪问题和补丁。

如需提出问题或进行讨论，请加入我们的社区。


## 加入社区

- [Slack 频道](https://join.slack.com/t/zillizworkplace/shared_invite/zt-enpvlmud-6gnqhPqQryhQLfj3BQhbew) 这里可以进行沟通与咨询在使用过程中遇到的问题。


## 路线图

你可以参考我们的[路线图](https://github.com/zilliztech/phantoscope/milestones)。

我们欢迎更多的人可以一起参与到 Phantoscope 的开发当中。 


## 许可协议
Apache License 2.0
