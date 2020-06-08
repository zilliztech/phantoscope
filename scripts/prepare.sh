# get the local addr
LOCAL_ADDRESS=$(ip a | grep -Eo 'inet (addr:)?([0-9]*\.){3}[0-9]*' | grep -Eo '([0-9]*\.){3}[0-9]*' | grep -v '127.0.0.1'| head -n 1)

data="{\"endpoint\":\"$LOCAL_ADDRESS:50001\",\"name\":\"vgg16\"}"

# Regist operators named vgg16
curl --location --request POST '127.0.0.1:5000/v1/operator/regist' \
--header 'Content-Type: application/json' \
--data $data


# Create pipeline with registed operator vgg16
curl --location --request POST '127.0.0.1:5000/v1/pipeline/example' \
--header 'Content-Type: application/json' \
--data "{
        \"input\": \"image\",
        \"description\": \"pipeline example\",
        \"processors\": \"\",
        \"encoder\": \"vgg16\",
        \"indexFileSize\": 1024
}"


# Create application and use the pipeline which above created
curl --location --request POST '127.0.0.1:5000/v1/application/example' \
--header 'Content-Type: application/json' \
--data "{
\"fields\":{
        \"example\": {
                \"type\": \"object\",
                \"pipeline\": \"example\"
        }
},
\"s3Buckets\": \"example\"
}"
