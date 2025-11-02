from fastapi import FastAPI
from app.routes import sweets, users, inventory

app = FastAPI(title="Sweet Shop Management System")

app.include_router(users.router, prefix="/api/auth", tags=["Auth"])
app.include_router(sweets.router, prefix="/api/sweets", tags=["Sweets"])
app.include_router(inventory.router, prefix="/api/inventory", tags=["Inventory"])

@app.get("/")
def home():
    return {"message": "Welcome to the Sweet Shop API"}
