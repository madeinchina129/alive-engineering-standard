# Go 并发 FAQ

## Q: channel 应该用缓冲还是非缓冲？

```go
// 非缓冲：发送和接收同时准备好，同步（作为同步原语）
syncCh := make(chan struct{})

// 缓冲：有缓冲区，解耦发送和接收
jobCh := make(chan Job, 100)

// 缓冲大小设置经验：根据生产速度和消费速度的差值估算
// 生产 > 消费 → 大缓冲，但要注意 OOM
// 生产 ≈ 消费 → 小缓冲即可
```

```go
// 非缓冲 channel 作为信号量
done := make(chan struct{})
go func() {
    work()
    close(done)  // 关闭时通知
}()
<-done  // 等待完成
```

## Q: `sync.Mutex` 和 `sync.RWMutex` 怎么选？

```go
// Mutex：读写都用锁（适合写多读少）
var mu sync.Mutex
mu.Lock()
counter++
mu.Unlock()

// RWMutex：读操作不互斥（适合读多写少）
var rw sync.RWMutex
rw.RLock()     // 多个读可并行
count := cache[key]
rw.RUnlock()

rw.Lock()      // 写时排他
cache[key] = value
rw.Unlock()
```

## Q: goroutine 泄漏怎么预防？

```go
// ✅ 确保 goroutine 能退出
func process(ctx context.Context, ch <-chan int) {
    for {
        select {
        case v := <-ch:
            handle(v)
        case <-ctx.Done():
            return  // 退出 goroutine
        }
    }
}

// ❌ 泄漏：没有退出机制
func process(ch <-chan int) {
    for v := range ch {
        handle(v)  // 如果 ch 永远不会关闭，goroutine 泄漏
    }
}
```

## Q: `select` 的超时用法？

```go
select {
case result := <-ch:
    fmt.Println(result)
case <-time.After(5 * time.Second):
    fmt.Println("超时")
}
```

## Q: 如何限制并发数？

```go
// 使用 buffered channel 作为信号量
sem := make(chan struct{}, 10)  // 最多 10 个并发

for _, task := range tasks {
    sem <- struct{}{}  // 满时阻塞
    go func(t Task) {
        defer func() { <-sem }()
        t.Process()
    }(task)
}
```
