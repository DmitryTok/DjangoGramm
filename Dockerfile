FROM python:3

WORKDIR code/

COPY requirements.txt /code/

RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . /code/