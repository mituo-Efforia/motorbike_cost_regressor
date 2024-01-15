FROM python:3.10.12

COPY ./docker/python/requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt
WORKDIR /app
CMD [ "--host", "0.0.0.0", "--port", "8000", "--reload"]