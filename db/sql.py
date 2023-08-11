from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
import locale
from model import User, Nfe

locale.setlocale(locale.LC_TIME, "pt_BR.UTF-8")
locale.setlocale(locale.LC_MONETARY, "pt_BR.UTF-8")


cwd = os.getcwd()

db_name = "notas"
db_user = "docker"
db_pass = "1234"
db_host = "db"
db_port = "5432"

engine = "postgresql://{}:{}@{}:{}/{}".format(
    db_user, db_pass, db_host, db_port, db_name
)

engine = create_engine(engine, echo=True)
print(engine)

Session = sessionmaker(bind=engine)
session = Session()
session.close()


def insert_xml_from_folder(folder):
    for filepath in folder:
        print(filepath)
