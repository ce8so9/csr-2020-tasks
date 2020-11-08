from python:3.6

WORKDIR /usr/src/app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY pub.pem .
COPY flag.py .
COPY main.py .

CMD ["python", "main.py"]
