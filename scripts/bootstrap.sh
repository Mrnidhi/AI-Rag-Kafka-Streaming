#!/bin/bash
set -e

echo "Setting up AI RAG Platform..."

command -v docker >/dev/null 2>&1 || { echo "Docker is required. Aborting." >&2; exit 1; }
command -v docker-compose >/dev/null 2>&1 || { echo "Docker Compose is required. Aborting." >&2; exit 1; }

if [ ! -f .env ]; then
    cp .env.example .env
    echo "Created .env from template. Update it with your API keys."
fi

mkdir -p data/raw-documents data/processed data/embeddings

echo "Pulling Docker images..."
docker-compose pull

echo "Starting infrastructure..."
docker-compose up -d postgres redis kafka zookeeper

echo "Waiting for services..."
sleep 10

until docker exec rag-postgres pg_isready -U rag_user > /dev/null 2>&1; do
  echo "Waiting for PostgreSQL..."
  sleep 2
done

until docker exec rag-kafka kafka-broker-api-versions --bootstrap-server localhost:9092 > /dev/null 2>&1; do
  echo "Waiting for Kafka..."
  sleep 2
done

echo "Creating Kafka topics..."
for topic in documents.raw embeddings.ready events.live rag.query.logs; do
  docker exec rag-kafka kafka-topics --create --if-not-exists \
    --bootstrap-server localhost:9092 \
    --topic "$topic" \
    --partitions 3 \
    --replication-factor 1
done

echo ""
echo "Done. Next steps:"
echo "  1. Update .env with your API keys"
echo "  2. Start services (see docs/local-dev.md)"
echo ""
echo "Dashboards:"
echo "  Grafana:    http://localhost:3000 (admin/admin)"
echo "  Prometheus: http://localhost:9090"
echo "  Jaeger:     http://localhost:16686"
