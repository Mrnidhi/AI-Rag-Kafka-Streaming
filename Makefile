.PHONY: help up down build test eval clean bootstrap

help:
	@echo "Available commands:"
	@echo "  make bootstrap  - Set up local dev environment"
	@echo "  make up         - Start infrastructure (docker-compose)"
	@echo "  make down       - Stop infrastructure"
	@echo "  make build      - Build all services"
	@echo "  make test       - Run all tests"
	@echo "  make clean      - Remove build artifacts and containers"

bootstrap:
	./scripts/bootstrap.sh

up:
	docker-compose up -d
	@echo "Services starting. Use 'docker-compose logs -f' to follow."

down:
	docker-compose down

build:
	cd services/ingestion && go build -o bin/ingestion ./cmd/server
	cd services/embedding && pip install -r requirements.txt
	cd services/rag-gateway && ./gradlew build -x test
	cd services/agent && pip install -r requirements.txt

test:
	cd services/ingestion && go test ./...
	cd services/embedding && pytest tests/
	cd services/rag-gateway && ./gradlew test

clean:
	./scripts/cleanup.sh
