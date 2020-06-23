# What is an operator?

An operator is a basic unit within Phantoscope. 

The Phantoscope project can complete different tasks because of the diversity of the operators it has.

You can follow our instructions to implement your own operator and add it to your Phantoscope project. 

Depending on its function, an operator can be classified into two types: processor and encoder. 

## Processor
Processors take up a larger portion of the operators in an application. A processor only processes the data that it is fed. When it is done, the pipeline takes its output to the next operator down the line. 

Generally speaking, the input to a processor has the same format as its output. For example, a processor takes in an image, extracts human face from it, and then send out the extracted information. 

Phantoscope has the following in-built processors: 

#### MTCNN-face-detector

- **Docker image:** face-detector
- **Function:** Detects human faces from an image. 
- **Input:** An image
- **Output:** A group of detected human face images. 
- **Sample pipeline:** mtcnn_detect_face -> face_embedding

> It is implemented using [Facenet](https://github.com/davidsandberg/facenet.git).

#### Mask-RCNN-object-detector

- **Docker image:** mask-rcnn-detector
- **Function:** Detects objects from an image. 
- **Input:** An image
- **Output:** A group of detected object images. 
- **Sample pipeline:** mask_rcnn -> vgg/xception

> It is implemented using [Mask_RCNN](https://github.com/matterport/Mask_RCNN).

#### SSD-object-detector

- **Docker image: ** ssd-detector
- **Function: ** Detects objects from an image. 
- **Input: ** An image
- **Output: ** A group of detected object images. 
- **Sample pipeline:** ssd-object-detector -> vgg/xception

> It is implemented using [Tensorflow SSD](https://github.com/scanner-research/scannertools/blob/master/scannertools/scannertools/object_detection.py),

#### YOLOv3-object-detector

- **Docker image:** yolov3-detector
- **Function:** Detects objects from an image. 
- **Input:** An image
- **Output:** A group of detected object images.
- **Sample pipeline:** yolov3-object-detector -> vgg/xception

> It is implemented using [Paddlepaddle Yolov3](https://github.com/PaddlePaddle/PaddleDetection).

## Encoder

An encoder is the last link in the pipeline. You can take an encoder as a special processor. The difference between an encoder and a processor includes: 

An encoder converts unstructured data to vectors or tags, so the input to an encoder is in a different format from its output.

Phantoscope has the following in-built processors: 

#### Vgg16

- **Docker image:** vgg16-encoder
- **Vector dimension: ** 512
- **Function: ** Does embedding to the input image and gets the feature vectors.

> It is implemented using [Keras Vgg16](https://keras.io/zh/applications/).

#### Xception

- **Docker image: ** xception-encoder
- **Vector dimension: ** 2048
- **Function: ** Does embedding to the input image and gets the feature vectors.

> It is implemented using [Keras Xception](https://keras.io/zh/applications/).

#### Face-encoder

- **Docker image: ** face-encoder
- **Vector dimension: ** 128
- **Function: ** Does embedding to the output human face images and gets the feature vectors.

> It is implemented using [Facenet](https://github.com/davidsandberg/facenet.git).

## Run an Operator

```bash
$ export LOCAL_ADDRESS=$(ip a | grep -Eo 'inet (addr:)?([0-9]*\.){3}[0-9]*' | grep -Eo '([0-9]*\.){3}[0-9]*' | grep -v '127.0.0.1'| head -n 1)
# Pull the docker image of the corresponding version. 
$ docker pull psoperator/face-encoder:latest
# Start up a container with the downloaded docker image and configure the container settings: 
# 1. Set the container serviceendpoint to ${LOCAL_ADDRESS}:50004, and map the 50004 port to the local machine.
# 2. Map the container's /app/tmp directory to the local machine to facilitate checking and debugging the cached images in the encoder. 
$ docker run -p 50004:50004 -e OP_ENDPOINT=${LOCAL_ADDRESS}:50004 -v `pwd`/tmp:/app/tmp -d psoperator/face-encoder:latest
```

## Register an operator to Phantoscope


For this version, Phantoscope does not start up with an operator. To find and use an operator, you must manually register that operator to Phantoscope first. 

By default, Phantoscope starts a vgg16 operator when starting up and listening on the 50001 port. At this point, though vgg16 is started up, it is not registered to Phantoscope. 

Call `/v1/operator/regist` to send the register request: 

```json
{
    "endpoint": "LOCAL_HOST_IP:50001",
	"name": "vgg16_example"
}
```

Register vgg16 to Phantoscope in the name of **vgg16_example**. 

Phantoscope uses this endpoint to communicate with the operator, so you should set it to an intranet address starting off with 192 or 10, instead of setting it to 127.0.0.1. 


# Design Principles of an Operator

An operator is stateless. 

An operator should be standalone and reusable. 

An operator is self-dependent and does not require an external storage. 
