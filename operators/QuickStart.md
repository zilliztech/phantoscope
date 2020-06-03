
## 快速开始 (docker pull)

### CPU版本
PS: 待 docker hub 确定后上传拉取 （需要修改相关参数）

```bash
# 拉取对应版本的 docker 镜像, ${tag}应替换为可选的tag
docker pull psoperator/face-encoder:${tag}
# 以该镜像快速启动一个容器,同时设置容器配置:
# 1. 将容器的50004端口映射到本机
# 2. 将容器的 /app/tmp 目录映射到本机,以方便查看/调试 encoder 内部图片缓存
docker run -p 50004:50004 -v `pwd`/tmp:/app/tmp -d psoperator/face-encoder:${tag}
```

### GPU 版本

```bash
# 拉取对应版本的 docker 镜像, ${tag}应替换为可选的tag
docker pull psoperator/face-encoder-gpu:${tag}
# 以该镜像快速启动一个容器,同时设置容器配置:
# 1. 将容器的50004端口映射到本机
# 2. 将容器的 /app/tmp 目录映射到本机,以方便查看/调试 encoder 内部图片缓存
# 3. 开放容器对 GPU 的可见权限, 以只开放 device 0 的 GPU 为例
docker run --gpus="device=0" -e device_id="/device:GPU:0" \
   -p 50004:50004 -v `pwd`/tmp:/app/tmp -d psoperator/face-encoder-gpu:${tag}
```

## 快速开始 (docker build)
以 face embedding encoder 为例, 本节旨在3分钟之内以 docker build 的方式搭建一个最简单的 encoder 服务.

```bash
# 切换到工作目录
cd face-encoder
# 1. 准备模型, 以加速后续镜像构建, 比较耗时(可选)
cd data && ./prepare_model.sh && cd ..
# 2. 构建 docker 镜像
make cpu
# 3. 启动 docker 容器
# (提示: ${tag} 为 刚构建的镜像 tag, 可通过 docker images 查看)
docker run -p 50004:50004 -v `pwd`/tmp:/app/tmp \
   -d psoperator/face-encoder:${tag}
```

## 快速开始 (source build)
以 face embedding encoder 为例, 本节旨在3分钟之内以 source build 的方式搭建一个最简单的 encoder 服务.
