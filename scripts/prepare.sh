#/bin/bash -ex
# get the local addr
LOCAL_ADDRESS=$(ip a | grep -Eo 'inet (addr:)?([0-9]*\.){3}[0-9]*' | grep -Eo '([0-9]*\.){3}[0-9]*' | grep -v '127.0.0.1'| head -n 1)

echo 'Register operators named vgg16'
# Register operators named vgg16
curl --location --request POST ${LOCAL_ADDRESS}':5000/v1/operator/register' \
--header 'Content-Type: application/json' \
--data '{
    "name": "vgg_encoder",
    "addr": "psoperator/vgg16-encoder:latest",
    "author" :"phantoscope",
    "type":"encoder",
    "description": "vgg16 encoder",
    "version": "0.1.0"
}'

echo '\ncreate operator instance'
curl --location --request POST ${LOCAL_ADDRESS}':5000/v1/operator/vgg_encoder/instances/vgg_instance1' \
--header 'Content-Type: application/json'

echo '\nsleep 10s for instance warmup' && sleep 10


# Create pipeline with registered operator vgg16
echo 'Create pipeline with created instance vgg16'
curl --location --request POST ${LOCAL_ADDRESS}':5000/v1/pipeline/example_pipeline' \
--header 'Content-Type: application/json' \
--data '{
	"description":"pipeline example",
	"processors": [],
	"encoder": {
		"name": "vgg_encoder",
		"instance":"vgg_instance1"
	}
}'

# Create application with the pipeline created before
echo '\nCreate application with the created pipeline before'
curl --location --request POST ${LOCAL_ADDRESS}':5000/v1/application/example_app' \
--header 'Content-Type: application/json' \
--data '{
    "fields":{
        "example_field": {
            "type": "pipeline",
            "value": "example_pipeline"
        }
    },
    "s3Bucket": "example-s3"
}'