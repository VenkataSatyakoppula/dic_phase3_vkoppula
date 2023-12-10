from pydantic import BaseModel
from typing import List,Dict
import datetime
class DataSetCreate(BaseModel):
    id: int
    name: str

class Dataset(DataSetCreate):
    cleaning_step: int
    eda_step: int
    created_on : datetime.datetime


class DatasetBody(BaseModel):
    columns: List[str] = []
    rename: Dict = {}
    values: Dict = {}
