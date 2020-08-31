COMMIT_ID = $(shell git rev-parse --short HEAD)
GIT_TAG = $(shell git tag --points-at HEAD)


ifeq ($(GIT_TAG), )
  TAG=$(COMMIT_ID)
else
  TAG=$(GIT_TAG)
endif

TAG=$(shell cat version)

data1:
	cd data
	./prepare_model.sh
	cd -

cpu:
	docker build  \
 	--build-arg base_tag=ubuntu:bionic-20200219 \
 	-t psoperator/face-encoder:$(TAG) \
 	-f Dockerfile .

gpu:
	docker build  \
 	--build-arg base_tag=nvidia/cuda:10.0-cudnn7-devel-ubuntu18.04 \
 	-t psoperator/face-encoder-gpu:$(TAG) \
 	-f Dockerfile-gpu .
