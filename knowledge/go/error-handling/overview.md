# Go 错误处理规范

## Go 错误设计哲学

Go 没有异常（exception），错误是**值**（value），通过 `error` 接口返回和传递。

```go
type error interface {
    Error() string
}
```

### 错误作为值

```go
// ✅ 正确：函数返回 error，调用方决定如何处理
func ReadConfig(path string) ([]byte, error) {
    data, err := os.ReadFile(path)
    if err != nil {
        return nil, fmt.Errorf("读取配置失败 %s: %w", path, err)
    }
    return data, nil
}

// ❌ 错误：panic 处理可恢复错误
func ReadConfig(path string) []byte {
    data, err := os.ReadFile(path)
    if err != nil {
        panic(err)  // ❌ 不该 panic
    }
    return data
}
```

### 错误处理哲学

| 原则 | 说明 | 示例 |
|------|------|------|
| 显式处理 | 每个 error 必须被检查 | `if err != nil { return err }` |
| 尽早返回 | 出错立即返回，不继续执行 | 见上文 |
| 包装上下文 | 用 `%w` 附加信息 | `fmt.Errorf("xxx: %w", err)` |
| 只处理一次 | 要么处理，要么返回，不两者都做 | 不 logging + return |

---

## 错误处理策略

| 场景 | 方法 | 适用 |
|------|------|------|
| 简单传播 | 直接 `return err` | 不敏感操作 |
| 附加上下文 | `fmt.Errorf("context: %w", err)` | 所有生产代码 |
| 特定错误判断 | `errors.Is` / `errors.As` | 需要区分错误类型 |
| 哨兵错误 | `var ErrNotFound = errors.New("not found")` | 调用方需要判断 |
| 自定义类型 | 实现 `Error()` 的结构体 | 携带额外信息 |

---

## 适用范围

- **强制使用**：所有 Go 代码
- **禁止使用 panic 处理可恢复错误**
