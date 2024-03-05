from sqlalchemy.orm import Session
import models, schemas


# def get_user(db: Session, user_id: int):
#     return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


# def get_users(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).filter(models.Item.deleted==False).offset(skip).limit(limit).all()


def get_item_by_name(db: Session,item_name):
        partial_match_filter = models.Item.item_name.like(f"%{item_name}%")
        query_result =  db.query(models.Item).filter(partial_match_filter,models.Item.deleted==False).all()
        return query_result

def create_user_item(db: Session, item: schemas.ItemCreate,user_id: int = 1):
    db_item = models.Item(**item.model_dump(), )#owner_id=user_id)
    
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


# def update_user_item(db:)
def delete_user_item(db: Session, item_id):
    item_id=int(item_id)
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if db_item:
         db.delete(db_item)
        #  db.add(db_item)
         db.commit()
         return db_item
    else :
         return{"message":"{item_id} doesn't exists"}

