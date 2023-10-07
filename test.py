from pydantic import BaseModel


class TestData(BaseModel):
    a: str
    b: str
