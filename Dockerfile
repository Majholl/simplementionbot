FROM python:alpine


WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip && pip install  -r requirements.txt


COPY scr  .


CMD ["python", "main.py"]
