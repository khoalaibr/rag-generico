CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS pg_trgm;

-- Tabla para los vectores de documentos (sin cambios)
CREATE TABLE IF NOT EXISTS document_vectors (
    id VARCHAR(36) PRIMARY KEY,
    text TEXT NOT NULL,
    embedding VECTOR(384) NOT NULL,
    metadata_ JSONB
);

-- --- NUEVA TABLA PARA USUARIOS ---
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    -- En el futuro, podríamos añadir una columna de rol aquí
    role VARCHAR(50) DEFAULT 'user'
);