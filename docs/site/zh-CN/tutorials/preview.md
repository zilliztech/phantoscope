# 如何使用 phantoscope preview
phantoscope preview 是一个图形化界面，用来给 phantoscope 的用户快速验证自己的应用的搜索结果

## 安装 preview
```bash
$ export LOCAL_ADDRESS=$(ip a | grep -Eo 'inet (addr:)?([0-9]*\.){3}[0-9]*' | grep -Eo '([0-9]*\.){3}[0-9]*' | grep -v '127.0.0.1'| head -n 1)
$ docker run -d -e API_URL=$LOCAL_ADDRESS:5000 -p 8000:80 phantoscope/preview:latest
```

## 使用 preview 进行搜索
浏览器打开 127.0.0.1:8000

## 切换 application
