FROM python:3.9.0-alpine

RUN mkdir /app
WORKDIR /app

RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["sh", "./runserver.sh"]
