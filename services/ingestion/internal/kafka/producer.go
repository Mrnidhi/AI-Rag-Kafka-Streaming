package kafka

import (
	"encoding/json"
	"fmt"
	"log"
	"strings"

	"github.com/IBM/sarama"
	"github.com/srinidhigowda/ai-rag-kafka-streaming-platform/services/ingestion/internal/model"
)

type Producer struct {
	producer sarama.SyncProducer
	topic    string
}

func NewProducer(brokers, topic string) (*Producer, error) {
	cfg := sarama.NewConfig()
	cfg.Producer.Return.Successes = true
	cfg.Producer.RequiredAcks = sarama.WaitForAll
	cfg.Producer.Retry.Max = 3

	brokerList := strings.Split(brokers, ",")
	p, err := sarama.NewSyncProducer(brokerList, cfg)
	if err != nil {
		return nil, fmt.Errorf("failed to create kafka producer: %w", err)
	}

	return &Producer{producer: p, topic: topic}, nil
}

func (p *Producer) PublishChunks(chunks []model.Chunk) error {
	for _, chunk := range chunks {
		data, err := json.Marshal(chunk)
		if err != nil {
			return fmt.Errorf("failed to marshal chunk %s: %w", chunk.ID, err)
		}

		msg := &sarama.ProducerMessage{
			Topic: p.topic,
			Key:   sarama.StringEncoder(chunk.DocumentID),
			Value: sarama.ByteEncoder(data),
		}

		partition, offset, err := p.producer.SendMessage(msg)
		if err != nil {
			return fmt.Errorf("failed to publish chunk %s: %w", chunk.ID, err)
		}

		log.Printf("published chunk %s to partition %d offset %d", chunk.ID, partition, offset)
	}
	return nil
}

func (p *Producer) Close() error {
	return p.producer.Close()
}
