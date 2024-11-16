from sqlalchemy.orm import Session
import models
import schemas

# Função para buscar um patrimônio específico
def get_patrimonio(db: Session, item_id: str):
    return db.query(models.Patrimonio).filter(models.Patrimonio.Patrimonio == item_id).first()

# Função para listar os patrimônios com offset e limit
def get_patrimonios(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Patrimonio).offset(skip).limit(limit).all()

# Função para criar um novo patrimônio
def create_patrimonio(db: Session, patrimonio: schemas.PatrimonioCreate):
    db_patrimonio = models.Patrimonio(
        Item=patrimonio.Item,
        Setor=patrimonio.Setor,
        Filial=patrimonio.Filial,
        Tipo=patrimonio.Tipo,
        Patrimonio=patrimonio.Patrimonio
    )
    db.add(db_patrimonio)
    db.commit()
    db.refresh(db_patrimonio)
    return db_patrimonio

# Função para atualizar um patrimônio existente
def update_patrimonio(db: Session, item_id: str, patrimonio: schemas.PatrimonioCreate):
    db_patrimonio = get_patrimonio(db, item_id)
    if db_patrimonio:
        db_patrimonio.Item = patrimonio.Item
        db_patrimonio.Setor = patrimonio.Setor
        db_patrimonio.Filial = patrimonio.Filial
        db_patrimonio.Tipo = patrimonio.Tipo
        # db_patrimonio.Patrimonio = patrimonio.Patrimonio
        db.add(db_patrimonio)
        db.commit()
        db.refresh(db_patrimonio)
        return db_patrimonio
    return None

# Função para deletar um patrimônio
def delete_patrimonio(db: Session, item_id: str):
    db_patrimonio = get_patrimonio(db, item_id)
    if db_patrimonio:
        db.delete(db_patrimonio)
        db.commit()
    return db_patrimonio
