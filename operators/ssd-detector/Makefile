COMMIT_ID = $(shell git rev-parse --short HEAD)
GIT_TAG = $(shell git tag --points-at HEAD)


ifeq ($(GIT_TAG), )
  TAG=$(COMMIT_ID)
else
  TAG=$(GIT_TAG)
endif
cpu:
	docker build  \
 	--build-arg base_tag=ubuntu:bionic-20200219 \
 	-t psoperator/ssd-detector:$(TAG) \
 	-f Dockerfile .

gpu:
	docker build  \
 	--build-arg base_tag=nvidia/cuda:10.0-cudnn7-devel-ubuntu18.04 \
 	-t psoperator/ssd-detector-gpu:$(TAG) \
 	-f Dockerfile-gpu .
