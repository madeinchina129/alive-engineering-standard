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
