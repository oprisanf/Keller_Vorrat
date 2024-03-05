from fastapi import FastAPI, HTTPException, Depends
import crud
import models
import schemas
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from typing import List
import requests
from prometheus_fastapi_instrumentator import Instrumentator


app = FastAPI()
models.Base.metadata.create_all(bind=engine)
Instrumentator().instrument(app).expose(app)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# @app.post("/users/", response_model=schemas.User)
# def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
#     db_user = crud.get_user_by_email(db, email=user.email)
#     if db_user:
#         raise HTTPException(status_code=400, detail="Email already registered")
#     return crud.create_user(db=db, user=user)


# @app.get("/users/", response_model=list[schemas.User])
# def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     users = crud.get_users(db, skip=skip, limit=limit)
#     return users


# @app.get("/users/{user_id}", response_model=schemas.User)
# def read_user(user_id: int, db: Session = Depends(get_db)):
#     db_user = crud.get_user(db, user_id=user_id)
#     if db_user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return db_user


@app.get("/")
async def root():
    return {"message": "Hello Vorrat Master"}


@app.get("/items", response_model=List[schemas.Item])
async def get_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items


@app.get("/item/{item_name}", response_model=List[schemas.Item])
async def get_item(item_name: str, db: Session = Depends(get_db)):
    
    items = crud.get_item_by_name(db, item_name)
    if not items:
        raise HTTPException(
            status_code=404, detail='Item id:{item_name} not found')
    return items


@app.post("/item/", response_model=schemas.Item)
async def create_item(item: schemas.ItemCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_user_item(db, item=item)
    except crud.DuplicateError as e:
        print(e)
        return None

# @app.put("/item/{item_id}", response_model=Item)
# async def update_item(item_id: int, item: Item):
#     existing_item = find_item_by_id(item_id)
#     if existing_item is None:
#         raise HTTPException(status_code=404, detail=f"No ItemBase found with id {item_id}")
#     existing_item.item_name = item.item_name
#     existing_item.description = item.description
#     existing_item.price = item.price
#     existing_item.expiry_date = item.expiry_date

#     return existing_item


@app.delete("/item/{item_id}")
async def delete_item(item_id: int, db: Session = Depends(get_db)):
    return crud.delete_user_item(db=db, item_id=item_id)
  