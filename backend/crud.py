from sqlalchemy.orm import Session
import models, schemas
import os

def create_dataset(db: Session, name:str,file_path: str):
    db_dataset = models.Dataset(name=name, file_path=file_path)
    db.add(db_dataset)
    db.commit()
    db.refresh(db_dataset)
    return db_dataset

def list_all(db:Session):
    return db.query(models.Dataset).all()


def get_dataset(db: Session, name:str):
    return db.query(models.Dataset).filter(models.Dataset.name == name).first()

def update_clean_step(db: Session, name:str,clean_step:int):
    datset  = db.query(models.Dataset).filter(models.Dataset.name == name).first()
    datset.cleaning_step = clean_step
    db.commit()

def delete_dataset(db: Session, name:str):
    dataset = db.query(models.Dataset).filter(models.Dataset.name == name).first()
    if dataset:
        file_path = dataset.file_path
        os.remove(file_path)
        db.delete(dataset)
        db.commit()
        return True
    return False
    