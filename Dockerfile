# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.11.4-slim-bookworm

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update && apt-get install -y gcc libpq-dev tzdata mono-mcs \
    locales rabbitmq-server && rm -rf /var/lib/apt/lists/* && \
    cp /usr/share/zoneinfo/America/Sao_Paulo /etc/localtime

ENV TZ America/Sao_Paulo
ENV LANG pt_BR.UTF-8
ENV LANGUAGE pt_BR.UTF-8
ENV LC_ALL pt_BR.UTF-8

# Install pip requirements
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

RUN locale-gen pt_BR.UTF-8
ENV LANG=pt_BR.UTF-8
RUN sed -i -e "s/# $LANG.*/$LANG UTF-8/" /etc/locale.gen && \
    dpkg-reconfigure --frontend=noninteractive locales && \
    update-locale LANG=$LANG LC_ALL=${LANG} LC_TIME=${LANG} LC_MONETARY=${LANG}

WORKDIR /app
COPY . /app


ENV PYTHONPATH /app
# ENV DATABASE_URL=postgresql+psycopg2://sa:1234@db:5432/notas

# RUN alembic revision --autogenerate -m "First migration"

# RUN ./alembic_setup.sh

COPY ./celery /app/celery
# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser


# COPY alembic_env.py dest
# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
# ENTRYPOINT [ ]
CMD ./alembic_setup.sh && ./celery/init_worker.sh && python ./hotel_api/main.py

