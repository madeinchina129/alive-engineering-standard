---
id: springboot.data_jpa
priority: P1
owner: Java Team
version: 1.0
generated: 2026-06-28
---

# JPA 数据访问规范

> **领域**: Spring Boot 开发规范 | **优先级**: P1 | **版本**: 1.0
> 
> Spring Data JPA 使用规范，Entity/Repository 定义，查询方法

> **关联规范**: [Layered Architecture 分层规范](../20_SpringBoot/2001_LayeredArchitecture.md)


---

---

# JPA 数据访问方案

## 为什么选择 Spring Data JPA

### 声明式查询

```java
public interface UserRepository extends JpaRepository<User, Long> {
    // 方法命名查询 — 无需 SQL
    Optional<User> findByEmail(String email);
    List<User> findByStatus(UserStatus status);
    boolean existsByEmail(String email);
    
    // 分页查询
    Page<User> findByStatus(UserStatus status, Pageable pageable);
    
    // 复杂查询 — JPQL
    @Query("SELECT u FROM User u WHERE u.name LIKE %:keyword%")
    List<User> searchByName(@Param("keyword") String keyword);
}
```

### 自动实现

JpaRepository 提供了开箱即用的 CRUD：
- `save(entity)` — 插入/更新
- `findById(id)` — 主键查询
- `findAll()` — 全部查询
- `findAll(Pageable)` — 分页查询
- `deleteById(id)` — 删除
- `count()` — 计数

### 乐观锁支持

```java
@Entity
public class Product {
    @Version
    private Long version;  // 自动乐观锁
}
```

### 审计字段自动填充

```java
@EntityListeners(AuditingEntityListener.class)
public abstract class BaseEntity {
    @CreatedDate
    private LocalDateTime createdAt;
    
    @LastModifiedDate
    private LocalDateTime updatedAt;
}
```

---

## 对比其他方案

| 维度 | Spring Data JPA | MyBatis | JDBC Template |
|------|----------------|---------|---------------|
| SQL 控制 | 自动生成/JPQL | 手写 SQL | 手写 SQL |
| 开发效率 | 最高 | 中 | 低 |
| 复杂查询 | JPQL 或 Specification | XML SQL | 手写 |
| 性能调优 | 一级/二级缓存 | 原生 SQL | 无 |
| 学习成本 | 中 | 低 | 低 |

---

## 适用范围

- **强制使用**：所有关系型数据库访问
- **复杂查询**：使用 @Query + JPQL
- **动态查询**：使用 Specification / QueryDSL


---

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


---

# JPA FAQ

## Q: JpaRepository 和 CrudRepository 如何选择？

A: 始终使用 `JpaRepository`。它继承了 `CrudRepository` 和 `PagingAndSortingRepository`，提供完整的 CRUD + 分页 + 批量操作。

## Q: @Getter 和 @Data 在 Entity 中如何选择？

A: 使用 `@Getter` 而非 `@Data`。`@Data` 会生成 `@Setter`（违反 Entity 不可变性）、`equalsAndHashCode`（可能触发懒加载）、`toString`（可能触发 N+1）。

## Q: 如何避免 N+1 查询？

A: 四种方式：
```java
// 1. @EntityGraph（推荐）
@EntityGraph(attributePaths = {"orders"})
List<User> findAllWithOrders();

// 2. JOIN FETCH（JPQL）
@Query("SELECT u FROM User u JOIN FETCH u.orders")
List<User> findAllWithOrders();

// 3. @BatchSize（部分优化）
@BatchSize(size = 10)
@OneToMany(mappedBy = "user")
private List<Order> orders;

// 4. QueryDSL（复杂场景）
```

## Q: @Transactional(readOnly = true) 真的能优化性能吗？

A: 能：
- 设置 `FlushMode.MANUAL`（不自动 flush）
- 数据库可以优化只读查询
- 防止误写

但不适用于所有数据库（MySQL 对 readOnly 事务的优化有限）。

## Q: 自增 ID 和 UUID 主键怎么选？

- **自增 ID**：性能最优，但暴露增长规律
- **UUID**：不暴露 ID 规律，适合分布式，但索引性能差
- **Snowflake**：不暴露 ID 规律，分布式友好，推荐

```java
// Snowflake ID 生成器
@Id
private Long id;  // 由应用层生成，而非数据库
```

## Q: @Version 乐观锁怎么处理冲突？

```java
// 乐观锁冲突抛出 OptimisticLockException
// 在 Service 层重试
@Transactional
public OrderResponse placeOrder(OrderRequest request) {
    try {
        return tryPlaceOrder(request);
    } catch (OptimisticLockException e) {
        // 重试一次
        return tryPlaceOrder(request);
    }
}
```


---

# JPA Code Review Checklist

## Entity 定义
- [ ] 是否使用 @Getter 而非 @Data？
- [ ] 无参构造器是否 protected？
- [ ] 是否使用 @Builder 模式？
- [ ] 是否使用 @CreatedDate / @LastModifiedDate？
- [ ] 是否使用了 @Version 乐观锁？
- [ ] 字段长度是否通过 @Column(length) 限制？
- [ ] 枚举是否使用 @Enumerated(EnumType.STRING)？

## Repository
- [ ] Repository 是否只包含数据访问方法？
- [ ] Repository 中是否没有业务逻辑？
- [ ] 查询方法命名是否遵循规范？
- [ ] 复杂查询是否使用 @Query？
- [ ] 是否避免了 N+1 查询？

## 事务管理
- [ ] Service 层是否使用 @Transactional(readOnly = true)？
- [ ] 写方法是否覆盖 @Transactional？
- [ ] 是否没有在 Repository 层加 @Transactional？
- [ ] 批量操作是否使用 saveAll/deleteAllInBatch？

## 性能
- [ ] 是否避免了循环中的单条 SQL？
- [ ] 大量数据是否使用分页查询？
- [ ] 关联查询是否使用了 @EntityGraph？
- [ ] 是否配置了合理的 fetch strategy？

## 安全
- [ ] 是否使用了参数化查询？（@Query + @Param）
- [ ] 是否避免了 SQL 注入风险？
- [ ] 软删除是否使用 @SQLRestriction？
- [ ] 密码等敏感数据是否加密存储？


---

你是一个 Spring Boot JPA 数据访问专家。请根据以下规范回答问题。

## 核心规范

### Entity 定义
- 使用 @Getter 而非 @Data
- 无参构造器 protected
- @Builder 模式创建实例
- @CreatedDate + @LastModifiedDate 审计
- @Version 乐观锁
- @Enumerated(EnumType.STRING)
- 业务方法在 Entity 中（`activate()`, `deactivate()`）

### Repository
- 继承 JpaRepository
- 只包含数据访问方法，无业务逻辑
- 方法命名查询遵循规范（`findBy...`, `existsBy...`）
- 复杂查询使用 @Query + JPQL
- 关联查询使用 @EntityGraph 避免 N+1

### 事务
- Service 类级 @Transactional(readOnly = true)
- 写方法 @Transactional 覆盖
- Repository 不加 @Transactional
- 批量操作 saveAll / deleteAllInBatch

### 强制规则
1. Repository 无业务逻辑
2. 禁止循环单条 SQL
3. 禁止 N+1 查询
4. 禁止 @Setter 在 Entity（改用业务方法）
5. 禁止 Repository 标注 @Transactional

## 代码审查检查
审查时检查：Entity 定义规范、Repository 职责、N+1 防范、事务配置、批量操作、参数化查询。



---

*本文档由 AES Knowledge Generator 自动生成。知识源：`knowledge/springboot/data-jpa/`*
