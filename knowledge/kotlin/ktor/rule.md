# Kotlin Ktor 细则

## 强制规则 (MUST)

### 1. 使用 ContentNegotiation + kotlinx.serialization

```kotlin
// ✅ 正确：kotlinx.serialization
install(ContentNegotiation) {
    json(Json {
        ignoreUnknownKeys = true
        isLenient = true
        prettyPrint = true
    })
}

@Serializable
data class UserResponse(val id: Long, val name: String)

// ❌ 错误：手动序列化
call.respondText(mapper.writeValueAsString(user), ContentType.Application.Json)
```

### 2. 路由模块化

```kotlin
// ✅ 正确：按资源拆分路由
fun Application.configureUserRoutes() {
    routing {
        route("/api/users") {
            get { /* 列表 */ }
            get("/{id}") { /* 详情 */ }
            post { /* 创建 */ }
            put("/{id}") { /* 更新 */ }
            delete("/{id}") { /* 删除 */ }
        }
    }
}

// ❌ 错误：所有路由在一个文件
fun Application.module() {
    routing {
        get("/api/users") { }
        get("/api/users/{id}") { }
        get("/api/orders") { }
        // ... 越来越多
    }
}
```

### 3. 使用 StatusPages 统一错误处理

```kotlin
// ✅ 正确：全局错误处理
install(StatusPages) {
    exception<ValidationException> { call, cause ->
        call.respond(HttpStatusCode.BadRequest, ErrorResponse(cause.message))
    }
    exception<NotFoundException> { call, cause ->
        call.respond(HttpStatusCode.NotFound, ErrorResponse(cause.message))
    }
    exception<Throwable> { call, cause ->
        call.respond(HttpStatusCode.InternalServerError, ErrorResponse("内部错误"))
    }
}

// ❌ 错误：每个路由重复 try-catch
get("/users/{id}") {
    try {
        // ...
    } catch (e: NotFoundException) {
        call.respond(HttpStatusCode.NotFound, ...)
    }
}
```

### 4. 配置 CORS

```kotlin
// ✅ 正确：明确配置允许的源
install(CORS) {
    allowOrigin("https://myapp.com")
    allowMethod(HttpMethod.Get)
    allowMethod(HttpMethod.Post)
    allowHeader(HttpHeaders.ContentType)
    allowHeader(HttpHeaders.Authorization)
}

// ❌ 错误：允许所有源
install(CORS) { anyHost() }  // ❌ 生产环境不安全
```

### 5. 依赖注入

```kotlin
// ✅ 正确：构造函数注入
class UserService(private val repo: UserRepository)

fun Application.module() {
    val repo = DatabaseUserRepository()
    val service = UserService(repo)
    
    routing {
        get("/api/users") {
            val users = service.getUsers()
            call.respond(users)
        }
    }
}
```

## 禁止行为 (MUST NOT)

- ❌ 在路由 handler 中直接使用数据库
- ❌ 不使用 ContentNegotiation 手动 JSON 序列化
- ❌ CORS 允许所有源
- ❌ 路由 handler 超过 20 行
