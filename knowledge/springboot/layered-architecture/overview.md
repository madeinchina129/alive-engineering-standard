# Layered Architecture 分层架构

## 为什么选择分层架构

### 关注点分离

Spring Boot 项目的标准分层结构：

```
src/main/java/com/example/project/
├── controller/        # HTTP 请求处理
├── service/           # 业务逻辑
├── repository/        # 数据访问
├── domain/            # 领域模型
├── dto/               # 数据传输对象
└── config/            # 配置类
```

每一层都有明确的职责，不允许跨层调用。

### 可测试性

```java
// Controller 层测试 — mock Service
@WebMvcTest(UserController.class)
class UserControllerTest {
    @MockBean
    private UserService userService;
    
    @Test
    void shouldReturnUserList() {
        when(userService.findAll()).thenReturn(List.of(new UserDTO(...)));
        // ...
    }
}

// Service 层测试 — mock Repository
@ExtendWith(MockitoExtension.class)
class UserServiceTest {
    @Mock
    private UserRepository userRepository;
    
    @Test
    void shouldCreateUser() {
        // 纯业务逻辑测试，不依赖 HTTP 和数据库
    }
}
```

### 灵活性

- Controller 层可替换为 GraphQL 或 gRPC 而不影响业务逻辑
- Repository 层可替换为 MyBatis、JPA 或 MongoDB 而不影响业务逻辑
- Service 层是核心业务逻辑，不依赖任何框架

---

## 对比其他架构

| 维度 | 传统三层架构 | DDD 四层架构 | 六边形架构 |
|------|-------------|-------------|-----------|
| 复杂度 | 低 | 高 | 高 |
| 适用场景 | CRUD 应用 | 复杂业务领域 | 多端口适配 |
| 学习成本 | 低 | 高 | 中 |
| 我们的选择 | ✅ 默认 | 复杂业务视情况 | 微服务边界 |

---

## 适用范围

- **强制使用**：所有 Spring Boot 项目
- **CRUD 项目**：Controller → Service → Repository
- **复杂业务**：增加 Domain 层 + Application 层

## 依赖规则

```
Controller → Service → Repository
     ↓           ↓
    DTO        Domain
```

- Controller 层只依赖 Service 层和 DTO
- Service 层只依赖 Repository 层和 Domain
- Repository 层只依赖 Domain 层
- Domain 层不依赖任何框架
