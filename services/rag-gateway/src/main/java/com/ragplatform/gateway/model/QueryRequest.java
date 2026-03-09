package com.ragplatform.gateway.model;

import jakarta.validation.constraints.NotBlank;

public record QueryRequest(
        @NotBlank String question,
        Integer contextLimit,
        Boolean stream
) {
    public QueryRequest {
        if (contextLimit == null) contextLimit = 5;
        if (stream == null) stream = false;
    }
}
