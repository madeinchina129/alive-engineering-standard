# Go 并发编程细则

## 强制规则 (MUST)

### 1. 通过 channel 通信，而非共享内存

```go
// ✅ 正确：channel 传递结果
func worker(id int, results chan<- string) {
    results <- fmt.Sprintf("Worker %d 完成", id)
}

// ❌ 错误：用共享变量传递结果
var results []string
var mu sync.Mutex
go func() {
    mu.Lock()
    results = append(results, "完成")  // ❌ 共享可变状态
    mu.Unlock()
}()
```

### 2. 使用 Context 传播取消和超时

```go
// ✅ 正确：Context 控制超时
func queryDB(ctx context.Context) (Result, error) {
    ctx, cancel := context.WithTimeout(ctx, 3*time.Second)
    defer cancel()

    result, err := db.QueryContext(ctx, "SELECT ...")
    if errors.Is(err, context.DeadlineExceeded) {
        return nil, fmt.Errorf("数据库超时")
    }
    return result, err
}

// ❌ 错误：没有超时控制
func queryDB() (Result, error) {
    return db.Query("SELECT ...")  // ❌ 可能永远阻塞
}
```

### 3. 使用 WaitGroup 等待 goroutine 完成

```go
// ✅ 正确：WaitGroup 管理生命周期
func processBatch(items []Item) {
    var wg sync.WaitGroup
    for _, item := range items {
        wg.Add(1)
        go func(it Item) {
            defer wg.Done()
            process(it)
        }(item)
    }
    wg.Wait()
}

// ❌ 错误：不等待 goroutine
for _, item := range items {
    go process(item)
}
// main 函数可能先退出，goroutine 未执行
```

### 4. 关闭 channel 由发送方负责

```go
// ✅ 正确：发送方关闭 channel
func produce(ctx context.Context, items []int) <-chan int {
    out := make(chan int)
    go func() {
        defer close(out)
        for _, item := range items {
            select {
            case out <- item:
            case <-ctx.Done():
                return
            }
        }
    }()
    return out
}

// ❌ 错误：接收方关闭 channel
func consume(ch <-chan int) {
    close(ch)  // ❌ panic: close of receive-only channel
}
```

### 5. 所有并发代码启用 race detector

```go
// ✅ 正确：通过 -race 检测数据竞争
// $ go test -race ./...
// $ go build -race ./cmd/server
```

## 推荐实践 (SHOULD)

### Worker Pool 模式

```go
func workerPool(numWorkers int, jobs <-chan Job) {
    var wg sync.WaitGroup
    for i := 0; i < numWorkers; i++ {
        wg.Add(1)
        go func() {
            defer wg.Done()
            for job := range jobs {
                job.Execute()
            }
        }()
    }
    wg.Wait()
}
```

## 禁止行为 (MUST NOT)

- ❌ 不启动 goroutine 后不管理生命周期
- ❌ 向已关闭的 channel 发送数据
- ❌ 关闭 channel 时不确保发送方已结束
- ❌ 不加锁访问共享变量（race condition）
- ❌ 使用 `time.Sleep` 等待 goroutine 完成
