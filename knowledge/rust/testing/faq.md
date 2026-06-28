# Rust 测试 FAQ

## Q: 单元测试和集成测试的区别？

```
单元测试：测试私有逻辑，和源文件在一起
集成测试：测试公共 API，在 tests/ 目录中
```

```rust
// 单元测试可以测试私有函数
// src/user.rs
fn validate_email(email: &str) -> bool {
    email.contains('@')
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn test_validate_email() {
        assert!(validate_email("a@b.com"));  // 可以测试私有函数
    }
}
```

## Q: `#[cfg(test)]` 的作用？

`#[cfg(test)]` 条件编译——测试模块只在 `cargo test` 时编译，不包含在 release 二进制中。避免测试依赖（如 `mockall`）进入生产。

## Q: 如何 mock 依赖？

```rust
// 使用 mockall crate
#[automock]
trait Database {
    fn get_user(&self, id: i32) -> Result<User, Error>;
}

#[test]
fn test_service() {
    let mut mock = MockDatabase::new();
    mock.expect_get_user()
        .with(eq(1))
        .returning(|_| Ok(User { id: 1, name: "Alice".into() }));
    
    let service = UserService::new(mock);
    let user = service.get_user(1).unwrap();
    assert_eq!(user.name, "Alice");
}
```

## Q: 如何测试 async 函数？

```rust
#[tokio::test]
async fn test_async_fetch() {
    let result = fetch_data("https://example.com").await;
    assert!(result.is_ok());
}
```

需要在 `Cargo.toml` 中配置 tokio 的 `test` feature。

## Q: `#[should_panic]` 什么时候用？

```rust
#[test]
#[should_panic(expected = "除数为 0")]
fn test_divide_by_zero() {
    divide(10, 0);
}

// 更推荐的方法是返回 Result
#[test]
fn test_divide_by_zero() -> Result<(), String> {
    let result = divide(10, 0);
    assert!(result.is_err());
    Ok(())
}
```

## Q: 测试文件默认是并行执行的，怎么控制？

```rust
// 默认并行执行测试
// 需要串行时使用 --
// cargo test -- --test-threads=1

// 或者用 serial_test crate
#[test]
#[serial]
fn test_database_operation() { /* ... */ }
```
