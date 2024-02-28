from fastapi import FastAPI
from pydantic import BaseModel
app = FastAPI()

class ItemBase(BaseModel):
    item_id: int
    question: str
    answers: list[str]
  

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/item")
async def root():
    return {"message": "Test Hello World"}


@app.get("/item/{item_id}")
async def read_item(item_id : int):
    return {"item/id": item_id}

@app.post("/item/")
async def create_item(item: ItemBase):
    return item