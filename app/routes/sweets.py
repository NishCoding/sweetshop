from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app import crud, schemas, database
from app.auth import get_current_user, require_admin

router = APIRouter()

@router.post("/", response_model=schemas.Sweet)
def create_sweet(
    sweet: schemas.SweetCreate,
    db: Session = Depends(database.SessionLocal),
    user=Depends(get_current_user)
):
    return crud.create_sweet(db, sweet)

@router.get("/", response_model=list[schemas.Sweet])
def get_sweets(db: Session = Depends(database.SessionLocal)):
    return crud.get_sweets(db)

@router.get("/search", response_model=list[schemas.Sweet])
def search_sweets(
    name: str | None = Query(None),
    category: str | None = Query(None),
    min_price: float | None = Query(None),
    max_price: float | None = Query(None),
    db: Session = Depends(database.SessionLocal)
):
    return crud.search_sweets(db, name, category, min_price, max_price)

@router.put("/{sweet_id}", response_model=schemas.Sweet)
def update_sweet(
    sweet_id: int,
    sweet_data: schemas.SweetCreate,
    db: Session = Depends(database.SessionLocal),
    user=Depends(require_admin)
):
    updated = crud.update_sweet(db, sweet_id, sweet_data.model_dump())
    if not updated:
        raise HTTPException(status_code=404, detail="Sweet not found")
    return updated

@router.delete("/{sweet_id}")
def delete_sweet(
    sweet_id: int,
    db: Session = Depends(database.SessionLocal),
    user=Depends(require_admin)
):
    deleted = crud.delete_sweet(db, sweet_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Sweet not found")
    return {"message": "Sweet deleted successfully"}
