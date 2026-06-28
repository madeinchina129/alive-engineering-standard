# Rust 错误处理细则

## 强制规则 (MUST)

### 1. 可恢复错误使用 Result，不 panic

```rust
// ✅ 正确：返回 Result
fn divide(a: f64, b: f64) -> Result<f64, String> {
    if b == 0.0 {
        Err("除数不能为 0".into())
    } else {
        Ok(a / b)
    }
}

// ❌ 错误：可恢复错误不应 panic
fn divide(a: f64, b: f64) -> f64 {
    if b == 0.0 {
        panic!("除数不能为 0")  // ❌ 可恢复错误不应 panic
    }
    a / b
}
```

### 2. 使用 `?` 传播错误

```rust
// ✅ 正确：? 操作符
fn process() -> Result<(), Box<dyn std::error::Error>> {
    let data = std::fs::read_to_string("input.txt")?;
    let parsed: i32 = data.trim().parse()?;
    println!("Parsed: {parsed}");
    Ok(())
}

// ❌ 错误：手动 match 传播
fn process() -> Result<(), Box<dyn std::error::Error>> {
    let data = match std::fs::read_to_string("input.txt") {
        Ok(d) => d,
        Err(e) => return Err(e.into()),
    };
    // ...
    Ok(())
}
```

### 3. 自定义错误使用 thiserror

```rust
// ✅ 正确：thiserror 派生宏
use thiserror::Error;

#[derive(Error, Debug)]
pub enum AppError {
    #[error("用户不存在: {0}")]
    UserNotFound(String),
    
    #[error("权限不足: 需要 {required}, 实际 {actual}")]
    InsufficientPermission { required: String, actual: String },
    
    #[error("数据库错误: {0}")]
    Database(#[from] sqlx::Error),
}

// ❌ 错误：手动实现 Display/Debug
pub enum AppError {
    UserNotFound(String),
}

impl std::fmt::Display for AppError {
    fn fmt(&self, f: &mut std::fmt::Formatter) -> std::fmt::Result {
        match self {
            AppError::UserNotFound(id) => write!(f, "用户不存在: {id}"),
        }
    }
}
```

### 4. 应用层使用 anyhow 简化

```rust
// ✅ 正确：应用层用 anyhow::Result
use anyhow::{Result, Context};

fn process_file(path: &str) -> Result<()> {
    let content = std::fs::read_to_string(path)
        .with_context(|| format!("无法读取文件: {path}"))?;
    
    let config: Config = toml::from_str(&content)
        .context("配置文件格式无效")?;
    
    Ok(())
}
```

### 5. 使用 `.ok()` / `.ok_or()` 转换 Option

```rust
// ✅ 正确：Option → Result
fn find_user(id: &str) -> Result<User, AppError> {
    users
        .iter()
        .find(|u| u.id == id)
        .ok_or_else(|| AppError::UserNotFound(id.into()))
}

// Option 转 Option（丢弃错误信息）
let value = risky_operation().ok();
```

## 推荐实践 (SHOULD)

### 1. 错误包含上下文信息

```rust
// ✅ 附加上下文
let data = std::fs::read_to_string(path)
    .with_context(|| format!("读取配置文件失败: {path}"))?;

// ❌ 缺少上下文
let data = std::fs::read_to_string(path)?;
```

### 2. 库 crate 使用 thiserror，应用使用 anyhow

```rust
// lib crate：thiserror 定义精确错误类型
// mylib/src/error.rs
#[derive(Error, Debug)]
pub enum MyLibError { ... }

// app crate：anyhow 简化传播
// app/src/main.rs
use anyhow::Result;
use mylib::MyLibError;
```

## 禁止行为 (MUST NOT)

- ❌ 用 `panic!` 处理可恢复错误
- ❌ `unwrap()` 直接暴露在生产代码中
- ❌ `expect()` 不带有意义的消息
- ❌ 捕获所有错误打印后继续运行（swallow errors）
- ❌ 在库 crate 中使用 `anyhow`
