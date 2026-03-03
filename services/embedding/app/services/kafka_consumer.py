import json
import logging
import threading

from kafka import KafkaConsumer, KafkaProducer

from app.config import settings
from app.services.embedder import embedding_service
from app.services.vector_store import vector_store

logger = logging.getLogger(__name__)


class ChunkConsumer:
    """Consumes document chunks from Kafka, generates embeddings,
    stores them in pgvector, and publishes completion events."""

    def __init__(self):
        self._running = False
        self._thread = None

    def start(self):
        if self._running:
            return
        self._running = True
        self._thread = threading.Thread(target=self._consume_loop, daemon=True)
        self._thread.start()
        logger.info("kafka consumer started for topic: %s", settings.kafka_topic_documents)

    def stop(self):
        self._running = False
        if self._thread:
            self._thread.join(timeout=5)

    def _consume_loop(self):
        try:
            consumer = KafkaConsumer(
                settings.kafka_topic_documents,
                bootstrap_servers=settings.kafka_brokers.split(","),
                group_id=settings.kafka_consumer_group,
                value_deserializer=lambda m: json.loads(m.decode("utf-8")),
                auto_offset_reset="earliest",
                enable_auto_commit=True,
            )

            producer = KafkaProducer(
                bootstrap_servers=settings.kafka_brokers.split(","),
                value_serializer=lambda v: json.dumps(v).encode("utf-8"),
            )
        except Exception:
            logger.exception("failed to connect to kafka")
            self._running = False
            return

        try:
            while self._running:
                records = consumer.poll(timeout_ms=1000)
                for _, messages in records.items():
                    for msg in messages:
                        self._process_chunk(msg.value, producer)
        except Exception:
            logger.exception("consumer loop error")
        finally:
            consumer.close()
            producer.close()

    def _process_chunk(self, chunk: dict, producer: KafkaProducer):
        try:
            text = chunk.get("content", "")
            doc_id = chunk.get("document_id", "")
            chunk_index = chunk.get("index", 0)
            metadata = chunk.get("metadata")

            if not text:
                return

            embedding = embedding_service.embed_single(text)

            embedding_id = vector_store.store_embedding(
                document_id=doc_id,
                chunk_text=text,
                embedding=embedding,
                chunk_index=chunk_index,
                metadata=metadata,
            )

            producer.send(
                settings.kafka_topic_embeddings,
                value={
                    "embedding_id": embedding_id,
                    "document_id": doc_id,
                    "chunk_index": chunk_index,
                    "status": "stored",
                },
            )

            logger.info("embedded chunk %d for doc %s", chunk_index, doc_id)

        except Exception:
            logger.exception("failed to process chunk for doc %s", chunk.get("document_id"))


chunk_consumer = ChunkConsumer()
