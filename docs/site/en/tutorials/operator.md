# What is an operator?

An operator is an abstract of a basic unit within Phantoscope. An example of an operator is that a unit within Phantoscope can be created according to the operator.

The Phantoscope project can complete different tasks because of the diversity of the operators it has.

You can follow our [instructions](../../../../operators/HowToAddAnOperator.md) to implement your own operator and add it to your Phantoscope project. 

Depending on its function, an operator can be classified into two types: processor and encoder. 

## Processor
Processors take up a larger portion of the operators in an application. A processor only processes the data that it is fed. When it is done, the pipeline takes its output to the next operator down the line. 

Generally speaking, the input to a processor has the same format as its output. For example, a processor takes in an image, extracts human face from it, and then sends out the extracted information. 

A processor only receives, processes, and sends out data, no matter where it receives from or sends out to.

Phantoscope has the following types of in-built processors: 

#### MTCNN-face-detector

- **Docker image:** face-detector
- **Function:** Detects human faces from an image. 
- **Input:** An image.
- **Output:** A group of detected human face images. 
- **Sample pipeline:** mtcnn-face-detector -> face-encoder

> It is implemented using [Facenet](https://github.com/davidsandberg/facenet.git).

#### Mask-RCNN-object-detector

- **Docker image:** mask-rcnn-detector
- **Function:** Detects objects from an image. 
- **Input:** An image.
- **Output:** A group of detected object images. 
- **Sample pipeline:** mask-rcnn-object-detetcor -> vgg/xception

> It is implemented using [Mask_RCNN](https://github.com/matterport/Mask_RCNN).

#### SSD-object-detector

- **Docker image:** ssd-detector
- **Function:** Detects objects from an image. 
- **Input:** An image.
- **Output:** A group of detected object images. 
- **Sample pipeline:** ssd-object-detector -> vgg/xception

> It is implemented using [Tensorflow SSD](https://github.com/scanner-research/scannertools/blob/master/scannertools/scannertools/object_detection.py).

#### YOLOv3-object-detector

- **Docker image:** yolov3-detector
- **Function:** Detects objects from an image. 
- **Input:** An image.
- **Output:** A group of detected object images.
- **Sample pipeline:** yolov3-object-detector -> vgg/xception

> It is implemented using [Paddlepaddle Yolov3](https://github.com/PaddlePaddle/PaddleDetection).

## Encoder

You can take an encoder as a special processor. The difference between an encoder and a processor includes: 

The input to an encoder is in a different format from its output.

An encoder converts unstructured data to vectors or tags.

So an encoder is the last link in processing data. 

Phantoscope has the following types of in-built encoders: 

#### Vgg16

- **Docker image:** vgg16-encoder
- **Vector dimension:** 512
- **Function:** Does embedding to the input image and gets the feature vectors.

> It is implemented using [Keras Vgg16](https://keras.io/zh/applications/).

#### Xception

- **Docker image:** xception-encoder
- **Vector dimension:** 2048
- **Function:** Does embedding to the input image and gets the feature vectors.

> It is implemented using [Keras Xception](https://keras.io/zh/applications/).

#### Face-encoder

- **Docker image:** face-encoder
- **Vector dimension:** 128
- **Function:** Does embedding to the output human face images and gets the feature vectors.

> It is implemented using [Facenet](https://github.com/davidsandberg/facenet.git).


## Register an operator to Phantoscope

Phantoscope does not start up with an operator. For this version, you must manually register an operator to Phantoscope first using the following command.

`addr` is the address pulled by the operator, which can be understood as the docker image address in the following command.

```bash
$ curl --location --request POST '127.0.0.1:5000/v1/operator/register' \
--header 'Content-Type: application/json' \
--data '{
    "name": "face_detector",
    "addr": "psoperator/face-detector:latest",
    "author" :"phantoscope",
    "type":"processor",
    "description": "detect face in input images",
    "version": "0.1.0"
}'
```

## Create an operator instance

After you successfully registered an operator, you also need to create an instance according to the operator as the actual unit that Phantoscope works on.

For this version, you can create an operator instance using the following command.

```bash
$ curl --location --request POST '127.0.0.1:5000/v1/operator/face_detector/instances' \
--header 'Content-Type: application/json' \
--data '{
    "instanceName": "face_detector1" 
}'
```

The first creation pulls the Docker image from the remote, which takes relatively long. When the creation is successful, a container of the image appears on the local machine.

```bash
CONTAINER ID        IMAGE                                       COMMAND                  CREATED             STATUS              PORTS                                                NAMES
67b697aad41b        psoperator/face-detector:latest             "python3 server.py"      26 seconds ago      Up 25 seconds       51001/tcp, 0.0.0.0:32768->80/tcp                     phantoscope_face_detector_face_detector1
```


# Design Principles of an Operator

An operator is stateless. 

An operator should be standalone and reusable. 

An operator is self-dependent and does not require an external storage. 
