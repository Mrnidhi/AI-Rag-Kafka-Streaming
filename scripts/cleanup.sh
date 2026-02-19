#!/bin/bash
set -e

echo "Cleaning up..."

docker-compose down -v 2>/dev/null || true

rm -rf services/rag-gateway/build/
rm -rf services/ingestion/bin/
find services/embedding -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find services/agent -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true

echo "Cleanup complete."
