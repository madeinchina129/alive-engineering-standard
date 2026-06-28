# JPA 数据访问规范

## Entity 定义规范

### 基础 Entity

```java
@Entity
@Table(name = "users")
@Getter
@NoArgsConstructor(access = AccessLevel.PROTECTED)
@EntityListeners(AuditingEntityListener.class)
public class User {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, unique = true, length = 100)
    private String email;

    @Column(nullable = false, length = 50)
    private String name;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    private UserStatus status;

    @CreatedDate
    @Column(updatable = false)
    private LocalDateTime createdAt;

    @LastModifiedDate
    private LocalDateTime updatedAt;

    @Version
    private Long version;

    @Builder
    public User(String email, String name) {
        this.email = email;
        this.name = name;
        this.status = UserStatus.ACTIVE;
    }
}
```

### Entity 最佳实践

```java
// 1. 使用 @Getter 而非 @Data（避免 @Setter）
// @Data = @Getter + @Setter + @ToString + @EqualsAndHashCode ← 容易出问题

// 2. 无参构造器 protected
// JPA 需要无参构造器，但不需要对外暴露

// 3. 业务方法在 Entity 中
public void deactivate() {
    this.status = UserStatus.INACTIVE;
}

public void changeEmail(String newEmail) {
    if (!isEmailValid(newEmail)) {
        throw new IllegalArgumentException("Invalid email");
    }
    this.email = newEmail;
}
```

## Repository 定义规范

### 基础 Repository

```java
public interface UserRepository extends JpaRepository<User, Long> {
    // 查询方法命名规则：findBy + 字段名 + 条件
    Optional<User> findByEmail(String email);
    List<User> findByStatus(UserStatus status);
    boolean existsByEmail(String email);
    
    // 分页
    Page<User> findByStatus(UserStatus status, Pageable pageable);
    
    // 排序
    List<User> findByStatusOrderByCreatedAtDesc(UserStatus status);
}
```

### 复杂查询使用 @Query

```java
public interface UserRepository extends JpaRepository<User, Long> {
    
    @Query("SELECT u FROM User u WHERE u.name LIKE %:keyword% OR u.email LIKE %:keyword%")
    List<User> searchByKeyword(@Param("keyword") String keyword);
    
    @Query("SELECT COUNT(u) FROM User u WHERE u.status = :status")
    long countByStatus(@Param("status") UserStatus status);
    
    @Query("SELECT u FROM User u WHERE u.createdAt BETWEEN :start AND :end")
    List<User> findByCreatedAtBetween(@Param("start") LocalDateTime start, @Param("end") LocalDateTime end);
}
```

## 强制规则 (MUST)

### 1. Repository 只定义数据访问方法

```java
// ✅ 正确：Repository 只包含数据访问
public interface UserRepository extends JpaRepository<User, Long> {
    Optional<User> findByEmail(String email);
}

// ❌ 错误：Repository 中包含业务逻辑
public interface UserRepository extends JpaRepository<User, Long> {
    default User findActiveUser(String email) {  // ❌ 业务逻辑在 Service 层
        return findByEmail(email)
            .filter(u -> u.getStatus() == UserStatus.ACTIVE)
            .orElseThrow(() -> new RuntimeException("User not active"));
    }
}
```

### 2. 读写方法分离事务

```java
@Service
@Transactional(readOnly = true)  // 查询方法使用只读事务
public class UserService {
    
    @Transactional  // 写操作覆盖为读写事务
    public UserResponse create(UserCreateRequest request) {
        // ...
    }
}
```

### 3. 批量操作使用 saveAll 和 deleteAllInBatch

```java
// ✅ 批量插入
userRepository.saveAll(users);

// ✅ 批量删除（一条 SQL）
userRepository.deleteAllInBatch(users);

// ❌ 避免循环单条操作
for (User user : users) {
    userRepository.save(user);  // N 条 SQL
}
```

### 4. 关联查询使用 @EntityGraph 避免 N+1

```java
@Entity
@NamedEntityGraph(name = "User.orders", attributeNodes = @NamedAttributeNode("orders"))
public class User {
    @OneToMany(mappedBy = "user")
    private List<Order> orders;
}

public interface UserRepository extends JpaRepository<User, Long> {
    @EntityGraph("User.orders")
    List<User> findAll();  // 一次 JOIN 查询，而非 N+1
}
```

## 推荐实践 (SHOULD)

### 1. 使用 BaseEntity 抽取公共字段

```java
@MappedSuperclass
@EntityListeners(AuditingEntityListener.class)
public abstract class BaseEntity {
    @CreatedDate
    @Column(updatable = false)
    private LocalDateTime createdAt;
    
    @LastModifiedDate
    private LocalDateTime updatedAt;
    
    @Version
    private Long version;
}
```

### 2. 软删除使用 @SQLRestriction

```java
@Entity
@SQLRestriction("deleted = false")  // 全局过滤软删除
public class User extends BaseEntity {
    @Column(nullable = false)
    private boolean deleted = false;
    
    public void softDelete() {
        this.deleted = true;
    }
}
```

## 禁止行为 (MUST NOT)

- ❌ Entity 中直接使用 @Setter（改用业务方法）
- ❌ 在循环中执行单条 SQL
- ❌ Repository 中包含业务逻辑
- ❌ 使用 `@Transactional` 标注 Repository 方法
- ❌ 忽略 N+1 查询问题
- ❌ 查询大量数据时不使用分页
