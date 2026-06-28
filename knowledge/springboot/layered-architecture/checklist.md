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
