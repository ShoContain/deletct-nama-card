FROM python:3.9.11-buster
RUN apt update && apt install -y libgl1-mesa-dev
COPY ./requirements/ /requirements/
RUN pip install -r /requirements/prod.txt  && \ 
    pip install -r /requirements/dev.txt && \
    rm -rf  /requirements/
