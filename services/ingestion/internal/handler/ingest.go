package handler

import (
	"fmt"
	"io"
	"log"

	"github.com/gofiber/fiber/v2"
	"github.com/srinidhigowda/ai-rag-kafka-streaming-platform/services/ingestion/internal/kafka"
	"github.com/srinidhigowda/ai-rag-kafka-streaming-platform/services/ingestion/internal/model"
	"github.com/srinidhigowda/ai-rag-kafka-streaming-platform/services/ingestion/internal/parser"
)

type IngestHandler struct {
	Producer   *kafka.Producer
	ChunkSize  int
	ChunkOverlap int
	MaxFileMB  int
}

func (h *IngestHandler) IngestDocument(c *fiber.Ctx) error {
	var req model.IngestRequest
	if err := c.BodyParser(&req); err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{
			"error": "invalid request body",
		})
	}

	if req.Title == "" || req.Content == "" {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{
			"error": "title and content are required",
		})
	}

	doc := parser.ParsePlainText(req.Title, req.Content, req.Source, req.Metadata)
	chunks := parser.ChunkDocument(doc, h.ChunkSize, h.ChunkOverlap)

	if err := h.Producer.PublishChunks(chunks); err != nil {
		log.Printf("failed to publish chunks for doc %s: %v", doc.ID, err)
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{
			"error": "failed to process document",
		})
	}

	return c.Status(fiber.StatusAccepted).JSON(model.IngestResponse{
		DocumentID: doc.ID,
		Chunks:     len(chunks),
		Status:     "accepted",
	})
}

func (h *IngestHandler) UploadFile(c *fiber.Ctx) error {
	file, err := c.FormFile("file")
	if err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{
			"error": "file is required",
		})
	}

	maxBytes := int64(h.MaxFileMB) * 1024 * 1024
	if file.Size > maxBytes {
		return c.Status(fiber.StatusRequestEntityTooLarge).JSON(fiber.Map{
			"error": fmt.Sprintf("file exceeds %dMB limit", h.MaxFileMB),
		})
	}

	f, err := file.Open()
	if err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{
			"error": "failed to read file",
		})
	}
	defer f.Close()

	content, err := io.ReadAll(f)
	if err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{
			"error": "failed to read file content",
		})
	}

	source := c.FormValue("source", "upload")
	doc := parser.ParsePlainText(file.Filename, string(content), source, nil)
	chunks := parser.ChunkDocument(doc, h.ChunkSize, h.ChunkOverlap)

	if err := h.Producer.PublishChunks(chunks); err != nil {
		log.Printf("failed to publish chunks for file %s: %v", file.Filename, err)
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{
			"error": "failed to process file",
		})
	}

	return c.Status(fiber.StatusAccepted).JSON(model.IngestResponse{
		DocumentID: doc.ID,
		Chunks:     len(chunks),
		Status:     "accepted",
	})
}
