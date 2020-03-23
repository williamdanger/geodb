FROM python:2-buster

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY app /app

COPY data /data

COPY seedDB.py .
COPY cleanDB.py .

CMD python app/main.py
