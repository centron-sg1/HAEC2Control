FROM python:3.12-alpine

WORKDIR /app

RUN apk add --no-cache \
    jq

RUN pip install --no-cache-dir \
    flask \
    boto3

COPY app.py .
COPY run.sh .


RUN chmod +x run.sh

CMD ["./run.sh"]
