from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    embedding_dimension: int = 384

    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_user: str = "rag_user"
    postgres_password: str = "rag_pass"
    postgres_db: str = "rag_platform"

    kafka_brokers: str = "localhost:9092"
    kafka_topic_documents: str = "documents.raw"
    kafka_topic_embeddings: str = "embeddings.ready"
    kafka_consumer_group: str = "embedding-service"

    batch_size: int = 32
    api_port: int = 8001

    class Config:
        env_file = ".env"


settings = Settings()
