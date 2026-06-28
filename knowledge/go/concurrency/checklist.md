# Go 并发 Checklist

## goroutine 管理
- [ ] 每个 goroutine 是否有明确的退出条件？
- [ ] 是否使用 `sync.WaitGroup` 等待完成？
- [ ] 是否避免 goroutine 泄漏？
- [ ] 是否使用 `go run -race` 检测竞争？

## channel 使用
- [ ] 由发送方负责关闭 channel？
- [ ] 是否避免向已关闭的 channel 发送？
- [ ] 缓冲 channel 的大小是否合理？
- [ ] 是否使用 `for range` 遍历 channel？

## Context 使用
- [ ] 发起网络/IO 请求时是否传递 Context？
- [ ] 耗时操作是否设置了超时？
- [ ] goroutine 是否监听 `ctx.Done()`？
- [ ] defer cancel() 是否调用？

## 同步原语
- [ ] 共享变量是否用 Mutex/RWMutex 保护？
- [ ] 读多写少是否使用 RWMutex？
- [ ] 是否避免死锁（锁顺序一致）？
- [ ] 是否避免了 `time.Sleep` 等待 goroutine？

## select
- [ ] 多 channel 等待是否使用 select？
- [ ] 是否有 default 分支防止阻塞？
- [ ] 是否有超时控制？
- [ ] 是否避免空 select{}？

## 工具
- [ ] 测试是否启用 `-race`？
- [ ] `go vet` 是否有并发相关警告？
