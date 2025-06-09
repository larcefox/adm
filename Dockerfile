FROM python:3.10

WORKDIR /idm

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y python3-dev \
    libpq-dev \
    uvicorn \
    vim 


ENV FASTIFY_ADDRESS=0.0.0.0
ENV FLASK_RUN_PORT=8200
ENV SECRET_KEY=eee900166eff16f6691ee02580e28086
ENV DEBUG=True
ENV APP_SETTINGS=config.DevelopmentConfig
ENV DATABASE_URL=postgresql+psycopg2://larce:Dronsy25@localhost:5432/adm
ENV FLASK_APP=src
ENV FLASK_DEBUG=1
ENV APP_NAME='qure'
ENV DB_SCHEMA='auth'

COPY . .

CMD python manage.py run
