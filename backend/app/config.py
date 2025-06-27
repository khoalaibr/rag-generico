# backend/app/config.py

import os
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '..', '.env')
load_dotenv(dotenv_path=dotenv_path)


class Settings:
    """
    Clase para gestionar las configuraciones de la aplicación.
    Lee las variables de entorno al ser instanciada.
    """
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY")
    SECRET_KEY: str = os.getenv("SECRET_KEY")

# Creamos una instancia única de la configuración
settings = Settings()

# Verificación para asegurar que las variables críticas se cargaron
if not all([settings.DATABASE_URL, settings.GEMINI_API_KEY, settings.SECRET_KEY]):
    raise ValueError("Una o más variables de entorno críticas no están definidas. Revisa tu archivo .env.")

