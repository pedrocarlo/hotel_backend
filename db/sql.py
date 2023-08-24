from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
import os
from os import path
import locale
from db.model import User, Nfe
from sefaz.xml_parser import get_tags

locale.setlocale(locale.LC_TIME, "pt_BR.UTF-8")
locale.setlocale(locale.LC_MONETARY, "pt_BR.UTF-8")


cwd = os.getcwd()

db_name = "notas"
db_user = "sa"
db_pass = "1234"
db_host = "db"
db_port = "5432"

engine = "postgresql://{}:{}@{}:{}/{}".format(
    db_user, db_pass, db_host, db_port, db_name
)

engine = create_engine(engine, echo=True)
print(engine)

Session = sessionmaker(bind=engine)

def get_session():
    return Session()

def get_xml_chave(chave: str):
    with Session() as session:
        session.scalars(select(Nfe).where(Nfe.chave == chave)).one()
        pass


def insert_xml_from_folder(folder) -> Nfe:
    session = Session()
    try:
        files = os.listdir(folder)
        for filename in files:
            nota = get_tags(path.join(folder, filename))
            session.add(nota)
        # fail whole operation if cannot add everything together
        # TODO see if i want to change this behavior
        session.commit()
    finally:
        session.close()


# insert_xml_from_folder(cwd + "/" + "xml/completa")
