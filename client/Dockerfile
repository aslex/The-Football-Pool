FROM python:stretch

COPY . /client

WORKDIR /client

RUN npm install
RUN npm install 'react-router-dom'

ENTRYPOINT [ "npm", "start" ]