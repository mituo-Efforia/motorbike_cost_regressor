FROM python:3.10.12

WORKDIR /app
#Linuxのコマンドをアップデート　
RUN apt-get update \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    #pipのアップデート
    && pip install --upgrade pip

COPY ./docker/python/requirements.txt /tmp

RUN pip install --no-cache-dir -r /tmp/requirements.txt
