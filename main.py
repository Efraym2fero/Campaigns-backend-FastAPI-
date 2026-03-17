
import base64
from contextlib import asynccontextmanager
import json
from random import randint
from typing import Annotated, Any, Generic, Optional, TypeVar

from fastapi import FastAPI, HTTPException, Query, Request,Depends
from datetime import datetime, timezone

from pydantic import BaseModel
from sqlmodel import  Field, create_engine,SQLModel,Session, func, select

class Campaign(SQLModel,table=True):
    campID : int = Field(default=None,primary_key=True)
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


T = TypeVar("T")
class Response(BaseModel,Generic[T]):
    data : T



class CeateCampaign(SQLModel):
    campName: str
    campDate: datetime|None =None


class PaginatedRes(BaseModel,Generic[T]):
    data : T
    next:Optional[str]
    prev:Optional[str]

class CursorPaginatedRes(BaseModel,Generic[T]):
    data : T
    next:Optional[str]

def encodeCursor(val):
    data = json.dumps({"id" : val})
    return base64.urlsafe_b64encode(data.encode()).decode()

def decodeCursor(cursor):
    decCur = base64.urlsafe_b64decode(cursor.encode()).decode()
    data = json.loads(decCur)
    return data.get("id")


@app.get("/")
async def root():
    return {"mesage":"You are in the root"}

@app.get("/campaigns",response_model=PaginatedRes[list[Campaign]])
async def getAllCampaigns(req:Request,s:sessionDep,page:int=Query(1,ge=1),pageSize:int = Query(10,ge=1)):
    limit = pageSize
    offset = (page -1)*limit
    data = s.exec(select(Campaign).order_by(Campaign.campID).offset(offset).limit(limit)).all()
    total = s.exec(select(func.count()).select_from(Campaign)).one()
    baseURL = str(req.url).split("?")[0]

    if offset+limit < total:
        nextURL = f"{baseURL}?page={page+1}&pageSize={limit}"
    else:
        nextURL=None

    if page>1:
        prevURL = f"{baseURL}?page={page-1}&pageSize={limit}"
    else:
        prevURL = None
    
    return{
        "data":data,
        "next":nextURL,
        "prev":prevURL
        } 

@app.get("/campaigns1",response_model=PaginatedRes[list[Campaign]])
async def getAllCampaigns(req:Request,s:sessionDep,offset:int=Query(0,ge=0),limit:int = Query(10,ge=1)):

    data = s.exec(select(Campaign).order_by(Campaign.campID).offset(offset).limit(limit)).all()
    total = s.exec(select(func.count()).select_from(Campaign)).one()
    baseURL = str(req.url).split("?")[0]

    if offset+limit < total:
        nextURL = f"{baseURL}?offset={offset+limit}&limit={limit}"
    else:
        nextURL=None

    if offset > 0:
        prevURL = f"{baseURL}?offset={max(0, offset-limit)}&limit={limit}"
    else:
        prevURL = None
    
    return{
        "data":data,
        "next":nextURL,
        "prev":prevURL
        }



@app.get("/campaigns2",response_model=CursorPaginatedRes[list[Campaign]])
async def getAllCampaigns(req:Request,s:sessionDep,cursor:Optional[str],limit:int = Query(10,ge=1)):
    cursorID = 0
    if cursor:
        cursorID = decodeCursor(cursor)

    data = s.exec(select(Campaign).order_by(Campaign.campID).where(Campaign.campID > cursorID).limit(limit+1)).all()
    baseURL = str(req.url).split("?")[0]
    print(baseURL)
    if len(data) > limit:
        nextCur = encodeCursor(data[:limit][-1].campID)
        print(nextCur)
        nextURL = f"{baseURL}?cursor={nextCur}&limit={limit}"
    else:
        nextURL=None
    
    return{
        "data":data[:limit],
        "next":nextURL
        }



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
    print(encodeCursor(0))