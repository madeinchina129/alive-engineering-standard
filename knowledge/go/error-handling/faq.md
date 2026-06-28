# Go 错误处理 FAQ

## Q: `%w` 和 `%v` 的区别？

```
%w：包装错误，保留错误链（errors.Is/As 可遍历）
%v：格式化字符串，不保留错误链
```

```go
// %w：调用方可以 errors.Is(err, os.ErrNotExist)
return fmt.Errorf("read: %w", err)

// %v：调用方不能 errors.Is，只能看字符串
return fmt.Errorf("read: %v", err)
```

## Q: `errors.Is` 和 `errors.As` 的区别？

```
errors.Is：判断错误链中是否包含目标错误（值比较）
errors.As：提取错误链中匹配类型的错误（类型断言）
```

```go
// Is：检查是否存在特定 sentinel error
if errors.Is(err, ErrNotFound) {}

// As：提取自定义错误类型的实例
var valErr *ValidationError
if errors.As(err, &valErr) {
    fmt.Println(valErr.Field)  // 访问额外字段
}
```

## Q: log 错误应该在哪个层做？

```go
// 业务层：返回包装后的错误（不 log）
func (s *UserService) GetUser(id int) (*User, error) {
    user, err := s.repo.FindByID(id)
    if err != nil {
        return nil, fmt.Errorf("get user %d: %w", id, err)
    }
    return user, nil
}

// HTTP 层：log 错误并返回用户友好的响应
func (h *UserHandler) GetUser(w http.ResponseWriter, r *http.Request) {
    user, err := h.svc.GetUser(id)
    if err != nil {
        log.Printf("获取用户失败: %v", err)  // 只在这里 log
        http.Error(w, "内部错误", 500)
        return
    }
}
```

## Q: 什么时候用 panic/recover？

只在程序无法继续运行的情况下使用：
- 配置加载失败（启动时就应失败）
- 端口被占用
- 不可能发生的分支（`switch` 的 default）

## Q: 自定义错误要实现 Unwrap() 吗？

```go
// 如果要让 errors.Is/As 能遍历到包装链，实现 Unwrap
func (e *MyError) Unwrap() error {
    return e.Err  // 返回被包装的原始错误
}

// 如果没有包装其他错误，返回 nil
func (e *ValidationError) Unwrap() error {
    return nil
}
```
