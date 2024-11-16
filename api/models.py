from sqlalchemy import Column, Integer, String
from database import Base

# Modelo SQLAlchemy para a tabela patrimonio
class Patrimonio(Base):
    __tablename__ = "patrimonio"
    Item = Column(String, nullable=False)
    Setor = Column(String, nullable=True)
    Filial = Column(String, nullable=True)
    Tipo = Column(String, nullable=True)
    Patrimonio = Column(Integer, primary_key=True)
