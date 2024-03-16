FROM python:3.10-slim-bullseye

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

RUN python3 manage.py migrate && python3 manage.py makemigrations

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8080"]
