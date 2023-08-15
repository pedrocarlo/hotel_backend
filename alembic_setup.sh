#!/bin/sh

DIR=./alembic
if [ ! -d "$DIR" ];
then
    alembic init alembic
    cp ./alembic_env.py ./alembic/env.py
    alembic revision --autogenerate -m "First migration"
    echo "Created $DIR and first revision"
fi
