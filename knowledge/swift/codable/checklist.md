# Swift Codable Checklist

## Codable 基础
- [ ] Model 是否遵循 Codable 协议？
- [ ] 是否使用 CodingKeys 处理命名差异？
- [ ] 可选字段是否使用 `decodeIfPresent`？
- [ ] 是否有合理的默认值？

## 解码配置
- [ ] JSONDecoder 是否统一配置（extension）？
- [ ] keyDecodingStrategy 是否设置（.convertFromSnakeCase）？
- [ ] dateDecodingStrategy 是否设置？
- [ ] 是否避免每个解码点重复配置？

## 自定义实现
- [ ] 复杂类型是否自定义 init(from:)？
- [ ] 嵌套 JSON 是否使用泛型包装？
- [ ] 是否避免不必要的完整手动实现？

## 错误处理
- [ ] 解码错误是否被 try-catch 捕获？
- [ ] 是否避免 force try（try!）？
- [ ] 是否有 fallback 值处理？
