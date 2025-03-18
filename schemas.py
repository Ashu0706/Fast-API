from pydantic import BaseModel

class Items(BaseModel):
    name: str
    description: str

