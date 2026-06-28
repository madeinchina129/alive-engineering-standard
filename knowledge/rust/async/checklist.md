# Rust 异步 Checklist

## async/.await 基础
- [ ] 所有 Future 是否已被 `.await`？
- [ ] 是否避免丢弃未 .await 的 Future？
- [ ] 是否在 async fn 中使用了正确的运行时？
- [ ] 是否避免在 async 上下文使用阻塞 API？

## tokio 运行时
- [ ] 运行时 flavor 选择是否正确（多线程/单线程）？
- [ ] 阻塞任务是否使用 `spawn_blocking`？
- [ ] 异步锁是否使用 `tokio::sync::Mutex`？
- [ ] 是否避免 `std::sync::MutexGuard` 跨 .await？

## 并发控制
- [ ] 并行任务是否使用 `join!` / `try_join!`？
- [ ] 动态任务是否使用 `JoinSet`？
- [ ] 是否设置了操作超时？
- [ ] 是否避免了无限制的并发任务？

## 资源共享
- [ ] 共享状态是否使用 `Arc` 包装？
- [ ] async 上下文是否使用 `tokio::sync` 而非 `std::sync`？
- [ ] 是否使用了 CancellationToken 管理取消？
- [ ] 是否避免了在 async 函数中持有锁跨 .await？

## 错误处理
- [ ] 异步操作的错误是否被处理？
- [ ] JoinError 是否被正确处理？
- [ ] 超时错误是否被区分处理？
