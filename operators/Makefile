MAKEFILE_PATH=$(abspath $(lastword $(MAKEFILE_LIST)))
CURRENT_DIR=$(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))
protoc:
	echo $(CURRENT_DIR)
	python -m grpc_tools.protoc -I $(CURRENT_DIR)/rpc/ $(CURRENT_DIR)/rpc/rpc.proto --python_out=$(CURRENT_DIR)/rpc --grpc_python_out=$(CURRENT_DIR)/rpc


