from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    openai_api_key: str = ""
    agent_model: str = "gpt-4"
    max_iterations: int = 10
    embedding_service_url: str = "http://localhost:8001"
    api_port: int = 8002

    class Config:
        env_file = ".env"


settings = Settings()
