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
