import json
import logging
from contextlib import contextmanager

import psycopg2
from pgvector.psycopg2 import register_vector

from app.config import settings

logger = logging.getLogger(__name__)


class VectorStore:
    def __init__(self):
        self._conn = None

    def _get_connection(self):
        if self._conn is None or self._conn.closed:
            self._conn = psycopg2.connect(
                host=settings.postgres_host,
                port=settings.postgres_port,
                user=settings.postgres_user,
                password=settings.postgres_password,
                dbname=settings.postgres_db,
            )
            register_vector(self._conn)
        return self._conn

    @contextmanager
    def _cursor(self):
        conn = self._get_connection()
        cur = conn.cursor()
        try:
            yield cur
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            cur.close()

    def store_embedding(
        self,
        document_id: str,
        chunk_text: str,
        embedding: list[float],
        chunk_index: int,
        metadata: dict | None = None,
    ) -> str:
        with self._cursor() as cur:
            cur.execute(
                """
                INSERT INTO embeddings (document_id, chunk_text, embedding, chunk_index, metadata)
                VALUES (%s, %s, %s::vector, %s, %s)
                RETURNING id
                """,
                (
                    document_id,
                    chunk_text,
                    embedding,
                    chunk_index,
                    json.dumps(metadata) if metadata else None,
                ),
            )
            return str(cur.fetchone()[0])

    def search(
        self, query_embedding: list[float], top_k: int = 5, threshold: float = 0.7
    ) -> list[dict]:
        with self._cursor() as cur:
            # cosine distance: 1 - cosine_similarity, so lower = more similar
            cur.execute(
                """
                SELECT
                    e.id,
                    e.document_id,
                    e.chunk_text,
                    1 - (e.embedding <=> %s::vector) as score,
                    e.metadata
                FROM embeddings e
                WHERE 1 - (e.embedding <=> %s::vector) >= %s
                ORDER BY e.embedding <=> %s::vector
                LIMIT %s
                """,
                (query_embedding, query_embedding, threshold, query_embedding, top_k),
            )

            results = []
            for row in cur.fetchall():
                results.append(
                    {
                        "chunk_id": str(row[0]),
                        "document_id": str(row[1]),
                        "content": row[2],
                        "score": float(row[3]),
                        "metadata": row[4],
                    }
                )
            return results

    def close(self):
        if self._conn and not self._conn.closed:
            self._conn.close()


vector_store = VectorStore()
