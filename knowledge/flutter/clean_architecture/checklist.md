# Clean Architecture Code Review Checklist

## 目录结构
- [ ] 项目是否遵循 domain/data/presentation 三层结构？
- [ ] Domain 层是否零依赖？（没有 Flutter/Dio 导入）
- [ ] Data 层是否实现了 Domain 层的接口？
- [ ] Presentation 层是否只依赖 Domain 层？

## Domain 层
- [ ] Entity 是否纯 Dart 类？（无序列化注解）
- [ ] Repository 是否定义为抽象接口？
- [ ] UseCase 是否每个只做一件事？
- [ ] UseCase 命名是否清晰？（GetUsers, CreateUser, DeleteUser）
- [ ] 错误类型是否使用 Either/Failure 模式？

## Data 层
- [ ] DTO 是否转换为 Entity 后才返回？（不直接将 DTO 传到 UI）
- [ ] RepositoryImpl 是否正确处理了所有边缘情况？
- [ ] DataSource 是否只负责单一数据源？
- [ ] 缓存策略是否在 Repository 层实现？

## Presentation 层
- [ ] Provider 是否调用 UseCase 而非直接调用 Repository？
- [ ] UI 是否通过 Provider 访问状态？
- [ ] 是否没有在 Widget 中直接调用 DataSource？
- [ ] 错误是否在 Provider 层处理？

## 数据流
- [ ] 数据流方向是否正确：UI → Provider → UseCase → Repository → DataSource？
- [ ] 是否存在反向依赖？
- [ ] 依赖注入是否通过 Riverpod 实现？
- [ ] 是否避免了 UseCase 之间的直接依赖？

## 测试
- [ ] Domain 层是否可以纯单元测试？
- [ ] Repository 接口是否可以 mock？
- [ ] UseCase 是否可以独立测试？
