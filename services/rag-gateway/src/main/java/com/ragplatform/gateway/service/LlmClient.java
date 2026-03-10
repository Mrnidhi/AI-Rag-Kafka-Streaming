package com.ragplatform.gateway.service;

import com.fasterxml.jackson.databind.JsonNode;
import com.ragplatform.gateway.config.AppConfig;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestClient;

import java.util.List;
import java.util.Map;

@Service
public class LlmClient {

    private static final Logger log = LoggerFactory.getLogger(LlmClient.class);
    private static final String OPENAI_CHAT_URL = "https://api.openai.com/v1/chat/completions";

    private final RestClient restClient;
    private final AppConfig config;

    public LlmClient(RestClient restClient, AppConfig config) {
        this.restClient = restClient;
        this.config = config;
    }

    public LlmResponse complete(String systemPrompt, String userMessage) {
        AppConfig.LlmConfig llm = config.getLlm();

        Map<String, Object> body = Map.of(
                "model", llm.getModel(),
                "max_tokens", llm.getMaxTokens(),
                "temperature", llm.getTemperature(),
                "messages", List.of(
                        Map.of("role", "system", "content", systemPrompt),
                        Map.of("role", "user", "content", userMessage)
                )
        );

        try {
            JsonNode response = restClient.post()
                    .uri(OPENAI_CHAT_URL)
                    .contentType(MediaType.APPLICATION_JSON)
                    .header("Authorization", "Bearer " + llm.getApiKey())
                    .body(body)
                    .retrieve()
                    .body(JsonNode.class);

            if (response == null) {
                return new LlmResponse("Failed to get response from LLM", 0);
            }

            String answer = response
                    .path("choices").path(0)
                    .path("message").path("content")
                    .asText("No response generated");

            int tokens = response.path("usage").path("total_tokens").asInt(0);

            return new LlmResponse(answer, tokens);

        } catch (Exception e) {
            log.error("LLM call failed", e);
            return new LlmResponse("LLM service unavailable", 0);
        }
    }

    public record LlmResponse(String answer, int tokensUsed) {}
}
