MAKEFILE_PATH=$(abspath $(lastword $(MAKEFILE_LIST)))
CURRENT_DIR=$(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))
protoc:
	echo $(CURRENT_DIR)
	python -m grpc_tools.protoc -I $(CURRENT_DIR)/rpc/ $(CURRENT_DIR)/rpc/rpc.proto --python_out=$(CURRENT_DIR)/rpc --grpc_python_out=$(CURRENT_DIR)/rpc

ifeq ($(GIT_TAG), )
  TAG=$(COMMIT_ID)
else
  TAG=$(GIT_TAG)
endif

# todo: read tag from dir


cpu:
	for i in face-encoder vgg16-encoder; \
	do \
		cd $$i; \
		echo `pwd` ; \
		make cpu; \
		cd -; \
	done

gpu:
	for i in face-encoder vgg16-encoder; \
	do \
		cd $$i; \
		echo `pwd` ; \
		make gpu; \
		cd -; \
	done

login:
	docker login -u psoperator -p $(DOCKERHUB_TOKEN)

push: login
	for i in face-encoder vgg16-encoder; \
	do \
		cd $$i; \
		echo `pwd` ; \
		tag=`cat version`; \
		docker push psoperator/$$i:$$tag; \
		cd -; \
	done


