#!/bin/bash -ex
## model url from mask_rcnn https://github.com/matterport/Mask_RCNN
url='https://github.com/matterport/Mask_RCNN/releases/download/v2.0/mask_rcnn_coco.h5'
file='mask_rcnn_coco.h5'

if [[ ! -f "${file}" ]]; then
    echo "[INFO] Model does not exist, begin to download..."
    wget ${url}
    echo "[INFO] Model download successfully!"
fi

if [[ -f "${file}" ]]; then

    echo "[INFO] Model has been prepared!"
    exit 0
fi
echo "[ERROR] Failed to prepare model due to unexpected reason!"
exit 1
