from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import crud
import models
import schemas
from database import engine, Base, get_db
from mangum import Mangum

# Criação das tabelas no banco de dados
models.Base.metadata.create_all(bind=engine)

# Inicializando o FastAPI
app = FastAPI()
handler = Mangum(app)

# Endpoint para criar um novo patrimônio
@app.post("/patrimonio/", response_model=schemas.PatrimonioResponse)
def criar_patrimonio(patrimonio: schemas.PatrimonioCreate, db: Session = Depends(get_db)):
    return crud.create_patrimonio(db=db, patrimonio=patrimonio)

# Endpoint para listar os patrimônios
@app.get("/patrimonio/", response_model=List[schemas.PatrimonioResponse])
def listar_patrimonios(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_patrimonios(db=db, skip=skip, limit=limit)

# Endpoint para buscar um patrimônio específico
@app.get("/patrimonio/{item_id}", response_model=schemas.PatrimonioResponse)
def obter_patrimonio(item_id: str, db: Session = Depends(get_db)):
    db_patrimonio = crud.get_patrimonio(db, item_id=item_id)
    if db_patrimonio is None:
        raise HTTPException(status_code=404, detail="Patrimônio não encontrado")
    return db_patrimonio

# Endpoint para atualizar um patrimônio existente
@app.put("/patrimonio/{item_id}", response_model=schemas.PatrimonioResponse)
def atualizar_patrimonio(item_id: str, patrimonio: schemas.PatrimonioCreate, db: Session = Depends(get_db)):
    db_patrimonio = crud.update_patrimonio(db, item_id=item_id, patrimonio=patrimonio)
    if db_patrimonio is None:
        raise HTTPException(status_code=404, detail="Patrimônio não encontrado")
    return db_patrimonio

# Endpoint para deletar um patrimônio
@app.delete("/patrimonio/{item_id}", response_model=schemas.PatrimonioResponse)
def deletar_patrimonio(item_id: str, db: Session = Depends(get_db)):
    db_patrimonio = crud.delete_patrimonio(db, item_id=item_id)
    if db_patrimonio is None:
        raise HTTPException(status_code=404, detail="Patrimônio não encontrado")
    return db_patrimonio
