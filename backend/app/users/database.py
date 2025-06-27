# backend/app/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

# Creamos el motor de SQLAlchemy
engine = create_engine(settings.DATABASE_URL)

# Creamos una fábrica de sesiones
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Creamos una clase Base para nuestros modelos ORM
Base = declarative_base()

# Dependencia para obtener una sesión de la BD en cada petición
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
