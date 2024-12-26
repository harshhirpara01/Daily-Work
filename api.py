from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    age: int


@app.post("/")
async def login_name (self:Item):

    return { "name" :self.name , "age" :self.age}


