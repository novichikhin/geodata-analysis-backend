from pydantic import BaseModel


class ObjectModel(BaseModel):
    name: str
    latitude: float
    longitude: float
