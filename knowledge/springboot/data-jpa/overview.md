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
