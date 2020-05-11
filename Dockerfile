# mkdir tmp/video
From ubuntu:bionic-20200219
RUN mkdir -p /app/tmp

COPY search /app
COPY requirements.txt /app/requirements.txt

WORKDIR /app


RUN sed -i 's/archive.ubuntu.com/mirrors.aliyun.com/g' /etc/apt/sources.list

RUN apt-get update && apt-get install -y \
	python3 \
	python3-pip \
	gunicorn3 \
	libglib2.0-0 \
	libsm6 \
	libxext6 \
	libxrender1 \
        libmysqlclient-dev \
	&& apt-get clean \
	&& rm -rf /var/lib/apt/lists/*


RUN pip3 install -r /app/requirements.txt  -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com

CMD ["/usr/bin/gunicorn3", "-w", "4", "-b", "0.0.0.0:5000", "main:app"]
