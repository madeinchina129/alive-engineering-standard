# Rust 异步编程细则

## 强制规则 (MUST)

### 1. async fn 必须 .await 才有意义

```rust
// ✅ 正确：.await 执行 Future
let body = fetch_data("https://example.com").await;

// ❌ 错误：未 .await 的 Future 不执行
let body = fetch_data("https://example.com");  // ❌ 什么都没发生
```

### 2. 阻塞操作使用 spawn_blocking

```rust
// ✅ 正确：CPU 密集/阻塞操作在 blocking 线程池
let result = tokio::task::spawn_blocking(|| {
    std::thread::sleep(Duration::from_secs(5));
    compute_heavy()
}).await?;

// ❌ 错误：在异步执行器中阻塞线程
async fn heavy() {
    std::thread::sleep(Duration::from_secs(5));  // ❌ 阻塞整个线程池
}
```

### 3. 使用 tokio::select! 处理超时

```rust
// ✅ 正确：select! 超时处理
tokio::select! {
    result = async_operation() => {
        println!("操作完成: {result:?}");
    }
    _ = tokio::time::sleep(Duration::from_secs(10)) => {
        println!("操作超时");
    }
}

// ❌ 错误：没有超时控制
let result = async_operation().await;  // ❌ 可能永远等待
```

### 4. 使用 JoinSet 管理多个任务

```rust
// ✅ 正确：JoinSet 管理任务生命周期
use tokio::task::JoinSet;

let mut set = JoinSet::new();
for url in urls {
    set.spawn(fetch_url(url));
}

while let Some(result) = set.join_next().await {
    match result {
        Ok(data) => println!("成功: {data}"),
        Err(e) => eprintln!("失败: {e}"),
    }
}
```

### 5. async trait 使用 async-trait 宏

```rust
// ✅ 正确：async-trait
#[async_trait]
trait Repository {
    async fn find_by_id(&self, id: i32) -> Result<User, Error>;
}

#[async_trait]
impl Repository for UserRepo {
    async fn find_by_id(&self, id: i32) -> Result<User, Error> {
        // ...
    }
}
```

## 推荐实践 (SHOULD)

### 使用 tokio::spawn 的 handle

```rust
let handle = tokio::spawn(async {
    // 并发工作
});
handle.await??;  // 等待并处理 JoinError
```

## 禁止行为 (MUST NOT)

- ❌ 在 async 上下文中使用 `std::thread::sleep`
- ❌ Future 不 .await 就丢弃
- ❌ 在 async 函数中执行 CPU 密集任务（用 spawn_blocking）
- ❌ 不加超时的网络 IO
- ❌ 在 async fn 中持有跨 .await 的 MutexGuard（应使用 tokio::sync::Mutex）
