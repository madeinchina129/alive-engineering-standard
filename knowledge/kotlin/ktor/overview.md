# Kotlin Ktor 服务端规范

## Ktor 应用结构

Ktor 是 Kotlin 原生的异步 Web 框架，基于协程：

```kotlin
fun main() {
    embeddedServer(Netty, port = 8080) {
        configureRouting()
        configureSerialization()
        configureStatusPages()
    }.start(wait = true)
}

fun Application.configureRouting() {
    routing {
        get("/health") {
            call.respond(mapOf("status" to "UP"))
        }
        route("/api/users") {
            get { /* 获取用户列表 */ }
            post { /* 创建用户 */ }
        }
    }
}
```

### 核心模块

```
Ktor Server
├── Netty / CIO / Jetty   # 引擎
├── Routing               # 路由
├── StatusPages           # 错误处理
├── ContentNegotiation    # JSON 序列化
├── CORS                  # 跨域
├── Authentication        # 认证
└── Sessions              # 会话
```

---

## 配置方式对比

| 方式 | 适用场景 | 配置位置 |
|------|---------|---------|
| `embeddedServer` | 独立应用 | `application.conf` + 代码 |
| `EngineMain` | 标准服务 | `application.conf` |
| 自定义 `Application` | 测试 | 测试代码 |

---

## 适用范围

- **REST API 服务**
- **微服务**
- **WebSocket 服务**
