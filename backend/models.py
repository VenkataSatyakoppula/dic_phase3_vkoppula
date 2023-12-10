from sqlalchemy import Boolean, Column, ForeignKey, Integer, String,DateTime
from datetime import datetime
from database import Base

class Dataset(Base):
    __tablename__ = "dataset"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    file_path = Column(String)
    cleaning_step = Column(Integer,default=0)
    eda_step = Column(Integer,default=0)
    created_on = Column(DateTime,default=datetime.utcnow)
