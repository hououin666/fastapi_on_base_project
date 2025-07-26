FROM python:3.12.3

WORKDIR /app

COPY app/requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY app .

CMD ["python", "main.py"]