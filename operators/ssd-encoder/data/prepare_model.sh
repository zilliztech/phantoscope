#!/bin/bash -ex
## model url from facenet
url='http://download.tensorflow.org/models/object_detection/ssd_mobilenet_v1_coco_2017_11_17.tar.gz'
file='ssd_mobilenet_v1_coco_2017_11_17.tar.gz'
dir='ssd_mobilenet_v1_coco_2017_11_17'

if [[ ! -d "${dir}" ]]; then
    if [[ ! -f "${file}" ]]; then
        echo "[INFO] Model tar package does not exist, begin to download..."
        wget ${url}
        echo "[INFO] Model tar package download successfully!"
    fi

    echo "[INFO] Model directory does not exist, begin to untar..."
    tar -zxvf ${file}
    rm ${file}
    echo "[INFO] Model directory untar successfully!"
fi

if [[ -d "${dir}" ]];then
    echo "[INFO] Model has been prepared successfully!"
    exit 0
fi

echo "[ERROR] Failed to prepare model due to unexpected reason!"
exit 1
