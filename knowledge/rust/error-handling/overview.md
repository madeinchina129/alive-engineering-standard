# Rust 错误处理规范

## Result 与 Option

Rust 没有异常，使用 `Result<T, E>` 和 `Option<T>` 处理可恢复错误：

```rust
// Result：可能成功或失败
enum Result<T, E> {
    Ok(T),    // 成功
    Err(E),   // 失败
}

// Option：可能有值或为空
enum Option<T> {
    Some(T),  // 有值
    None,     // 无值
}
```

### 基本用法

```rust
// 文件读取，Result<String, io::Error>
let content = std::fs::read_to_string("config.toml");
match content {
    Ok(data) => println!("{data}"),
    Err(e) => eprintln!("读取失败: {e}"),
}

// HashMap 查找，Option<&V>
let value = map.get("key");
match value {
    Some(v) => println!("{v}"),
    None => println!("未找到"),
}
```

---

## 错误传播

使用 `?` 操作符简化错误传播：

```rust
// ✅ 正确：? 自动传播错误
fn read_config(path: &str) -> Result<String, io::Error> {
    let content = std::fs::read_to_string(path)?;  // Err 时 return
    Ok(content)
}

// 等价于
fn read_config(path: &str) -> Result<String, io::Error> {
    let content = match std::fs::read_to_string(path) {
        Ok(data) => data,
        Err(e) => return Err(e),
    };
    Ok(content)
}
```

---

## 错误处理策略选择

| 错误类型 | 处理方式 | 示例 |
|---------|---------|------|
| 可恢复错误 | `Result<T, E>` + `?` | 文件未找到、网络超时 |
| 不可恢复错误 | `panic!` | 越界访问、不可达状态 |
| 可能是空值 | `Option<T>` | 缓存未命中、集合中找不到 |
| 业务错误 | 自定义 `Error` 枚举 | 余额不足、权限不足 |

---

## 适用范围

- **强制使用**：所有 Rust 项目使用 Result/Option，不得使用 panic 处理可恢复错误
- **工具**：`cargo clippy`、`thiserror`、`anyhow` 库
