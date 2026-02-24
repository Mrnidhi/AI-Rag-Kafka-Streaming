package config

import (
	"os"
	"strconv"
)

type Config struct {
	Port            string
	KafkaBrokers    string
	KafkaTopic      string
	MaxFileSizeMB   int
	ChunkSize       int
	ChunkOverlap    int
}

func Load() *Config {
	return &Config{
		Port:          getEnv("API_PORT", "8000"),
		KafkaBrokers:  getEnv("KAFKA_BROKERS", "localhost:9092"),
		KafkaTopic:    getEnv("KAFKA_TOPIC_DOCUMENTS", "documents.raw"),
		MaxFileSizeMB: getEnvInt("MAX_FILE_SIZE_MB", 50),
		ChunkSize:     getEnvInt("CHUNK_SIZE", 512),
		ChunkOverlap:  getEnvInt("CHUNK_OVERLAP", 64),
	}
}

func getEnv(key, fallback string) string {
	if v := os.Getenv(key); v != "" {
		return v
	}
	return fallback
}

func getEnvInt(key string, fallback int) int {
	if v := os.Getenv(key); v != "" {
		if n, err := strconv.Atoi(v); err == nil {
			return n
		}
	}
	return fallback
}
