FROM python:3.6.7-slim-jessie

ADD requirements.txt /
RUN pip install --no-cache-dir -r requirements.txt

ADD jsonhandler.py /
ADD main.py /

ENTRYPOINT ["gunicorn", "--bind=0.0.0.0:5000", "--access-logfile=-", "main:app"]

EXPOSE 5000
