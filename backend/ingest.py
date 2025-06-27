# backend/ingest.py
import os
import logging
import sys
import json 
from sqlalchemy import create_engine, text, Table, MetaData, Column, String, JSON
from pgvector.sqlalchemy import Vector
from llama_index.core import SimpleDirectoryReader, Settings as LlamaSettings
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.embeddings import resolve_embed_model

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

try:
    from app.config import settings
except ImportError:
    print("Error: No se pudo importar la configuración.")
    sys.exit(1)

def run_ingestion():
    logging.info("Iniciando el proceso de ingesta con control manual y explícito...")
    
    os.environ["GOOGLE_API_KEY"] = settings.GEMINI_API_KEY
    embed_model = resolve_embed_model("local:sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
    LlamaSettings.embed_model = embed_model
    logging.info("Modelo de embedding configurado.")
    
    reader = SimpleDirectoryReader("./data")
    documents = reader.load_data()
    logging.info(f"Se cargaron {len(documents)} documento(s).")
    
    parser = SentenceSplitter()
    nodes = parser.get_nodes_from_documents(documents, show_progress=True)
    logging.info(f"Documentos parseados en {len(nodes)} nodos.")
    
    logging.info("Conectándose a la base de datos con SQLAlchemy...")
    db_engine = create_engine(settings.DATABASE_URL)
    
    meta = MetaData()
    documents_table = Table(
        'document_vectors', meta,
        Column('id', String, primary_key=True),
        Column('text', String),
        Column('embedding', Vector(384)),
        Column('metadata_', JSON)
    )

    with db_engine.connect() as connection:
        with connection.begin() as transaction:
            logging.info("Transacción iniciada. Vaciando tabla 'document_vectors'...")
            connection.execute(text("TRUNCATE TABLE document_vectors;"))
            
            logging.info("Insertando nodos en la base de datos...")
            for node in nodes:
                node_embedding = embed_model.get_text_embedding(node.get_content(metadata_mode="all"))
                stmt = documents_table.insert().values(
                    id=node.id_,
                    text=node.get_content(),
                    embedding=node_embedding,
                    metadata_=node.metadata
                )
                connection.execute(stmt)
            logging.info(f"Se intentaron insertar {len(nodes)} nodos.")
            transaction.commit()
            logging.info("¡Transacción confirmada!")

        # --- PASO DE AUTO-VERIFICACIÓN ---
        # Justo después de la ingesta, contamos las filas para estar 100% seguros.
        count_result = connection.execute(text("SELECT COUNT(id) FROM document_vectors;")).scalar_one()
        logging.info(f"VERIFICACIÓN POST-INGESTA: La tabla 'document_vectors' ahora contiene {count_result} fila(s).")

    logging.info("¡Proceso de ingesta completado exitosamente y datos guardados!")

if __name__ == "__main__":
    run_ingestion()
