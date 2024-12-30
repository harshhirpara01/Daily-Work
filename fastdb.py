from email.policy import default
from enum import unique
from operator import index

from fastapi import FastAPI,Query,Depends
from typing import Optional,List
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Boolean, Column
from sqlalchemy.orm import Session

from database import base,engine,SessionLocal


class user(base):
    __tablename__ ="user"
    id=Column(Integer,primary_key=True,index=True)
    email=Column(String,unique=True,index=True)
    is_active = Column(Boolean,default=True)

class userschema(BaseModel):
    id:int
    email:str
    is_active:bool


    class Config:
        orm_mode =True



def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()


base.metadata.create_all(bind=engine)



app = FastAPI()

@app.post("/user")
async def index(user:userschema,db:Session=Depends(get_db)):

    u = user(email=user.email,is_active = user.is_active,id=user.id)
    db.add(u)
    db.commit()
    return u

