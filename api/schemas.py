from pydantic import BaseModel

# Modelos Pydantic
class PatrimonioCreate(BaseModel):
    Item: str
    Setor: str = None
    Filial: str = None
    Tipo: str = None
    Patrimonio: int = None

class PatrimonioResponse(PatrimonioCreate):
    pass