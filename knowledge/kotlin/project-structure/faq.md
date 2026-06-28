# Kotlin 项目结构 FAQ

## Q: domain 层真的不能有任何框架依赖吗？

是的。domain 层是业务核心，应保持纯 Kotlin。框架注解（如 `@Entity`）应放在 infrastructure 层的实体中。

## Q: Spring Boot 项目怎么组织？

```
com.example/
├── domain/              # 纯 Kotlin
├── application/         # @Service / @Transactional
├── infrastructure/      # @Repository / @Component
└── presentation/        # @RestController / @ControllerAdvice
```

## Q: Android 项目用 feature 分包还是 layer 分包？

推荐 feature 分包（Google 官方推荐），方便独立开发和测试。

## Q: data class 和普通 class 的区别？

```kotlin
data class User(val id: Long, val name: String)
// 自动生成：toString()、equals()、hashCode()、copy()、componentN()

class User(val id: Long, val name: String)
// 没有上述方法，需要手动实现
```
