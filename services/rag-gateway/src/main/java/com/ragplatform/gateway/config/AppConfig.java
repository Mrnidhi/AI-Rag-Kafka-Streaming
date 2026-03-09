package com.ragplatform.gateway.config;

import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.client.RestClient;

@Configuration
@ConfigurationProperties(prefix = "rag")
public class AppConfig {

    private String embeddingServiceUrl;
    private LlmConfig llm = new LlmConfig();
    private RetrieverConfig retriever = new RetrieverConfig();
    private CacheConfig cache = new CacheConfig();
    private RateLimitConfig rateLimit = new RateLimitConfig();

    @Bean
    public RestClient restClient() {
        return RestClient.create();
    }

    public String getEmbeddingServiceUrl() { return embeddingServiceUrl; }
    public void setEmbeddingServiceUrl(String embeddingServiceUrl) { this.embeddingServiceUrl = embeddingServiceUrl; }
    public LlmConfig getLlm() { return llm; }
    public void setLlm(LlmConfig llm) { this.llm = llm; }
    public RetrieverConfig getRetriever() { return retriever; }
    public void setRetriever(RetrieverConfig retriever) { this.retriever = retriever; }
    public CacheConfig getCache() { return cache; }
    public void setCache(CacheConfig cache) { this.cache = cache; }
    public RateLimitConfig getRateLimit() { return rateLimit; }
    public void setRateLimit(RateLimitConfig rateLimit) { this.rateLimit = rateLimit; }

    public static class LlmConfig {
        private String provider = "openai";
        private String apiKey;
        private String model = "gpt-4";
        private int maxTokens = 1024;
        private double temperature = 0.3;

        public String getProvider() { return provider; }
        public void setProvider(String provider) { this.provider = provider; }
        public String getApiKey() { return apiKey; }
        public void setApiKey(String apiKey) { this.apiKey = apiKey; }
        public String getModel() { return model; }
        public void setModel(String model) { this.model = model; }
        public int getMaxTokens() { return maxTokens; }
        public void setMaxTokens(int maxTokens) { this.maxTokens = maxTokens; }
        public double getTemperature() { return temperature; }
        public void setTemperature(double temperature) { this.temperature = temperature; }
    }

    public static class RetrieverConfig {
        private int topK = 5;
        private double threshold = 0.7;

        public int getTopK() { return topK; }
        public void setTopK(int topK) { this.topK = topK; }
        public double getThreshold() { return threshold; }
        public void setThreshold(double threshold) { this.threshold = threshold; }
    }

    public static class CacheConfig {
        private boolean enabled = true;
        private int ttlSeconds = 3600;

        public boolean isEnabled() { return enabled; }
        public void setEnabled(boolean enabled) { this.enabled = enabled; }
        public int getTtlSeconds() { return ttlSeconds; }
        public void setTtlSeconds(int ttlSeconds) { this.ttlSeconds = ttlSeconds; }
    }

    public static class RateLimitConfig {
        private int requestsPerMinute = 60;

        public int getRequestsPerMinute() { return requestsPerMinute; }
        public void setRequestsPerMinute(int requestsPerMinute) { this.requestsPerMinute = requestsPerMinute; }
    }
}
