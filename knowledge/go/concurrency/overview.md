# Go 并发编程规范

## Go 并发模型

Go 使用 **CSP（Communicating Sequential Processes）** 模型，通过 **goroutine** 和 **channel** 实现并发：

```go
// goroutine：轻量级线程
go func() {
    fmt.Println("并发执行")
}()

// channel：goroutine 之间通信
ch := make(chan int)
go func() { ch <- 42 }()
value := <-ch
```

### 核心原则

> **Do not communicate by sharing memory; instead, share memory by communicating.**

```go
// ✅ 正确：通过 channel 传递数据
func worker(jobs <-chan int, results chan<- int) {
    for job := range jobs {
        results <- process(job)
    }
}

// ❌ 错误：通过共享变量通信（需要锁）
var counter int
var mu sync.Mutex

go func() {
    mu.Lock()
    counter++
    mu.Unlock()
}()
```

---

## 并发原语对比

| 原语 | 用途 | 适用场景 |
|------|------|---------|
| `go` | 启动 goroutine | 任何并发任务 |
| `chan T` | goroutine 通信 | 数据流、结果传递 |
| `sync.WaitGroup` | 等待一组 goroutine | fan-out 模式 |
| `sync.Mutex` | 互斥锁 | 保护共享资源 |
| `sync.RWMutex` | 读写锁 | 读多写少场景 |
| `context.Context` | 取消/超时传播 | HTTP 请求、数据库操作 |
| `select` | 多 channel 等待 | 超时控制、多路复用 |

---

## 适用范围

- **强制使用**：所有需要使用并发的 Go 代码
- **工具**：`go vet`、`go race`（数据竞争检测）
