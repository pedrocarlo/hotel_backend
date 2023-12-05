import datetime
from pydantic import BaseModel, ConfigDict, Field
from typing import Annotated, Optional
from fastapi import Query
from decimal import Decimal

import pydantic


class NfeBase(BaseModel):
    chave: str
    cnpj: str
    nome: str
    total: str
    date: datetime.datetime
    completa: bool
    manifestada: bool
    manisfestando: bool
    desbravador: bool
    irrelevant: bool

    class Config:
        from_attributes = True


class NfeCreate(NfeBase):
    pass


class Config:
    arbitrary_types_allowed = True


# @pydantic.dataclasses.dataclass(config=Config)
class NfeQueryParams(BaseModel):
    model_config = ConfigDict(extra="ignore")

    cnpj_vendedor: Annotated[Optional[str], Query(min_length=11, max_length=14)] = None
    nome: Annotated[Optional[str], None] = None
    total: Annotated[Optional[Decimal], Query(ge=0)] = None
    start_date: Annotated[Optional[datetime.datetime], None] = None
    end_date: Annotated[Optional[datetime.datetime], None] = None
    completa: Annotated[Optional[bool], None] = None
    manifestada: Annotated[Optional[bool], None] = None
    manifestando: Annotated[Optional[bool], None] = None
    desbravador: Annotated[Optional[bool], None] = None


class LoginUsername(BaseModel):
    username: Annotated[str, None]
    hash_password: Annotated[str, None]


class UserRequest(BaseModel):
    login_info: Annotated[Optional[LoginUsername], None] = None
    token: Annotated[Optional[str], "Auth Token"] = None


class UserResponse(BaseModel):
    # id: int
    # active: bool
    # expire: datetime.datetime
    success: bool
    token: Annotated[Optional[str], "Auth Token"] = None  # Maybe not so safe doing this
    err: Annotated[Optional[str], None] = None
    admin: Annotated[Optional[bool], None] = None

    class Config:
        from_attributes = True
