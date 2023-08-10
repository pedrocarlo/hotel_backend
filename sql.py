from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, CHAR
from sqlalchemy.orm import sessionmaker, declarative_base
import os
cwd = os.getcwd()


Base = declarative_base()

db_name = 'notas'
db_user = 'docker'
db_pass = '1234'
db_host = 'db'
db_port = '5432'

# Connecto to the database
engine = 'postgresql://{}:{}@{}:{}/{}'.format(db_user, db_pass, db_host, db_port, db_name)
print(engine)
# engine = create_engine("postgresql://docker:1234@localhost:/notas")

