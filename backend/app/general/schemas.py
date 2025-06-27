# backend/app/general/schemas.py
from pydantic import BaseModel, Field

# --- Esquema para la Petición (Request) ---
class PromptRequest(BaseModel):
    """Esquema para una instrucción o prompt general del usuario."""
    prompt: str = Field(
        ...,
        min_length=10,
        max_length=2000,
        description="La instrucción, pregunta o texto que el usuario quiere enviar al LLM."
    )

# --- Esquema para la Respuesta (Response) ---
class PromptResponse(BaseModel):
    """Esquema para la respuesta directa del LLM."""
    answer: str = Field(
        ...,
        description="La respuesta generada por el LLM."
    )
