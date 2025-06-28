# backend/app/rag/service.py
import os
import logging
from sqlalchemy import create_engine, text
from llama_index.core import PromptTemplate, Settings as LlamaSettings, get_response_synthesizer
from llama_index.core.schema import NodeWithScore, TextNode
from llama_index.core.embeddings import resolve_embed_model
from llama_index.llms.gemini import Gemini
from app.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SPANISH_QA_TEMPLATE = PromptTemplate(
    "A continuación se muestra información de contexto.\n"
    "---------------------\n"
    "{context_str}\n"
    "---------------------\n"
    "Dada la información de contexto y no conocimientos previos, "
    "responde a la siguiente pregunta.\n"
    "IMPORTANTE: Tu respuesta DEBE ser exclusivamente en español.\n"
    "Pregunta: {query_str}\n"
    "Respuesta: "
)

class RAGService:
    def __init__(self):
        logger.info("Inicializando RAGService...")
        os.environ["GOOGLE_API_KEY"] = settings.GEMINI_API_KEY
        self.embed_model = resolve_embed_model("local:sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
        self.llm = Gemini(model_name="models/gemini-1.5-flash-latest")
        LlamaSettings.embed_model = self.embed_model
        self.db_engine = create_engine(settings.DATABASE_URL)
        logger.info("RAGService inicializado.")

    def answer_query(self, question: str) -> str:
        logger.info(f"Procesando pregunta HTTP: '{question}'")
        try:
            query_embedding = self.embed_model.get_text_embedding(question)
            sql_query = text("""
                SELECT id, text, embedding <-> :query_embedding AS distance
                FROM document_vectors ORDER BY distance ASC LIMIT 3
            """)
            source_nodes = []
            with self.db_engine.connect() as connection:
                result = connection.execute(sql_query, {"query_embedding": str(list(query_embedding))})
                for row in result:
                    node = TextNode(id_=row._mapping['id'], text=row._mapping['text'])
                    source_nodes.append(NodeWithScore(node=node, score=(1.0 - row._mapping['distance'])))
            
            if source_nodes:
                logger.info(f"Nodos recuperados: {len(source_nodes)}")
                response_synthesizer = get_response_synthesizer(llm=self.llm, text_qa_template=SPANISH_QA_TEMPLATE)
                response = response_synthesizer.synthesize(question, source_nodes)
                return response.response
            else:
                logger.warning("No se recuperaron nodos.")
                return "No pude encontrar información relevante en mis documentos para responder a tu pregunta."
        except Exception as e:
            logger.error(f"Error en answer_query: {e}", exc_info=True)
            return "Ocurrió un error al procesar la consulta."

rag_service = RAGService()
