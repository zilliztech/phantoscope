
Phantoscope Preview 是一个图形化界面，用来给 Phantoscope 的用户快速验证自己的应用的搜索结果。

## 安装 Preview
```bash
$ export LOCAL_ADDRESS=$(ip a | grep -Eo 'inet (addr:)?([0-9]*\.){3}[0-9]*' | grep -Eo '([0-9]*\.){3}[0-9]*' | grep -v '127.0.0.1'| head -n 1)
$ docker run -d -e API_URL=$LOCAL_ADDRESS:5000 -p 8000:80 phantoscope/preview:0.2.0
```

## 使用 Preview 进行搜索
浏览器打开 http://127.0.0.1:8000 即可看到 Preview 界面。


![](https://live.staticflickr.com/65535/50140138947_2801b030df_o.gif)



## Preview 工作区介绍
![](../../../../.github/phantoscope-preview.png)

1. 点击左上方放大镜图案可以从本地选择图片文件进行搜索。
2. 拖拽图片至左侧区域也可以进行搜索。
3. 通过调整剪裁区的边框可以使用部分图片进行搜索。
4. 点击 **application** 可以进行 application 的切换。

> 注意：application 目前需要使用 RESTful API 进行创建。

