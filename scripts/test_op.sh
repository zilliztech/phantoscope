#!/bin/bash -x
LOCAL_ADDRESS=$(ip a | grep -Eo 'inet (addr:)?([0-9]*\.){3}[0-9]*' | grep -Eo '([0-9]*\.){3}[0-9]*' | grep -v '127.0.0.1'| head -n 1)


id='5'


# Regist operators
# detector
detector_end='50004'
op_name='test_op2'${id}

encoder_end='50005'
encoder_name='test_op1'${id}
curl --location --request POST '127.0.0.1:5000/v1/operator/regist' \
--header 'Content-Type: application/json' \
--data "{\"endpoint\":\"$LOCAL_ADDRESS:${detector_end}\",\"name\":\"${op_name}\"}"

# encoder

curl --location --request POST '127.0.0.1:5000/v1/operator/regist' \
--header 'Content-Type: application/json' \
--data "{\"endpoint\":\"$LOCAL_ADDRESS:${encoder_end}\",\"name\":\"${encoder_name}\"}"


pipeline_name='test_pipeline'${id}
# Create pipeline
curl --location --request POST '127.0.0.1:5000/v1/pipeline/'${pipeline_name}'' \
--header 'Content-Type: application/json' \
--data-raw '{
        "input": "image",
        "description": "pipeline example",
        "processors": "'${op_name}'",
        "encoder": "'${encoder_name}'",
        "indexFileSize": 1024
}'

app_name='test_app'${id}
field_name='test_field'${id}
s3_bucket='test-bucket'${id}
# Create application
curl --location --request POST '127.0.0.1:5000/v1/application/'${app_name}'' \
--header 'Content-Type: application/json' \
--data-raw '{
"fields":{
        "'${field_name}'": {
                "type": "object",
                "pipeline": "'${pipeline_name}'"
        }
},
"s3Buckets": "'${s3_bucket}'"
}'

## upload & search
data_path='/tmp/256_ObjectCategories'
search_url='https://tse2-mm.cn.bing.net/th/id/OIP.d0Uth461I3nJDr28WXudhgHaHa?w=204&h=189&c=7&o=5&dpr=2&pid=1.7'

python3 load_data.py -s 127.0.0.1:5000 -a ${app_name} -p ${pipeline_name} -d ${data_path}

curl --location --request POST '127.0.0.1:5000/v1/application/'${app_name}'/search' \
--header 'Content-Type: application/json' \
--data-raw '{
        "fields": {
            "'${field_name}'": {
                "url": "'${search_url}'"
            }
    },
    "topk": 10,
    "nprobe": 20
}'