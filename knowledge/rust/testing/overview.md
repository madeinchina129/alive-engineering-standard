# Rust 测试规范

## 测试策略

Rust 内置测试框架，无需额外测试库：

```rust
#[test]
fn test_addition() {
    assert_eq!(2 + 2, 4);
}

#[test]
fn test_with_result() -> Result<(), String> {
    if 2 + 2 == 4 { Ok(()) } else { Err("2+2 != 4".into()) }
}
```

### 测试金字塔

```
      ╱  E2E  ╲         集成测试在 tests/ 目录
     ╱  集成   ╲        
    ╱  单元测试  ╲      #[cfg(test)] mod tests 内联
   ━━━━━━━━━━━━━━━
```

---

## 测试类型

| 类型 | 位置 | 用途 |
|------|------|------|
| 单元测试 | `src/**/*.rs` 中的 `#[cfg(test)] mod tests` | 函数/模块内部测试 |
| 集成测试 | `tests/` 目录下 `.rs` 文件 | 公共 API 测试 |
| 文档测试 | `///` doc comment 中的代码块 | 文档示例即测试 |
| Bench | `#[bench]`（nightly）/ criterion | 性能基准测试 |

---

```rust
// 文档测试：文档中的代码块自动成为测试
/// ```
/// let result = add(2, 2);
/// assert_eq!(result, 4);
/// ```
fn add(a: i32, b: i32) -> i32 { a + b }
```

---

## 适用范围

- **单元测试**：所有函数和模块
- **集成测试**：公共 API 和跨模块功能
- **文档测试**：所有公开 API
