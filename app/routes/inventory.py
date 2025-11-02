from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, database
from app.auth import require_admin

router = APIRouter()

@router.post("/{sweet_id}/purchase")
def purchase_sweet(sweet_id: int, db: Session = Depends(database.SessionLocal)):
    sweet = crud.get_sweet_by_id(db, sweet_id)
    if not sweet or sweet.quantity <= 0:
        raise HTTPException(status_code=400, detail="Out of stock")
    sweet.quantity -= 1
    db.commit()
    return {"message": "Purchase successful"}

@router.post("/{sweet_id}/restock")
def restock_sweet(
    sweet_id: int,
    db: Session = Depends(database.SessionLocal),
    user=Depends(require_admin)
):
    sweet = crud.get_sweet_by_id(db, sweet_id)
    if not sweet:
        raise HTTPException(status_code=404, detail="Sweet not found")
    sweet.quantity += 10
    db.commit()
    return {"message": "Restocked successfully"}
