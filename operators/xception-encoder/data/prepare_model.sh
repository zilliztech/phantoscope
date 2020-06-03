#!/bin/bash -ex
## model url from facenet
file='xception_weights_tf_dim_ordering_tf_kernels_notop.h5'
url='https://github.com/fchollet/deep-learning-models/releases/download/v0.4/xception_weights_tf_dim_ordering_tf_kernels_notop.h5'

if [[ ! -f "${file}" ]]; then
    echo "[INFO] Model tar package does not exist, begin to download..."
    wget ${url}
    echo "[INFO] Model tar package download successfully!"
fi

if [[ -f "${file}" ]];then
    echo "[INFO] Model has been prepared successfully!"
    exit 0
fi

echo "[ERROR] Failed to prepare model due to unexpected reason!"
exit 1
