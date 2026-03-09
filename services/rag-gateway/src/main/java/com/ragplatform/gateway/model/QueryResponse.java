package com.ragplatform.gateway.model;

import java.util.List;

public record QueryResponse(
        String answer,
        List<RetrievedChunk> sources,
        long latencyMs,
        int tokensUsed
) {}
