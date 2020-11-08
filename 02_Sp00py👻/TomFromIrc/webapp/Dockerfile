FROM python:3

WORKDIR /usr/src/app

ADD app ./
RUN pip install --no-cache-dir -r requirements.txt
RUN useradd -U gunicorn
CMD gunicorn --config=gunicorn.conf.py wsgi:app
