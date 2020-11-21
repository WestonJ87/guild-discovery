
FROM python:3.8

COPY . .

RUN pip install -r ./guild-discovery/requirements.txt
EXPOSE 5000

RUN chmod +x ./entrypoint.sh

ENTRYPOINT [ "./entrypoint.sh" ]