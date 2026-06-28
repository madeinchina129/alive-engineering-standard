# Rust 错误处理 FAQ

## Q: `unwrap()` 什么时候可以用？

只在以下场景可以：

```rust
// 1. 测试中
#[test]
fn test_parse() {
    let result = "42".parse::<i32>().unwrap();
    assert_eq!(result, 42);
}

// 2. 确定不会出错（但优先用 expect 说明原因）
let ip = "127.0.0.1".parse::<IpAddr>().expect("硬编码 IP 应合法");
```

生产代码优先用 `?` 或 `match` 处理错误。

## Q: `thiserror` 和 `anyhow` 如何选择？

```
库 crate（给他人用） → thiserror（精确错误类型）
应用 crate（终端）  → anyhow（简化传播）
```

```rust
// mylib（库）：thiserror
use thiserror::Error;
#[derive(Error, Debug)]
pub enum ParseError {
    #[error("无效格式")]
    InvalidFormat,
    #[error("字段缺失: {0}")]
    MissingField(String),
}

// myapp（应用）：anyhow
use anyhow::{Result, Context};
fn run() -> Result<()> {
    let data = mylib::parse(input).context("解析失败")?;
    Ok(())
}
```

## Q: `Box<dyn Error>` 还是自定义错误？

```rust
// 原型/简单应用 → Box<dyn Error>
fn quick_fn() -> Result<(), Box<dyn std::error::Error>> {
    let data = std::fs::read_to_string("file.txt")?;
    Ok(())
}

// 正式项目/需要区分错误类型 → thiserror 自定义枚举
fn business_fn() -> Result<(), AppError> {
    Err(AppError::NotFound("user".into()))
}
```

## Q: `?` 可以在 Option 上用吗？

Rust 1.22+ 支持 `Option` 的 `?`：

```rust
// Option 的 ? 在 None 时提前返回 None
fn get_username(id: u32) -> Option<String> {
    let user = users.iter().find(|u| u.id == id)?;  // None → return None
    Some(user.name.clone())
}

// 混合使用
fn process() -> Result<(), AppError> {
    let value = risky_option().ok_or(AppError::NotFound)?;  // Option → Result
    Ok(())
}
```

## Q: 一个函数中有多种错误类型怎么办？

```rust
// 1. 使用 Box<dyn Error>
fn read_config() -> Result<Config, Box<dyn std::error::Error>> {
    let content = std::fs::read_to_string("config.toml")?;  // io::Error
    let config: Config = toml::from_str(&content)?;         // toml::Error
    Ok(config)
}

// 2. 自定义枚举 + From 实现（推荐）
#[derive(Error, Debug)]
pub enum ConfigError {
    #[error("IO 错误: {0}")]
    Io(#[from] std::io::Error),
    #[error("解析错误: {0}")]
    Parse(#[from] toml::de::Error),
}

fn read_config() -> Result<Config, ConfigError> {
    let content = std::fs::read_to_string("config.toml")?;  // 自动转换
    let config: Config = toml::from_str(&content)?;         // 自动转换
    Ok(config)
}
```

## Q: 什么时候该 `panic!`？

- 不可恢复状态（比如配置格式错误）
- 测试失败
- `unreachable!()` 标记逻辑上不可能的分支
- 示例代码
