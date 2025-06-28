# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Importamos los routers de nuestros endpoints HTTP
from .rag.router import router as rag_router
from .general.router import router as general_router
from .auth.router import router as auth_router

app = FastAPI(
    title="Asesor IA - Backend",
    description="API con RAG, IA General y Autenticación.",
    version="1.1.0",
)

# Configuración de CORS
origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "¡Bienvenido al Backend del Asesor IA!"}

# Incluimos ambos routers HTTP
app.include_router(auth_router, prefix="/api/v1")
app.include_router(rag_router, prefix="/api/v1")
app.include_router(general_router, prefix="/api/v1")
