from pydantic import BaseModel


class MatrixCreate(BaseModel):
    uuid: str
    name: str

    class Config:
        json_schema_extra = {'example': {'uuid': '0SN91roa6', 'name': 'first-matrix'}}
