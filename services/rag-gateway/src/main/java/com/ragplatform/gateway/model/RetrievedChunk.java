package com.ragplatform.gateway.model;

import com.fasterxml.jackson.annotation.JsonProperty;

public record RetrievedChunk(
        @JsonProperty("chunk_id") String chunkId,
        @JsonProperty("document_id") String documentId,
        String content,
        double score
) {}
