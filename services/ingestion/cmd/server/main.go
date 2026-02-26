package main

import (
	"log"

	"github.com/gofiber/fiber/v2"
	"github.com/gofiber/fiber/v2/middleware/cors"
	"github.com/gofiber/fiber/v2/middleware/logger"
	"github.com/gofiber/fiber/v2/middleware/recover"
	"github.com/joho/godotenv"

	"github.com/srinidhigowda/ai-rag-kafka-streaming-platform/services/ingestion/internal/config"
	"github.com/srinidhigowda/ai-rag-kafka-streaming-platform/services/ingestion/internal/handler"
	"github.com/srinidhigowda/ai-rag-kafka-streaming-platform/services/ingestion/internal/kafka"
)

func main() {
	_ = godotenv.Load()

	cfg := config.Load()

	producer, err := kafka.NewProducer(cfg.KafkaBrokers, cfg.KafkaTopic)
	if err != nil {
		log.Fatalf("kafka producer init failed: %v", err)
	}
	defer producer.Close()

	h := &handler.IngestHandler{
		Producer:     producer,
		ChunkSize:    cfg.ChunkSize,
		ChunkOverlap: cfg.ChunkOverlap,
		MaxFileMB:    cfg.MaxFileSizeMB,
	}

	app := fiber.New(fiber.Config{
		BodyLimit: cfg.MaxFileSizeMB * 1024 * 1024,
	})

	app.Use(recover.New())
	app.Use(logger.New())
	app.Use(cors.New())

	api := app.Group("/api/v1")
	api.Get("/health", handler.HealthCheck)
	api.Post("/ingest", h.IngestDocument)
	api.Post("/ingest/upload", h.UploadFile)

	log.Printf("ingestion service starting on :%s", cfg.Port)
	log.Fatal(app.Listen(":" + cfg.Port))
}
