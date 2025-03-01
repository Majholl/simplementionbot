FROM python:latest


WORKDIR /app

COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install  -r /app/requirements.txt




COPY scr  /app/scr

WORKDIR /app/scr



CMD ["sh", "-c", "[ python == '3.11' ] && python app.py"]
