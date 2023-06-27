FROM --platform=linux/arm64 python:3

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt && pip check

COPY goodwe-poller.py /app

ENTRYPOINT [ "python", "/app/goodwe-poller.py" ]
