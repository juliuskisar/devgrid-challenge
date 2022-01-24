FROM python:3.9

RUN mkdir /app

WORKDIR /app

ADD requirements.txt /app/

RUN pip install -r requirements.txt

ADD . /app/

RUN rm -rf venv

RUN pytest test_main.py

EXPOSE 8080

# VOLUME ["/app/logs"]

CMD ["gunicorn", "-b", "0.0.0.0:8080", "-w", "1", "--reload", "main:app"]