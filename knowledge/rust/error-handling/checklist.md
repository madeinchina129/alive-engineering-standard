# Rust 错误处理 Checklist

## Result/Option
- [ ] 可恢复错误是否使用 Result 而非 panic？
- [ ] 可能为空是否使用 Option 而非 null 或哨兵值？
- [ ] `?` 是否用于传播错误？
- [ ] 是否避免在库代码中使用 `unwrap()`？

## 自定义错误
- [ ] 是否使用 `thiserror` 派生自定义错误枚举？
- [ ] 错误枚举是否带有有意义的 `#[error("...")]` 消息？
- [ ] 是否有错误分类（用户错误 vs 系统错误）？
- [ ] 错误消息是否包含上下文信息？

## 错误传播
- [ ] 应用层是否使用 `anyhow::Result` + `Context`？
- [ ] 库层是否使用精确的 `thiserror` 枚举？
- [ ] 混合类型错误是否有 From 实现或 Box<dyn Error>？
- [ ] Option 转 Result 是否使用 `ok_or_else()`？

## 禁止行为
- [ ] 是否避免用 `panic!` 处理可恢复错误？
- [ ] 生产代码是否避免 `unwrap()`？
- [ ] `expect()` 是否带有有意义的错误消息？
- [ ] 是否避免吞掉错误（空 catch）？
- [ ] 库 crate 是否避免使用 `anyhow`？

## 工具检查
- [ ] `cargo clippy` 是否零 warning？
- [ ] 是否运行了 `cargo test`？
