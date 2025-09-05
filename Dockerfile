
FROM python:3.13

WORKDIR /app

# set environmet variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ./wallets_api ./wallets_api