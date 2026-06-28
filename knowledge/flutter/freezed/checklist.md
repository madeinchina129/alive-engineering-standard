# Freezed Code Review Checklist

## 模型定义
- [ ] 所有 API 数据模型是否使用 @freezed？
- [ ] 是否包含 `fromJson` 工厂方法？
- [ ] 是否使用 `@Default` 提供默认值？
- [ ] const factory 构造函数是否使用了命名参数？

## Union 类型
- [ ] 有限状态是否使用了 sealed class？
- [ ] Union 类型是否使用 when/map 模式匹配？
- [ ] 是否避免了 is 类型检查和强制转换？

## 序列化
- [ ] JSON 字段命名是否和 API 一致？（@JsonKey 处理不一致）
- [ ] 嵌套模型是否正确处理？
- [ ] 泛型模型的 fromJsonT 参数是否正确传递？

## 模型组织
- [ ] 模型文件是否集中在 models/ 目录？
- [ ] 大型模型是否拆分为更小的模型？
- [ ] 自动生成文件是否添加到 .gitignore？

## 代码质量
- [ ] 模型类中是否没有业务逻辑？
- [ ] 是否没有编辑自动生成的文件？
- [ ] 是否使用了 const 构造函数？
- [ ] 是否避免了 mutable 集合类型？
