FROM docker.io/darkbrains/python:3.12.3

WORKDIR /app

COPY bin/app/requirements.txt .

RUN pip3.12 install --no-cache-dir -r requirements.txt

COPY /bin/app .

CMD ["python3", "main.py"]

EXPOSE 8085
