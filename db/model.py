from sqlalchemy import (
    ForeignKey,
    Column,
    String,
    Integer,
    Float,
    Boolean,
    DateTime,
)
from sqlalchemy.orm import declarative_base
import datetime

Base = declarative_base()


class Nfe(Base):
    __tablename__ = "nfe"
    chave = Column("chave", String(44), primary_key=True, autoincrement=False)
    cnpj = Column("cnpj", String(14))
    nome = Column("nome", String)
    total = Column("total", Float)
    date = Column("date", DateTime)
    completa = Column("completa", Boolean)
    # TODO no futuro se quiser saber qual tipo de manifestacao foi feita adicionar check aqui para todas as operacoes
    # TODO por enquanto so vai ser utilizado ciencda emissao ou operacao para notas mais antigas
    manifestada = Column("manifestada", Boolean)
    desbravador = Column("desbravador", Boolean)  # foi adicionado no desbravador ou nao
    irrelevant = Column('irrelevate', Boolean)
    
    def __init__(
        self,
        chave: str,
        cnpj: str,
        nome: str,
        total: float,
        date: datetime.datetime,
        completa: bool = False,
        manifestada: bool = False,
        desbravador: bool = False,
        irrelevant: bool = False,
    ):
        self.chave = chave
        self.cnpj = cnpj
        self.nome = nome
        self.total = total
        self.date = date
        self.completa = completa
        self.manifestada = manifestada
        self.desbravador = desbravador
        self.irrelevant = irrelevant

    def __repr__(self):
        return f"{self.chave[:10]} {self.cnpj} {self.nome[:15]} {self.date} \
              {'resumida' if self.completa else 'completa'} \
                manifestada:{self.manifestada} \
                desbravador:{self.desbravador}"
                
    def get_path(self):
        pass


class User(Base):
    __tablename__ = "user"
    id = Column("id", Integer, primary_key=True)
    nome = Column("nome", String)
    # TODO lembrar de hash a senha dos users
    senha = Column("senha", String)

    def __init__(self, nome: str, senha: str):
        self.nome = nome
        self.senha = senha
