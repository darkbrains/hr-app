FROM python:3.9-slim

WORKDIR /app

COPY bin/app/requirements.txt .

RUN pip install -r requirements.txt

COPY /bin/app .

RUN mkdir /tmp/prometheus_multiproc_dir

CMD ["python3", "main.py"]

EXPOSE 8085
