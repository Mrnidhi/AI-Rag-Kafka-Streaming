package com.ragplatform.gateway.service;

import com.fasterxml.jackson.databind.JsonNode;
import com.ragplatform.gateway.config.AppConfig;
import com.ragplatform.gateway.model.RetrievedChunk;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestClient;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;

@Service
public class RetrieverService {

    private static final Logger log = LoggerFactory.getLogger(RetrieverService.class);

    private final RestClient restClient;
    private final AppConfig config;

    public RetrieverService(RestClient restClient, AppConfig config) {
        this.restClient = restClient;
        this.config = config;
    }

    public List<RetrievedChunk> retrieve(String query, int topK) {
        String url = config.getEmbeddingServiceUrl() + "/api/v1/search";

        try {
            JsonNode response = restClient.post()
                    .uri(url)
                    .contentType(MediaType.APPLICATION_JSON)
                    .body(Map.of(
                            "query", query,
                            "top_k", topK,
                            "threshold", config.getRetriever().getThreshold()
                    ))
                    .retrieve()
                    .body(JsonNode.class);

            if (response == null || !response.has("results")) {
                return List.of();
            }

            List<RetrievedChunk> chunks = new ArrayList<>();
            for (JsonNode node : response.get("results")) {
                chunks.add(new RetrievedChunk(
                        node.path("chunk_id").asText(),
                        node.path("document_id").asText(),
                        node.path("content").asText(),
                        node.path("score").asDouble()
                ));
            }
            return chunks;

        } catch (Exception e) {
            log.error("retrieval failed for query: {}", query, e);
            return List.of();
        }
    }
}
