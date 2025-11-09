from sqlalchemy import Column, String, Integer, Float, Date,ForeignKey

from sqlalchemy.orm import relationship

from typing import Optional
from datetime import date

from models.model_base import Model_base



class Categoria(Model_base):
    __tablename__ = 'categorias'

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    nome: str = Column(String, nullable=False)
    descricao: Optional[str] = Column(String(255), nullable=False)
    transacoes = relationship("Transacoes", back_populates="categoria")

    def __repr__ (self) -> str:
        return f'Nome: {self.nome}'

class Transacoes(Model_base):
    __tablename__ = 'transacoes'

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    tipo: str = Column(String, nullable=False)
    valor: float = Column(Float, nullable=False)
    descricao: str = Column(String(255), nullable=False)
    data: date = Column(Date, nullable=False)
    id_categoria: int = Column(Integer, ForeignKey('categorias.id'))
    categoria = relationship("Categoria", back_populates="transacoes")

    def __repr__ (self) -> str:
        return f'Tipo: {self.tipo}'