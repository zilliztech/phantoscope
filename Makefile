COMMIT_ID = $(shell git rev-parse --short HEAD)
GIT_TAG = $(shell git tag --points-at HEAD)

.PHONY: api test lint release
all: test lint api clean
api:
	docker build -t phantoscope/api-server:$(COMMIT_ID) .
env:
	LOCAL_ADDRESS=$(shell ip a | grep -Eo 'inet (addr:)?([0-9]*\.){3}[0-9]*' | grep -Eo '([0-9]*\.){3}[0-9]*' | grep -v '127.0.0.1'| head -n 1) docker-compose -f docker-compose-test.yml up -d
test:
	PYTHONPATH=$(shell pwd)/search pytest tests --cov=./
lint:
	PYTHONPATH=$(shell pwd)/search pylint --rcfile=pylint.conf search --msg-template='{msg_id}:{line:3d},{column}: {obj}: {msg}' --exit-zero > lintoutput
	echo $(shell tail -2 lintoutput | grep -P "\d+" -o |sed -n "1p").$(shell tail -2 lintoutput | grep -P "\d+" -o |sed -n "2p")
clean:
	rm -rf .pytest_cache
	rm -rf lintoutput

ifeq ($(GIT_TAG), )
  TAG=$(COMMIT_ID)
else
  TAG=$(GIT_TAG)
endif

release:
	docker build -t phantoscope/api-server:$(TAG)

login:
	docker login -u phantoscope -p $(DOCKERHUB_TOKEN)
push: login
	docker push phantoscope/api-server:$(TAG)
