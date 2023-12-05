import os
from sqlalchemy import (
    ForeignKey,
    Column,
    String,
    Integer,
    Float,
    Boolean,
    DateTime,
    text,
)
from sqlalchemy.orm import declarative_base
import datetime
import secrets
import locale

locale.setlocale(locale.LC_TIME, "pt_BR.utf8")

Base = declarative_base()


class Nfe(Base):
    __tablename__ = "nfe"
    chave = Column("chave", String(44), primary_key=True, autoincrement=False)
    cnpj_comprador = Column(
        "cnpj_comprador",
        String(14),
        server_default=text("51548782000139"),
        default=text("51548782000139"),
        nullable=False,
    )
    cnpj_vendedor = Column("cnpj_vendedor", String(14))
    nome = Column("nome", String)
    total = Column("total", Float)
    date = Column("date", DateTime)
    completa = Column("completa", Boolean)
    # TODO no futuro se quiser saber qual tipo de manifestacao foi feita adicionar check aqui para todas as operacoes
    # TODO por enquanto so vai ser utilizado ciencda emissao ou operacao para notas mais antigas
    manifestada = Column("manifestada", Boolean)
    manifestando = Column("manifestando", Boolean)
    desbravador = Column("desbravador", Boolean)  # foi adicionado no desbravador ou nao
    irrelevant = Column("irrelevate", Boolean)

    def __init__(
        self,
        chave: str,
        cnpj_comprador: str,
        cnpj: str,
        nome: str,
        total: float,
        date: datetime.datetime,
        completa: bool = False,
        manifestada: bool = False,
        manifestando: bool = False,
        desbravador: bool = False,
        irrelevant: bool = False,
    ):
        self.chave = chave
        self.cnpj_comprador = cnpj_comprador
        self.cnpj_vendedor = cnpj
        self.nome = nome
        self.total = total
        self.date = date
        self.completa = completa
        self.manifestada = manifestada
        self.manifestando = manifestando
        self.desbravador = desbravador
        self.irrelevant = irrelevant

    def __repr__(self):
        return f"{self.chave[:10]} {self.cnpj_vendedor} {self.nome[:15]} {self.date} \
              {'completa' if self.completa else 'resumida'} \
                manifestada:{self.manifestada} \
                desbravador:{self.desbravador}"

    def get_folder(self):
        if self.irrelevant:
            folder = "outros"
        elif self.completa:
            folder = "completa"
        else:
            folder = "resumida"
        return folder

    def get_path(self):
        return os.path.join(os.getcwd(), "xml", self.get_folder(), f"{self.chave}.xml")


class User(Base):
    __tablename__ = "user"
    id = Column("id", Integer, primary_key=True)
    admin = Column(
        "admin",
        Boolean,
        nullable=False,
        server_default=text("false"),
        default=text("false"),
    )
    nome = Column("nome", String, nullable=False)
    # TODO lembrar de hash a senha dos users
    password = Column("senha", String, nullable=False)
    ativo = Column("ativo", Boolean, nullable=False)
    token = Column("token", String)
    token_expiracao = Column("token_expiracao", DateTime)

    def __init__(self, nome: str, password: str):
        self.nome = nome
        self.password = password
        self.ativo = True
        self.token = secrets.token_hex(16)
        # a principio esta timezone Brasil
        self.token_expiracao = datetime.datetime.now() + datetime.timedelta(days=5)


class Certificado(Base):
    __tablename__ = "certificados"
    id = Column("id", Integer, primary_key=True)
    cnpj = Column("cnpj", String)
    nsu = Column("ult_nsu", Integer)
    caminho = Column("caminho", String)
    validade = Column("validade", DateTime)

    def __init__(self, cnpj: str, nsu: int, caminho: str, validade: datetime.datetime):
        self.cnpj = cnpj
        self.nsu = nsu
        self.caminho = caminho
        self.validade = validade
