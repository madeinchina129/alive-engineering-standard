---
id: springboot.layered_architecture
priority: P0
owner: Java Team
version: 1.0
generated: 2026-06-28
---

# Layered Architecture 分层规范

> **领域**: Spring Boot 开发规范 | **优先级**: P0 | **版本**: 1.0
> 
> Spring Boot 项目分层架构标准，Controller/Service/Repository/DTO 分层职责



---




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





---

## 使用规范

# Layered Architecture 使用规范

## 层职责定义

### Controller 层

```java
@RestController
@RequestMapping("/api/v1/users")
@RequiredArgsConstructor
public class UserController {
    private final UserService userService;

    @GetMapping
    public ResponseEntity<List<UserResponse>> findAll() {
        return ResponseEntity.ok(userService.findAll());
    }

    @GetMapping("/{id}")
    public ResponseEntity<UserResponse> findById(@PathVariable Long id) {
        return ResponseEntity.ok(userService.findById(id));
    }

    @PostMapping
    public ResponseEntity<UserResponse> create(@Valid @RequestBody UserCreateRequest request) {
        return ResponseEntity.status(HttpStatus.CREATED).body(userService.create(request));
    }
}
```

职责：HTTP 入参校验 → 调用 Service → 返回 ResponseEntity

### Service 层

```java
@Service
@Transactional
@RequiredArgsConstructor
public class UserService {
    private final UserRepository userRepository;

    public List<UserResponse> findAll() {
        return userRepository.findAll().stream()
                .map(UserResponse::from)
                .toList();
    }

    public UserResponse findById(Long id) {
        return userRepository.findById(id)
                .map(UserResponse::from)
                .orElseThrow(() -> new ResourceNotFoundException("User not found: " + id));
    }

    public UserResponse create(UserCreateRequest request) {
        if (userRepository.existsByEmail(request.email())) {
            throw new DuplicateResourceException("Email already exists: " + request.email());
        }
        User user = request.toEntity();
        user = userRepository.save(user);
        return UserResponse.from(user);
    }
}
```

职责：业务逻辑编排 → 事务管理 → 异常处理

### Repository 层

```java
public interface UserRepository extends JpaRepository<User, Long> {
    Optional<User> findByEmail(String email);
    boolean existsByEmail(String email);
    List<User> findByStatus(UserStatus status);
}
```

职责：数据访问 → 查询封装

### Domain 层

```java
@Entity
@Table(name = "users")
@Getter
@NoArgsConstructor(access = AccessLevel.PROTECTED)
public class User {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, unique = true)
    private String email;

    @Column(nullable = false)
    private String name;

    @Enumerated(EnumType.STRING)
    private UserStatus status;

    @Builder
    public User(String email, String name) {
        this.email = email;
        this.name = name;
        this.status = UserStatus.ACTIVE;
    }

    public void deactivate() {
        this.status = UserStatus.INACTIVE;
    }
}
```

职责：核心业务实体 → 业务方法

### DTO 层

```java
public record UserCreateRequest(
    @NotBlank String email,
    @NotBlank String name
) {
    public User toEntity() {
        return User.builder()
                .email(email)
                .name(name)
                .build();
    }
}

public record UserResponse(
    Long id,
    String email,
    String name,
    UserStatus status
) {
    public static UserResponse from(User user) {
        return new UserResponse(user.getId(), user.getEmail(), user.getName(), user.getStatus());
    }
}
```

职责：数据传输 → 参数校验注解 → Entity ↔ DTO 转换

## 强制规则 (MUST)

### 1. 严格分层依赖

```java
// ✅ 正确：Controller 调用 Service
// ❌ 禁止：Controller 直接调用 Repository
// ❌ 禁止：Service 直接调用其他 Service 的 Repository
// ❌ 禁止：Domain 层依赖任何框架注解（JPA 注解在 Entity 中是例外）
```

### 2. 禁止跨层返回 Entity

```java
// ✅ 正确：Service 返回 DTO
public UserResponse findById(Long id) { ... }

// ❌ 错误：Service 直接返回 Entity
public User findById(Long id) { ... }
```

### 3. Controller 只做路由和校验

```java
// ✅ 正确：Controller 极简
@GetMapping("/{id}")
public ResponseEntity<UserResponse> findById(@PathVariable Long id) {
    return ResponseEntity.ok(userService.findById(id));
}

// ❌ 错误：Controller 中包含业务逻辑
@GetMapping("/{id}")
public ResponseEntity<UserResponse> findById(@PathVariable Long id) {
    if (id <= 0) throw new IllegalArgumentException(...);
    User user = userRepository.findById(id).orElseThrow(...);
    UserResponse response = new UserResponse(user.getId(), ...);
    return ResponseEntity.ok(response);
}
```

### 4. Service 层保持 @Transactional

```java
@Service
@Transactional(readOnly = true) // 默认只读
public class UserService {
    
    @Transactional // 写操作覆盖
    public UserResponse create(UserCreateRequest request) { ... }
}
```

## 推荐实践 (SHOULD)

### 1. 使用 @RequiredArgsConstructor 替代 @Autowired

```java
// ✅ 推荐
@RequiredArgsConstructor
public class UserService {
    private final UserRepository userRepository;
}
```

### 2. 使用 Record 定义 DTO

```java
public record UserResponse(Long id, String name) { }
```

### 3. Controller 统一响应格式

```java
public record ApiResponse<T>(int code, String message, T data) {
    public static <T> ApiResponse<T> ok(T data) {
        return new ApiResponse<>(200, "success", data);
    }
}
```

## 禁止行为 (MUST NOT)

- ❌ Controller 中调用 Repository
- ❌ Service 返回 Entity 对象给 Controller
- ❌ Domain 层依赖 Spring 注解
- ❌ DTO 包含业务方法
- ❌ Repository 层抛出业务异常





---

## 代码示例

```dart
// Layered Architecture 分层规范 — 示例
// Spring Boot 项目分层架构标准，Controller/Service/Repository/DTO 分层职责
// TODO: 补充具体实现
```





---

## 常见问题

# Layered Architecture FAQ

## Q: 为什么 Service 不能返回 Entity 给 Controller？

A: 耦合风险和安全隐患：
- Entity 包含 JPA 懒加载代理，序列化时可能抛出 LazyInitializationException
- Entity 包含不应暴露给前端的字段（密码、内部状态）
- Entity 变更直接影响到 API 响应格式，违反关注点分离

## Q: 跨 Service 调用怎么处理？

```java
// ✅ 正确：通过 Service 接口调用
@Service
public class OrderService {
    private final UserService userService;
    
    public OrderResponse create(OrderCreateRequest request) {
        UserResponse user = userService.findById(request.userId());
        // ...
    }
}
```

## Q: @Transactional(readOnly = true) 有什么好处？

- 数据库优化：只读事务支持数据库级优化
- 显式意图：标明方法是只读查询
- 写操作安全：防止误写

## Q: 两个 Service 互相依赖怎么办？

A: 这是设计问题，说明职责划分不清晰。解决方案：
1. 提取公共逻辑到第三个 Service
2. 使用事件驱动解耦（ApplicationEventPublisher）
3. 考虑是否应该合并为同一个 Service

## Q: DTO 应该放在哪个包？

A: 推荐两种方式：
1. 独立 dto 包 — 大型项目
2. 放在 Controller 包内 — 小型项目

选择标准：如果 DTO 被多个 Controller 共享，放在独立包。

## Q: 项目中有很多纯查询（读多写少），是否还需要 Service 层？

```java
// 可以简化，但至少保留 Service 接口
@RestController
public class UserController {
    private final UserRepository userRepository; // ❌ 不可直接注入
}
```

即使简单的查询也推荐通过 Service：
```java
@Service
public class UserService {
    public List<UserResponse> findAll() {
        return userRepository.findAll().stream()
                .map(UserResponse::from)
                .toList();
    }
}
```

好处：
- 后续添加缓存/权限检查时不需要修改 Controller
- 保持统一的架构风格





---

## 检查清单

# Layered Architecture Code Review Checklist

## 分层结构
- [ ] 项目是否遵循 Controller → Service → Repository 分层？
- [ ] 是否存在跨层调用？（Controller → Repository）
- [ ] 是否存在循环依赖？

## Controller
- [ ] Controller 是否只做路由和参数校验？
- [ ] Controller 中是否没有业务逻辑？
- [ ] 是否使用 @Valid/@Validated 进行参数校验？
- [ ] 是否返回 ResponseEntity 统一响应格式？

## Service
- [ ] Service 是否使用 @Transactional(readOnly = true) 标注？
- [ ] 写操作是否覆盖了 @Transactional？
- [ ] Service 是否返回 DTO 而非 Entity？
- [ ] Service 中是否没有直接调用 HttpServletRequest/Response？

## Repository
- [ ] Repository 是否只包含数据访问方法？
- [ ] Repository 中是否没有业务逻辑？
- [ ] 查询方法命名是否遵循 JPA 规范？
- [ ] 复杂查询是否使用 @Query 或 QueryDSL？

## Domain
- [ ] Domain/Entity 是否有业务方法？
- [ ] Domain 层是否不依赖 Spring 注解？
- [ ] JPA 注解是否仅限于 Entity 类？
- [ ] Entity 是否使用 @Getter 而非 @Setter 或 @Data？

## DTO
- [ ] DTO 是否使用 Record 或 immutable class？
- [ ] DTO 是否不包含业务逻辑？
- [ ] Request DTO 是否有校验注解？
- [ ] Entity ↔ DTO 转换是否在 DTO 层完成？

## 依赖注入
- [ ] 是否使用 @RequiredArgsConstructor 而非 @Autowired？
- [ ] 注入的依赖是否都是 final？

## 异常处理
- [ ] 业务异常是否在 Service 层抛出？
- [ ] 是否使用全局 @ControllerAdvice 处理异常？
- [ ] 是否没有吞掉异常（空的 catch 块）？





---

## AI Prompt

你是一个 Spring Boot 架构专家，精通分层架构（Layered Architecture）。请根据以下规范回答问题。

## 核心规范

### 分层结构
```
Controller → Service → Repository → DB
    ↓           ↓
   DTO        Domain
```

### 层职责
- **Controller**: HTTP 路由 + @Valid 参数校验，不包含业务逻辑
- **Service**: 业务逻辑 + @Transactional，返回 DTO 而非 Entity
- **Repository**: 数据访问，不包含业务逻辑
- **Domain/Entity**: 核心业务实体 + 业务方法，不依赖框架注解
- **DTO**: Request/Response 数据载体，使用 Record 类型

### 强制规则
1. 禁止跨层调用（Controller → Repository）
2. 禁止 Service 返回 Entity 给 Controller
3. Controller 只做路由和校验
4. Service 使用 @Transactional(readOnly = true) 默认只读
5. Domain 层不依赖 Spring 注解
6. 使用 @RequiredArgsConstructor 替代 @Autowired

### 依赖注入
- final field + @RequiredArgsConstructor
- 避免 @Autowired on field

### 异常处理
- 业务异常在 Service 抛出
- ControllerAdvice 全局处理
- 不吞异常

## 代码审查检查
审查时检查：分层依赖方向、DTO 使用、事务标注、跨层调用、Entity 暴露。




---

*本文档由 AES Knowledge Generator 自动生成。知识源：`knowledge/springboot/layered-architecture/`*