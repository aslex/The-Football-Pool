FROM python:stretch

COPY . /api

WORKDIR /api

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install flask-cors
RUN pip install requests

ENTRYPOINT [ "gunicorn", "-b", ":8080", "main:APP" ]