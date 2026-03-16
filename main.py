
from contextlib import asynccontextmanager
from random import randint
from typing import Annotated, Any, Generic, TypeVar

from fastapi import FastAPI, HTTPException, Request,Depends
from datetime import datetime, timezone

from pydantic import BaseModel
from sqlmodel import  Field, create_engine,SQLModel,Session, select

class Campaign(SQLModel,table=True):
    campID : int|None = Field(default=None,primary_key=True)
    campName:str = Field(index=True)
    campDate : datetime | None = Field(default=None,index=True)
    createdAt : datetime = Field(default_factory=lambda :datetime.now(timezone.utc), nullable=True,index=True)


dbName = "data.db"
dbURL = f"sqlite:///{dbName}"
connectArgs = {"check_same_thread":False}
engine = create_engine(dbURL,connect_args=connectArgs)

def createDBandTables():
    SQLModel.metadata.create_all(engine)

def getSession():
    with Session(engine) as s:
        yield s
sessionDep = Annotated[Session,Depends(getSession)]

@asynccontextmanager
async def lifeSpan(app:FastAPI):
    createDBandTables()
    with Session(engine) as s:
        if not s.exec(select(Campaign)).first():
            s.add_all([
                Campaign(campName="hello world",campDate=datetime.now()),
                Campaign(campName="power rangers",campDate=datetime.now())
            ])
            s.commit()
    yield


app = FastAPI(root_path="/api/v1",lifespan=lifeSpan)


""" data = [
    {
        "id":1,
        "name": "Party",
        "date": datetime.now(),
        "createdAt":datetime.now() 
    },
    {
        "id":2,
        "name": "Party2",
        "date": datetime.now(),
        "createdAt":datetime.now() 
    },
    {
        "id":3,
        "name": "Party3",
        "date": datetime.now(),
        "createdAt":datetime.now() 
    }
] """

T = TypeVar("T")
class Response(BaseModel,Generic[T]):
    data : T



class CeateCampaign(SQLModel):
    campName: str
    campDate: datetime|None =None


@app.get("/")
async def root():
    return {"mesage":"You are in the root"}


@app.get("/campaigns")
async def getAllCampaigns(s:sessionDep):
    data = s.exec(select(Campaign)).all()
    return{"campaigns":data}


@app.get("/campaigns/{id}")
async def getAllCampaigns(id:int,s:sessionDep):
    data = s.exec(select(Campaign)).all()

    for c in data:
        if c.campID == id:
            return{"campaign":c}


@app.post("/campaigns",status_code=201,response_model=Response[Campaign])
async def createCampaign(body:CeateCampaign,s:sessionDep):
    newData = Campaign.model_validate(body) 
    s.add(newData)
    s.commit()
    s.refresh(newData)
    return {"data":newData}

@app.put("/campaigns/{id}",status_code=201,response_model=Response[Campaign])
async def updateCampaign(id:int,body :CeateCampaign,s:sessionDep):
    data = s.get(Campaign,id)
    if not data:
        raise HTTPException(status_code=404)
    data.campName = body.campName
    data.campDate = body.campDate
    s.add(data)
    s.commit()
    s.refresh(data)
    return {"data":data}

@app.delete("/campaigns/{id}",status_code=204)
async def deleteCampaign(id:int,s:sessionDep):
    data = s.get(Campaign,id)
    if not data:
        raise HTTPException(status_code=404)
    s.delete(data)
    s.commit()



if __name__ == "__main__":
    print("hi")