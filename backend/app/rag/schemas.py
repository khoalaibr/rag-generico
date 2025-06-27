# backend/app/rag/schemas.py
from pydantic import BaseModel, Field

# --- Esquema para la Pregunta (Request) ---
# Define la estructura que debe tener el cuerpo de la petición
# que llega a nuestra API.
class QueryRequest(BaseModel):
    """Esquema para una pregunta del usuario."""
    question: str = Field(
        ..., # El campo es obligatorio
        min_length=3,
        max_length=500,
        description="La pregunta que el usuario quiere hacer al sistema RAG."
    )

# --- Esquema para la Respuesta (Response) ---
# Define la estructura de la respuesta que nuestra API devolverá.
class QueryResponse(BaseModel):
    """Esquema para la respuesta generada por el sistema."""
    answer: str = Field(
        ...,
        description="La respuesta generada por el LLM, fundamentada en los documentos."
    )
    # En el futuro, podríamos añadir las fuentes consultadas aquí.
    # sources: list[str] = []
