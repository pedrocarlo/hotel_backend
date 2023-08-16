#!/bin/bash

DIR=./alembic
if [ ! -d "$DIR" ]
then
    mkdir tmp
    cd tmp
    alembic init alembic
    cp -R ./alembic /app/alembic
    cd .. && rm -rf tmp
fi
cd /app
cp ./alembic_env.py ./alembic/env.py
sleep 5 && alembic revision --autogenerate -m "First migration" \
&& alembic upgrade head && echo "Created $DIR and first revision"

