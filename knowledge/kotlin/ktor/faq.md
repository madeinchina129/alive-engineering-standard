# Kotlin Ktor FAQ

## Q: Ktor 和 Spring Boot 怎么选？

- **Spring Boot**：企业级、全栈、大量第三方集成
- **Ktor**：轻量、Kotlin 原生、协程优先、配置简单

建议：微服务 / 新项目用 Ktor，遗留系统 / 需要丰富生态用 Spring Boot。

## Q: 怎么测试 Ktor 应用？

```kotlin
fun Application.module() {
    routing {
        get("/health") { call.respondText("OK") }
    }
}

class AppTest {
    @Test
    fun testHealth() = testApplication {
        application { module() }
        val response = client.get("/health")
        assertEquals(HttpStatusCode.OK, response.status)
        assertEquals("OK", response.bodyAsText())
    }
}
```

## Q: 如何处理文件上传？

```kotlin
route("/api/files") {
    post {
        val multipart = call.receiveMultipart()
        multipart.forEachPart { part ->
            when (part) {
                is PartData.FileItem -> {
                    val bytes = part.streamProvider().readBytes()
                    // 保存文件
                }
                is PartData.FormItem -> { /* 表单字段 */ }
            }
        }
    }
}
```

## Q: Ktor 支持 OpenAPI/Swagger 吗？

需要第三方插件：
- `io.ktor:ktor-server-swagger`
- 或手动集成 `openapi-generator`
