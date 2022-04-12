FROM python:3.9.11-buster
RUN apt update && apt install -y libgl1-mesa-dev
COPY . /server
WORKDIR /server
RUN pip install -r requirements/prod.txt
ENTRYPOINT make start