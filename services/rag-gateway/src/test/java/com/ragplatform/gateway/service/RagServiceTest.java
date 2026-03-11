package com.ragplatform.gateway.service;

import com.ragplatform.gateway.config.AppConfig;
import com.ragplatform.gateway.model.QueryRequest;
import com.ragplatform.gateway.model.QueryResponse;
import com.ragplatform.gateway.model.RetrievedChunk;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.data.redis.core.StringRedisTemplate;
import org.springframework.data.redis.core.ValueOperations;

import java.util.List;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.*;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
class RagServiceTest {

    @Mock private RetrieverService retrieverService;
    @Mock private LlmClient llmClient;
    @Mock private StringRedisTemplate redisTemplate;
    @Mock private ValueOperations<String, String> valueOps;

    private RagService ragService;
    private AppConfig config;

    @BeforeEach
    void setUp() {
        config = new AppConfig();
        config.setEmbeddingServiceUrl("http://localhost:8001");
        config.getCache().setEnabled(false);
        ragService = new RagService(retrieverService, llmClient, redisTemplate, config);
    }

    @Test
    void queryReturnsAnswerWithSources() {
        var chunks = List.of(
                new RetrievedChunk("c1", "d1", "RAG combines retrieval with generation", 0.9)
        );

        when(retrieverService.retrieve(anyString(), anyInt())).thenReturn(chunks);
        when(llmClient.complete(anyString(), anyString()))
                .thenReturn(new LlmClient.LlmResponse("RAG is a technique...", 150));

        var request = new QueryRequest("What is RAG?", 5, false);
        QueryResponse response = ragService.query(request);

        assertNotNull(response);
        assertEquals("RAG is a technique...", response.answer());
        assertEquals(1, response.sources().size());
        assertEquals(150, response.tokensUsed());
    }

    @Test
    void queryWithEmptyRetrievalStillCallsLlm() {
        when(retrieverService.retrieve(anyString(), anyInt())).thenReturn(List.of());
        when(llmClient.complete(anyString(), anyString()))
                .thenReturn(new LlmClient.LlmResponse("I don't have enough context.", 50));

        var request = new QueryRequest("Unknown topic?", 5, false);
        QueryResponse response = ragService.query(request);

        assertNotNull(response);
        assertTrue(response.sources().isEmpty());
    }
}
