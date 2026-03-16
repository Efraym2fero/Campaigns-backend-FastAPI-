
from random import randint
from typing import Any

from fastapi import FastAPI, HTTPException, Request
from datetime import datetime

app = FastAPI(root_path="/api/v1")


data = [
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
]


@app.get("/")
async def root():
    return {"mesage":"You are in the root"}

@app.get("/campaigns")
async def getCampaigns():
    return {"campaigns": data}

@app.get("/campaigns/{id}")
async def getACampaign(id:int):
    for c in data:
        if c.get("id") == id:
            return {"cmapaign": c}
    raise HTTPException(status_code=404)

@app.post("/campaigns")
async def createACampaign(body:dict[str,Any]):
    new = {
        "id":randint(4,100),
        "name": body.get("name"),
        "date": body.get("date"),
        "createdAt":datetime.now()  
    }
    data.append(new)
    return {"cmapaigns":new} 

@app.put("/campaigns/{id}")
async def updateACamoaign(id:int,body:dict[str,Any]):
    for i, c in enumerate(data):
        if c.get("id")==id:
            update = {
                "id":id,
                "name": body.get("name"),
                "date": body.get("date"),
                "createdAt":c.get("createdAt")
            }
            data[i]=update
            return {"cmapaigns":update} 
    raise HTTPException(status_code=404)

@app.delete("/campaigns/{id}")
async def deleteCampaign(id:int):
    for c in data:
        if c.get("id")==id:
            data.remove(c)

if __name__ == "__main__":
    print("hi")
