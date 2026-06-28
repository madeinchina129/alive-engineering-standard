# Rust 测试细则

## 强制规则 (MUST)

### 1. 单元测试内嵌在源文件中

```rust
// ✅ 正确：测试模块和源文件在一起
// src/math.rs
pub fn add(a: i32, b: i32) -> i32 { a + b }

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_add() {
        assert_eq!(add(2, 2), 4);
    }
}

// ❌ 错误：单元测试放在单独的测试文件中
// tests/math_test.rs 中测试私有函数（无法访问）
```

### 2. 集成测试放在 tests/ 目录

```rust
// ✅ 正确：tests/api_test.rs
// tests/api_test.rs
use myapp::create_server;

#[test]
fn test_health_check() {
    let server = create_server();
    let resp = reqwest::blocking::get("http://localhost:8080/health").unwrap();
    assert!(resp.status().is_success());
}
```

### 3. 测试函数返回 Result 用于 ? 操作符

```rust
// ✅ 正确：返回 Result 方便使用 ?
#[test]
fn test_database() -> Result<(), Box<dyn std::error::Error>> {
    let db = Database::connect(":memory:")?;
    let user = db.create_user("Alice")?;
    assert_eq!(user.name, "Alice");
    Ok(())
}

// ❌ 错误：unwrap 可能导致测试可读性差
#[test]
fn test_database() {
    let db = Database::connect(":memory:").unwrap();
    let user = db.create_user("Alice").unwrap();
    assert_eq!(user.name, "Alice");
}
```

### 4. 文档测试必须包含断言

```rust
// ✅ 正确：文档测试有 assert
/// ```
/// let result = divide(10, 2);
/// assert_eq!(result, 5);
/// ```

// ❌ 错误：文档测试没有断言
/// ```
/// let result = divide(10, 2);
/// // 不 assert，无法验证结果
/// ```
```

### 5. 使用 assert! / assert_eq! / assert_ne!，不用 println

```rust
// ✅ 正确
assert_eq!(result, expected, "结果应为 {expected}, 实际为 {result}");

// ❌ 错误：println 调试后在测试中残留
println!("result: {result}");
assert!(result > 0);
```

## 推荐实践 (SHOULD)

### 测试模块化

```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_new_user() { /* ... */ }

    #[test]
    fn test_user_defaults() { /* ... */ }

    mod validation_tests {
        use super::*;

        #[test]
        fn test_invalid_email() { /* ... */ }
    }
}
```

## 禁止行为 (MUST NOT)

- ❌ 测试依赖外部网络（集成测试应 mock）
- ❌ 共享可变测试状态（测试间相互影响）
- ❌ 使用 `#[ignore]` 隐藏失败测试（标记 bug 时例外）
- ❌ 不 assert 的测试
