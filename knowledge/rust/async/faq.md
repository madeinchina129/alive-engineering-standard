# Rust 异步 FAQ

## Q: `await` 什么时候执行？

Future 是惰性的，`await` 是执行点。调用 `async fn` 只创建 Future，`await` 才开始轮询：

```rust
let fut = fetch_data("url");  // 创建 Future（未执行）
fut.await                      // 开始轮询到完成
```

## Q: tokio 多线程和单线程怎么选？

```rust
// 多线程运行时（默认，适合网络服务）
#[tokio::main]
async fn main() {}

// 单线程运行时（适合轻量级）
#[tokio::main(flavor = "current_thread")]
async fn main() {}
```

多线程适合 CPU 边界 + IO 混合，单线程适合纯 IO 且避免同步开销。

## Q: `std::sync::Mutex` 和 `tokio::sync::Mutex` 的区别？

```rust
// std::sync::Mutex：同步锁，不能跨 .await 持有
let data = std::sync::Mutex::new(0);
async fn add() {
    let mut guard = data.lock().unwrap();  // 获取锁
    *guard += 1;
    // drop(guard) 必须在 .await 之前
    some_async().await;  // ❌ 持有 MutexGuard 跨 .await
}

// tokio::sync::Mutex：异步锁，可跨 .await
let data = tokio::sync::Mutex::new(0);
async fn add() {
    let mut guard = data.lock().await;
    *guard += 1;
    some_async().await;  // ✅ tokio Mutex 支持跨 .await
}
```

## Q: 如何并发执行多个 async 任务？

```rust
// tokio::join!：等待所有完成
let (a, b) = tokio::join!(task1(), task2());

// tokio::try_join!：任一失败即返回
let (a, b) = tokio::try_join!(task1(), task2())?;

// JoinSet：动态数量的任务
let mut set = JoinSet::new();
```

## Q: `spawn` 和 `spawn_blocking` 的区别？

```
spawn：异步任务，在线程池中执行 Future
spawn_blocking：阻塞任务，在专门的阻塞线程池执行
```

```rust
tokio::spawn(async { /* 异步操作 */ });
tokio::task::spawn_blocking(|| { /* 阻塞操作 */ });
```

## Q: 如何使用 Tokio 的 CancellationToken？

```rust
use tokio_util::sync::CancellationToken;

let token = CancellationToken::new();
let child_token = token.child_token();

tokio::spawn(async move {
    tokio::select! {
        _ = child_token.cancelled() => println!("已取消"),
        result = async_operation() => println!("{result:?}"),
    }
});

token.cancel();  // 取消所有关联的任务
```
