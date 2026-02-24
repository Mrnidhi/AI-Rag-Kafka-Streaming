package model

import "time"

type Document struct {
	ID        string    `json:"id"`
	Title     string    `json:"title"`
	Content   string    `json:"content"`
	Source    string    `json:"source"`
	Metadata  map[string]string `json:"metadata,omitempty"`
	CreatedAt time.Time `json:"created_at"`
}

type Chunk struct {
	ID         string            `json:"id"`
	DocumentID string            `json:"document_id"`
	Content    string            `json:"content"`
	Index      int               `json:"index"`
	Metadata   map[string]string `json:"metadata,omitempty"`
}

type IngestRequest struct {
	Title    string            `json:"title" validate:"required"`
	Content  string            `json:"content" validate:"required"`
	Source   string            `json:"source"`
	Metadata map[string]string `json:"metadata,omitempty"`
}

type IngestResponse struct {
	DocumentID string `json:"document_id"`
	Chunks     int    `json:"chunks"`
	Status     string `json:"status"`
}
