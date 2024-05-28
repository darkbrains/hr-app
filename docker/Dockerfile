FROM docker.io/darkbrains/python:3.12.3arm64

WORKDIR /app

COPY bin/app/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY /bin/app .

CMD ["python3", "main.py"]

EXPOSE 8085
