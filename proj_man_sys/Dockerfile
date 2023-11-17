
FROM python:3.10.4

RUN mkdir /code

COPY requirements.txt /code

RUN pip install -r /code/requirements.txt

COPY . /code

CMD python /code/manage.py runserver localhost:8000