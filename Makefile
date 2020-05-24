COMMIT_ID = $(shell git rev-parse --short HEAD)
GIT_TAG = $(shell git tag --points-at HEAD)

.PHONY: api test lint release
all: test lint api clean
api:
	docker build -t milvus.io/om-search:$(COMMIT_ID) .
test: lint
	PYTHONPATH=$(shell pwd)/search pytest tests
lint:
	PYTHONPATH=$(shell pwd)/search pylint --rcfile=pylint.conf search --msg-template='{msg_id}:{line:3d},{column}: {obj}: {msg}' --exit-zero > lintoutput
	echo $(shell tail -2 lintoutput | grep -P "\d+" -o |sed -n "1p").$(shell tail -2 lintoutput | grep -P "\d+" -o |sed -n "2p")
clean:
	rm -rf .pytest_ca[]che
	rm -rf lintoutput

ifeq ($(GIT_TAG), )
  TAG=$(COMMIT_ID)
else
  TAG=$(GIT_TAG)
endif

release:
	docker build -t milvus.io/om-search:$(TAG)
