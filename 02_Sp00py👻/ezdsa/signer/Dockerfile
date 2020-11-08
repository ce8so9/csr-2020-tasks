from python:3.6

WORKDIR /usr/src/app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY secp256k1-key.pem .
COPY main.py .

CMD ["python", "main.py"]
