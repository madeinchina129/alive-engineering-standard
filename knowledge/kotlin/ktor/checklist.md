# Kotlin Ktor Checklist

## 项目结构
- [ ] 路由是否按资源模块拆分？
- [ ] 业务逻辑是否在 handler 外部？
- [ ] 依赖是否通过构造函数注入？
- [ ] 配置文件是否使用 `application.conf` / `application.yaml`？

## 序列化
- [ ] 是否使用 `ContentNegotiation` + kotlinx.serialization？
- [ ] JSON 配置是否设置了 `ignoreUnknownKeys`？
- [ ] response 类型是否是 `@Serializable` data class？

## 错误处理
- [ ] 是否使用 `StatusPages` 统一处理异常？
- [ ] 领域异常是否映射到标准 HTTP 状态码？
- [ ] 生产环境是否隐藏堆栈信息？

## 安全
- [ ] CORS 是否只配置了必要的源？
- [ ] 敏感端点是否有认证/授权？
- [ ] HTTPS 是否强制？

## 测试
- [ ] 是否使用 `testApplication` 测试路由？
- [ ] 是否覆盖成功和错误两种情况？
