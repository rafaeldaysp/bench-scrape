FROM python:3.10

WORKDIR /app

COPY . ./

COPY docker-main.py /app/main.py

RUN pip install -r requirements.txt

CMD ["python", "./main.py", "--aliexpress"]