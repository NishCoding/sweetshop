from pydantic import BaseModel

# ----- SWEETS -----
class SweetBase(BaseModel):
    name: str
    category: str
    price: float
    quantity: int

class SweetCreate(SweetBase):
    pass

class Sweet(SweetBase):
    id: int

    class Config:
        from_attributes = True  # Replaces orm_mode


# ----- USERS -----
class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class UserLogin(UserBase):
    password: str

class User(UserBase):
    id: int
    is_admin: int

    class Config:
        from_attributes = True
