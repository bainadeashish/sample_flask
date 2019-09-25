FROM python:3.5
RUN apt-get update -y
RUN apt-get install -y vim
COPY . /code/
WORKDIR /code
RUN pip install -r requirements.txt
ENTRYPOINT ["sh", "start.sh"]