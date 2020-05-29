![](https://github.com/zilliztech/phantoscope/blob/master/.github/phantoscope-logo-fake.png)

![CI](https://github.com/zilliztech/phantoscope/workflows/CI/badge.svg?branch=master)

Phantoscope is an image search engine developed on Milvus and neutral networks. 

🚀 **Extremely high speed in processing and searching billions of images.**

🎭 **Compatible with Tensorflow, Pytorch, TensorRT, ONNX, XGBoost, and more.**

📝 **Provides abundant extensions. You can build an extension using your own model within five minutes.**

📇 **Provides GUI for verifying self-developed extensions and managing data.**

🏭 **Soon to provide an extension market, where you can share your extension with the world.**

🚢 **Soon to provide extension runtime mode with native support for Docker and kubernetes.**

English | [中文版](README_CN.md) 

## Table of Contents



- [Install](#install)
- [QuickStart](#quickStart)
- [Concepts](#concepts)
- [Contributing](#contributing)
- [Community](#community)
- [Roadmap](#roadmap)
- [License](#license)



<a href="#install"></a>
## Install

```
$ wget https://github.com/zilliztech/phantoscope/blob/master/docker-compose.yml
$ export LOCAL_ADDRESS=$(ip a | grep -Eo 'inet (addr:)?([0-9]*\.){3}[0-9]*' | grep -Eo '([0-9]*\.){3}[0-9]*' | grep -v '127.0.0.1'| head -n 1)
$ docker-compose up -d
```

## Build from code

```
$ make all
```

<a href="#quickstart"></a>
## QuickStart

Click [here](./docs/site/en/quickstart) to set up a simple Phantoscope application. You can use it to upload and search images.

<a href="#concepts"></a>
## Concepts

From [here](./docs/site/en/examples), you can get an idea as to how you can apply Phantoscope to different scenarios:

 - Search by human face![](./docs/site/en/examples/face.md)
 - Search by ![](./docs/site/en/examples/object.md)

The following figure illustrates the basic concepts of the Phantoscope project.


![](/.github/phantoscope-explain.png)

| Tutorial                                                                                              <img width=700/> | Level  |
| ------------------------------------------------------------ | ------ |
| [ What is operator](./docs/site/en/tutorials/operator.md)    | Simple |
| [What is pipeline](./docs/site/en/tutorials/pipeline.md)     | Simple |
| [What is application](./docs/site/en/tutorials/application.md) | Simple |

<a href="#contributing"></a>
## Contributing

Contributions are welcomed and greatly appreciated. 

Please read our [contribution guidelines](CONTRIBUTING.md) for detailed contribution workflow.

We use [GitHub issues](https://github.com/zilliztech/phantoscope/issues) to track issues and bugs. 

For general questions and public discussions, please join our community.

<a href="#community"></a>
## Community

- Go to our Slack Channel, if you run into issues and want to consult our experts.
- Click [here](https://zilliz.com/) to learn more about Zilliz. 

<a href="#roadmap"></a>

## Roadmap
[GitHub milestones](https://github.com/zilliztech/phantoscope/milestones) lays out the development plan for Phantoscope. 

We hope you could join us in developing operators.  From [here](https://github.com/ReigenAraka/omnisearch-operators), you can find more information about how to develop an operator.

If you have further questions, contact phantoscope@zilliz.com

<a href="#license"></a>
## License

Apache License 2.0
