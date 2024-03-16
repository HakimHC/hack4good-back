FROM python:3.10-slim-bullseye

WORKDIR /app

COPY db-carrefour.csv /app
COPY db-dia.csv /app
COPY db-mercadona.csv /app

COPY requirements.txt /app
COPY .env /app
COPY data.csv /app
RUN pip install -r requirements.txt

COPY populator.py /app
RUN python3 populator.py

COPY app.py /app

CMD ["python3", "app.py"]
