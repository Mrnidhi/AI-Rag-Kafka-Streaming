package parser

import (
	"strings"
	"unicode/utf8"

	"github.com/google/uuid"
	"github.com/srinidhigowda/ai-rag-kafka-streaming-platform/services/ingestion/internal/model"
)

// ChunkDocument splits a document's content into overlapping chunks.
// Overlap helps preserve context at chunk boundaries for better retrieval.
func ChunkDocument(doc model.Document, chunkSize, overlap int) []model.Chunk {
	text := strings.TrimSpace(doc.Content)
	if text == "" {
		return nil
	}

	runes := []rune(text)
	total := utf8.RuneCountInString(text)

	if total <= chunkSize {
		return []model.Chunk{{
			ID:         uuid.New().String(),
			DocumentID: doc.ID,
			Content:    text,
			Index:      0,
			Metadata:   doc.Metadata,
		}}
	}

	var chunks []model.Chunk
	start := 0
	idx := 0

	for start < total {
		end := start + chunkSize
		if end > total {
			end = total
		}

		segment := string(runes[start:end])

		// Try to break at the last sentence boundary within the chunk
		if end < total {
			if bp := findSentenceBreak(segment); bp > 0 {
				end = start + bp
				segment = string(runes[start:end])
			}
		}

		chunks = append(chunks, model.Chunk{
			ID:         uuid.New().String(),
			DocumentID: doc.ID,
			Content:    strings.TrimSpace(segment),
			Index:      idx,
			Metadata:   doc.Metadata,
		})

		idx++
		start = end - overlap
		if start < 0 {
			start = 0
		}
		if start >= total {
			break
		}
	}

	return chunks
}

func findSentenceBreak(text string) int {
	delimiters := []string{". ", ".\n", "! ", "!\n", "? ", "?\n"}
	lastPos := -1
	for _, d := range delimiters {
		if p := strings.LastIndex(text, d); p > lastPos {
			lastPos = p + len(d)
		}
	}
	return lastPos
}

// ParsePlainText reads raw text content and returns a Document.
func ParsePlainText(title, content, source string, metadata map[string]string) model.Document {
	return model.Document{
		ID:       uuid.New().String(),
		Title:    title,
		Content:  content,
		Source:   source,
		Metadata: metadata,
	}
}
