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
