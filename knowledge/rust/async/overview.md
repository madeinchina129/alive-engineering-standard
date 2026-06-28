# Rust 异步编程规范

## 异步模型

Rust 使用 **协作式多任务** 模型，通过 `async/.await` + 运行时（tokio/async-std）实现异步：

```rust
use tokio::time::{sleep, Duration};

async fn fetch_data(url: &str) -> Result<String, reqwest::Error> {
    let resp = reqwest::get(url).await?;
    let body = resp.text().await?;
    Ok(body)
}

#[tokio::main]
async fn main() {
    let data = fetch_data("https://api.example.com").await;
    println!("{data:?}");
}
```

### 核心概念

```rust
// async fn → 返回 Future，惰性执行
async fn hello() -> String {
    "Hello".to_string()
}

// .await → 在当前 Future 上轮询
let result = hello().await;

// Future 只有被 poll 时才会执行
let future = hello();       // 尚未执行
let result = future.await;  // 开始执行
```

---

## 异步 vs 同步 | 单线程 vs 多线程

| 运行时 | 线程模型 | 适用场景 |
|--------|---------|---------|
| tokio（多线程） | 多工作线程 | 网络服务、高并发 |
| tokio（单线程） | 单线程 | 轻量级、避免同步开销 |
| async-std | 多线程 | 类 std API |
| smol | 多线程 | 轻量级运行时 |

---

## 适用范围

- **网络 IO**：HTTP 服务、数据库、消息队列 — 必须异步
- **CPU 密集**：使用 `spawn_blocking` 或独立线程
- **文件 IO**：tokio 的 `tokio::fs`
