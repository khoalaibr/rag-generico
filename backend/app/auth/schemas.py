# backend/app/auth/schemas.py
from pydantic import BaseModel, EmailStr

# --- Esquemas para Tokens ---
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str | None = None

# --- Esquemas para Usuarios ---
class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserInDB(UserBase):
    id: int
    is_active: bool
    role: str

    class Config:
        orm_mode = True # Permite que Pydantic lea datos desde objetos de SQLAlchemy

class User(UserInDB):
    pass
