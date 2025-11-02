from sqlalchemy.orm import Session
from app import models, schemas
from app.utils.security import get_password_hash, verify_password

def create_sweet(db: Session, sweet: schemas.SweetCreate):
    db_sweet = models.Sweet(**sweet.model_dump())  
    db.add(db_sweet)
    db.commit()
    db.refresh(db_sweet)
    return db_sweet


def get_sweets(db: Session):
    return db.query(models.Sweet).all()


def get_sweet_by_id(db: Session, sweet_id: int):
    return db.query(models.Sweet).filter(models.Sweet.id == sweet_id).first()


def update_sweet(db: Session, sweet_id: int, sweet_data: dict):
    sweet = get_sweet_by_id(db, sweet_id)
    if not sweet:
        return None
    for key, value in sweet_data.items():
        setattr(sweet, key, value)
    db.commit()
    db.refresh(sweet)
    return sweet


def delete_sweet(db: Session, sweet_id: int):
    sweet = get_sweet_by_id(db, sweet_id)
    if not sweet:
        return None
    db.delete(sweet)
    db.commit()
    return True


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password[:72])      
    db_user = models.User(username=user.username, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def authenticate_user(db: Session, username: str, password: str):
    user = db.query(models.User).filter(models.User.username == username).first()
    if user and verify_password(password[:72], user.password):
        return user
    return None

def search_sweets(db: Session, name=None, category=None, min_price=None, max_price=None):
    query = db.query(models.Sweet)
    if name:
        query = query.filter(models.Sweet.name.ilike(f"%{name}%"))
    if category:
        query = query.filter(models.Sweet.category.ilike(f"%{category}%"))
    if min_price:
        query = query.filter(models.Sweet.price >= min_price)
    if max_price:
        query = query.filter(models.Sweet.price <= max_price)
    return query.all()
