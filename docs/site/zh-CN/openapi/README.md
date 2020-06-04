# Phantoscope API 文档

## 如何访问在线的 API 文档

你可以访问 https://app.swaggerhub.com/apis/ReigenAraka/Phantoscope/1.0.0 来阅读 Phantoscope 的 API 文档

## 如何使用 swagger 在本地启动 swagger 

    docker run -p 8080:8080 -e SWAGGER_JSON=/foo/swagger.json -v "$(pwd)":/foo  swaggerapi/swagger-ui

浏览器打开 127.0.0.1:8080 即可在本地浏览 Phantoscope 的 API 文档
