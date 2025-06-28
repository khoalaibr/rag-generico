# backend/app/general/service.py
import os
import logging
from llama_index.llms.gemini import Gemini
from app.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GeneralPurposeService:
    def __init__(self):
        logger.info("Inicializando GeneralPurposeService...")
        os.environ["GOOGLE_API_KEY"] = settings.GEMINI_API_KEY
        self.llm = Gemini(model_name="models/gemini-1.5-flash-latest")
        logger.info("GeneralPurposeService inicializado.")

    def get_llm_response(self, prompt: str) -> str:
        final_prompt = f"Responde a la siguiente instrucción en español, de forma útil y creativa.\n\nInstrucción: \"{prompt}\""
        logger.info(f"Enviando prompt al LLM: '{final_prompt[:80]}...'")
        response = self.llm.complete(final_prompt)
        return response.text

general_service = GeneralPurposeService()