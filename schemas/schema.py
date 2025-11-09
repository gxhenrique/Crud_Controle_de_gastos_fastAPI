from pydantic import BaseModel
from datetime import date

class SchemaCategoria(BaseModel):
    nome: str
    descricao: str

    class Config:
        orm_mode = True


class SchemaTransacoes(BaseModel):
    tipo: str
    valor: float
    descricao: str 
    data: date

    class Config:
        orm_mode = True
