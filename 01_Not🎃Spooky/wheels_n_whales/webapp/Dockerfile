FROM python:3

WORKDIR /usr/src/app

ADD app ./
RUN pip install --no-cache-dir -r requirements.txt
RUN useradd -U gunicorn
# RUN chown root:gunicorn /usr/src/app
RUN chmod -R 555 /usr/src/app
RUN ls -lah .
CMD gunicorn -b 0.0.0.0:8000 -u gunicorn -g gunicorn wsgi:app -t 2 -w 8