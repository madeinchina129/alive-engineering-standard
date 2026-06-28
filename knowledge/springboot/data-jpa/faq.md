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
