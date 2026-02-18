-- Initialize RAG Platform Database

-- Enable vector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Documents table
CREATE TABLE IF NOT EXISTS documents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(500) NOT NULL,
    content TEXT NOT NULL,
    source VARCHAR(500),
    metadata JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Embeddings table
CREATE TABLE IF NOT EXISTS embeddings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    document_id UUID REFERENCES documents(id) ON DELETE CASCADE,
    chunk_text TEXT NOT NULL,
    embedding vector(384), -- Adjust dimension based on model
    chunk_index INTEGER,
    metadata JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Create HNSW index for vector similarity search
CREATE INDEX IF NOT EXISTS embeddings_hnsw_idx 
ON embeddings USING hnsw (embedding vector_cosine_ops);

-- Create regular indexes
CREATE INDEX IF NOT EXISTS idx_documents_source ON documents(source);
CREATE INDEX IF NOT EXISTS idx_embeddings_document_id ON embeddings(document_id);

-- Query logs table
CREATE TABLE IF NOT EXISTS query_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    query TEXT NOT NULL,
    response TEXT,
    latency_ms INTEGER,
    tokens_used INTEGER,
    retrieved_docs JSONB,
    timestamp TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_query_logs_timestamp ON query_logs(timestamp DESC);

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Trigger for documents table
CREATE TRIGGER update_documents_updated_at BEFORE UPDATE ON documents
FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Insert sample document
INSERT INTO documents (title, content, source, metadata)
VALUES (
    'RAG Introduction',
    'Retrieval-Augmented Generation (RAG) is a technique that combines retrieval of relevant documents with LLM generation to produce accurate, grounded responses.',
    'sample',
    '{"category": "tutorial", "tags": ["rag", "llm", "ai"]}'::jsonb
);

COMMIT;
