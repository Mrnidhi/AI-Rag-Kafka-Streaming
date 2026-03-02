import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.config import settings
from app.routes import embed, health, search
from app.services.kafka_consumer import chunk_consumer

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(name)s %(levelname)s %(message)s",
)

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("starting embedding service on port %d", settings.api_port)
    try:
        chunk_consumer.start()
    except Exception:
        logger.warning("kafka consumer failed to start, running without it")
    yield
    chunk_consumer.stop()


app = FastAPI(
    title="Embedding Service",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(health.router, prefix="/api/v1")
app.include_router(embed.router, prefix="/api/v1")
app.include_router(search.router, prefix="/api/v1")
