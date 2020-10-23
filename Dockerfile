FROM python:3.8.3-alpine

RUN apk add git gcc musl-dev libffi-dev openssl-dev

RUN mkdir /app
WORKDIR /app

RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["sh", "./runserver.sh"]
