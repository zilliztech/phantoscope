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


build:
	for op in $(REBUILD_OPERATORS); \
	do \
		cd $${op}; \
		echo `pwd` ; \
		make cpu gpu; \
		cd -; \
	done

login:
	docker login -u psoperator -p $(PS_DOCKERHUB_TOKEN)

push: login
	for op in $(REBUILD_OPERATORS); \
	do \
		cd $$op; \
		echo `pwd` ; \
		tag=`cat version`; \
		docker push psoperator/$${op}:$${tag}; \
		docker push psoperator/$${op}-gpu:$${tag}; \
		cd -; \
	done


