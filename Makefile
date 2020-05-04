all:api
	echo "build finish"
api:
	docker build -t milvus.io/om-search:v1 .
test:
	export PYTHONPATH=$(pwd)/search
	pytest tests
lint:
	pylint --rcfile=pylint.conf search --msg-template='{msg_id}:{line:3d},{column}: {obj}: {msg}'
