# Phantoscope 快速开始
## 开始之前
开始之前[安装](..\..\..\..\README_CN.md#安装)

确认 Phantoscope 所有组件正常：
```bash
$ docker-compose ps
```

*看到如下输出即表示 Phantoscope 正在运行:*
```bash
        Name                      Command               State                         Ports                       
------------------------------------------------------------------------------------------------------------------
phantoscope_api_1      /usr/bin/gunicorn3 -w 4 -b ...   Up      0.0.0.0:5000->5000/tcp                            
phantoscope_milvus_1   /var/lib/milvus/docker-ent ...   Up      0.0.0.0:19121->19121/tcp, 0.0.0.0:19530->19530/tcp
phantoscope_minio_1    /usr/bin/docker-entrypoint ...   Up      0.0.0.0:9000->9000/tcp                            
phantoscope_mongo_1    docker-entrypoint.sh mongod      Up      0.0.0.0:27017->27017/tcp 
```


## 准备环境

运行 scripts 文件夹下的 prepare.sh 脚本。该脚本注册了一个 operator，并以该 operator 创建一个 pipeline，并根据该 pipeline 创建了一个名为 example_app 的 application。
```bash
$ chmod +x scripts/prepare.sh
$ ./scripts/prepare.sh
```

## 下载图片数据
本文使用的 MSCOCO 动物图片数据集是 COCO 数据集的一小部分，由斯坦福大学的研究人员提供。包含熊，鸟，猫，狗等 8 类的 800 个训练图像和 200 个测试图像：。
```bash
$ curl http://cs231n.stanford.edu/coco-animals.zip -o /tmp/coco-animals.zip
```

## 导入图片数据集
```bash
$ unzip /tmp/coco-animals.zip -d /tmp/
$ pip3 install requests tqdm
$ python3 scripts/load_data.py -s $LOCAL_ADDRESS:5000 -a example_app -p example_pipeline -d /tmp/coco-animals
```
上传图片根据机器性能不同，时间会有差异。

## 使用 Phantoscope Preview 进行搜索

```bash
$ docker run -d -e API_URL=http://$LOCAL_ADDRESS:5000 -p 8000:80 phantoscope/preview:0.2.0
```
浏览器打开 127.0.0.1:8000 
![Phantoscope Preview 演示图](https://live.staticflickr.com/65535/50140138947_2801b030df_o.gif)



## 使用 curl 导入一张图片
如果你想单独导入一张图片，可以使用如下命令
```bash
$ curl --location --request POST $LOCAL_ADDRESS':5000/v1/application/example_app/upload' \
--header 'Content-Type: application/json' \
--data "{
    \"fields\": {
        \"example_field\": {
            \"url\": \"https://tse2-mm.cn.bing.net/th/id/OIP.C3pWPyFPhBMiBeWoncc24QHaCq?w=300&h=108&c=7&o=5&dpr=2&pid=1.7\"
        }
    }
}"
```

*预期得到如下响应：*
```json
[
    {
        "_id":"5f103b21f92bc0c90cc7f737",
        "_docs":{
            "example_field":{
                "ids":[
                    1594899233036739000
                ],
                "url":"http://192.168.1.192:9000/example-s3/example_app-33c5bf6ce2a0482593993140e83a6481"
            }
        }
    }
]
```

## 使用 curl 进行搜索
```bash
$ curl --location --request POST $LOCAL_ADDRESS':5000/v1/application/example_app/search' \
--header 'Content-Type: application/json' \
--data "{
    \"fields\": {
        \"example_field\": {
            \"url\": \"https://tse2-mm.cn.bing.net/th/id/OIP.C3pWPyFPhBMiBeWoncc24QHaCq?w=300&h=108&c=7&o=5&dpr=2&pid=1.7\"
        }
    },
    \"topk\": 2
}"
```

*预期得到如下响应：*
```json
[
    {
        "_id":"5f103b21f92bc0c90cc7f737",
        "_docs":{
            "example_field":{
                "ids":[
                    1594899233036739000
                ],
                "url":"http://192.168.1.192:9000/example-s3/example_app-33c5bf6ce2a0482593993140e83a6481"
            }
        }
    },
    {
        "_id":"5f103b9faf56a7d8833f5597",
        "_docs":{
            "example_field":{
                "ids":[
                    1594899359173444000
                ],
                "url":"http://192.168.1.192:9000/example-s3/example_app-b20d796e8cda4a539201557bd418a89f"
            }
        }
    }
]
```
