#!/bin/bash -ex
## model url from facenet
url='https://storage.googleapis.com/esper/models/facenet/20170512-110547.tar.gz'
file='20170512-110547.tar.gz'
dir='20170512-110547'

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
