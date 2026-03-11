package com.ragplatform.gateway;

import org.junit.jupiter.api.Test;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.TestPropertySource;

@SpringBootTest
@TestPropertySource(properties = {
        "spring.data.redis.host=localhost",
        "spring.data.redis.port=6379",
        "rag.llm.api-key=test-key"
})
class RagGatewayApplicationTests {

    @Test
    void contextLoads() {
    }
}
