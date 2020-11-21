
FROM python:3.8

COPY . .

ARG REBUILD_DATABASE
ENV REBUILD_DATABASE=$REBUILD_DATABASE

RUN pip install -r ./guild-discovery/requirements.txt
EXPOSE 5000

RUN chmod +x ./entrypoint.sh

ENTRYPOINT [ "/bin/bash", "./entrypoint.sh",  "REBUILD_DATABASE"]