package com.ragplatform.gateway.service;

import com.ragplatform.gateway.config.AppConfig;
import com.ragplatform.gateway.model.QueryRequest;
import com.ragplatform.gateway.model.QueryResponse;
import com.ragplatform.gateway.model.RetrievedChunk;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.data.redis.core.StringRedisTemplate;
import org.springframework.stereotype.Service;

import java.time.Duration;
import java.util.List;
import java.util.stream.Collectors;

@Service
public class RagService {

    private static final Logger log = LoggerFactory.getLogger(RagService.class);

    private static final String SYSTEM_PROMPT = """
            You are a helpful assistant that answers questions based on the provided context.
            Always ground your answers in the given context. If the context does not contain
            enough information to answer, say so clearly. Include references to which parts
            of the context you used.""";

    private final RetrieverService retrieverService;
    private final LlmClient llmClient;
    private final StringRedisTemplate redisTemplate;
    private final AppConfig config;

    public RagService(
            RetrieverService retrieverService,
            LlmClient llmClient,
            StringRedisTemplate redisTemplate,
            AppConfig config
    ) {
        this.retrieverService = retrieverService;
        this.llmClient = llmClient;
        this.redisTemplate = redisTemplate;
        this.config = config;
    }

    public QueryResponse query(QueryRequest request) {
        long start = System.currentTimeMillis();

        // Check cache
        if (config.getCache().isEnabled()) {
            String cached = redisTemplate.opsForValue().get(cacheKey(request.question()));
            if (cached != null) {
                long elapsed = System.currentTimeMillis() - start;
                return new QueryResponse(cached, List.of(), elapsed, 0);
            }
        }

        List<RetrievedChunk> chunks = retrieverService.retrieve(
                request.question(),
                request.contextLimit()
        );

        String context = chunks.stream()
                .map(c -> "---\n" + c.content() + "\n---")
                .collect(Collectors.joining("\n\n"));

        String userMessage = "Context:\n" + context + "\n\nQuestion: " + request.question();

        LlmClient.LlmResponse llmResponse = llmClient.complete(SYSTEM_PROMPT, userMessage);

        // Cache the response
        if (config.getCache().isEnabled()) {
            try {
                redisTemplate.opsForValue().set(
                        cacheKey(request.question()),
                        llmResponse.answer(),
                        Duration.ofSeconds(config.getCache().getTtlSeconds())
                );
            } catch (Exception e) {
                log.warn("failed to cache response", e);
            }
        }

        long elapsed = System.currentTimeMillis() - start;

        return new QueryResponse(
                llmResponse.answer(),
                chunks,
                elapsed,
                llmResponse.tokensUsed()
        );
    }

    private String cacheKey(String question) {
        return "rag:query:" + question.toLowerCase().strip().hashCode();
    }
}
