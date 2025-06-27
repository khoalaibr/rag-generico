# backend/app/users/models.py
from sqlalchemy import Boolean, Column, Integer, String
# --- CORRECCIÓN DE IMPORTS ---
# Usamos una ruta relativa para llegar al archivo database.py
from ..database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(String, default="user")
