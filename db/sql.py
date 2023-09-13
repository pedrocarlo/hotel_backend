from sqlalchemy import create_engine, extract, select
from sqlalchemy.orm import sessionmaker, Session
import os
from os import path
import locale
from db.model import User, Nfe, Certificado
import db.schemas as schemas
from sefaz.xml_parser import get_tags
from typing import Optional, Annotated


locale.setlocale(locale.LC_TIME, "pt_BR.utf8")
locale.setlocale(locale.LC_MONETARY, "pt_BR.utf8")


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
curr_session = sessionmaker(bind=engine)


def get_session():
    return curr_session()


def get_by_chave(session: Session, chave: str):
    return session.query(Nfe).filter(Nfe.chave == chave).first()


def get_by_date(session: Session, year: int, month: int):
    return (
        session.query(Nfe)
        .filter(extract("year", Nfe.date) == year, extract("month", Nfe.date) == month)
        .all()
    )


def get_manifestando(session: Session):
    return (
        session.query(Nfe)
        .filter(
            Nfe.manifestando == True, Nfe.manifestada == False, Nfe.completa == False
        )
        .all()
    )


def get_manifestada(session: Session):
    return session.query(Nfe).filter(Nfe.manifestada == True).all()


def get_general(session: Session, params: schemas.NfeQueryParams):
    query = session.query(Nfe)
    if params.cnpj:
        query = query.filter(Nfe.cnpj == params.cnpj)
    if params.nome:
        query = query.filter(Nfe.nome.contains(params.nome))
    if params.total:
        query = query.filter(Nfe.total == params.total)
    if params.completa:
        query = query.filter(Nfe.completa == params.completa)
    if params.manifestada:
        query = query.filter(Nfe.manifestada == params.manifestada)
    if params.manifestando:
        query = query.filter(Nfe.manifestando == params.manifestando)
    if params.desbravador:
        query = query.filter(Nfe.desbravador == params.desbravador)
    if params.start_date and params.end_date:
        query = query.filter(Nfe.date.between(params.start_date, params.end_date))
    # TODO see if this limit will need to change
    return query.limit(500).all()


def add_certificados(session: Session):
    from sefaz.utils import get_certificados
    from sefaz.lerCertificado import get_validade

    certificados = get_certificados()
    for cert in certificados:
        cnpj = cert.cnpj
        nsu = 0
        caminho = cert.certificado
        validade = get_validade(cert)
        try:
            session.merge(Certificado(cnpj, nsu, caminho, validade))
            session.commit()
        finally:
            session.close()


def write_ult_nsu(session: Session, nsu: int, cnpj: str):
    try:
        query = session.query(Certificado).filter_by(cnpj=cnpj)
        query.first().nsu = nsu
        session.commit()
    finally:
        session.close()


def read_ult_nsu(session: Session, cnpj: str) -> int:
    query = session.query(Certificado).filter_by(cnpj=cnpj)

    return query.first().nsu


def insert_xml_from_folder(folder):
    session = get_session()
    try:
        files = os.listdir(folder)
        for filename in files:
            nota = get_tags(path.join(folder, filename))
            nota.cnpj_comprador = "51548782000139"
            session.merge(nota)
        # fail whole operation if cannot add everything together
        # TODO see if i want to change this behavior
        session.commit()
    finally:
        session.close()


# insert_xml_from_folder(cwd + "/" + "xml/completa")
