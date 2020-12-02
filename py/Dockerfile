
FROM python:3.8

COPY . .

ARG REBUILD_DATABASE
ENV REBUILD_DATABASE=$REBUILD_DATABASE

ENV FLASK_APP=./guild-discovery/index.py

RUN pip3 install -r ./guild-discovery/requirements.txt

RUN chmod +x ./entrypoint.sh

ENTRYPOINT [ "/bin/bash", "./entrypoint.sh",  "REBUILD_DATABASE"]