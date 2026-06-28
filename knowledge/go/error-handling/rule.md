# Go 错误处理细则

## 强制规则 (MUST)

### 1. 每个 error 必须被检查

```go
// ✅ 正确：每个返回的 error 都被处理
f, err := os.Open(path)
if err != nil {
    return fmt.Errorf("无法打开文件: %w", err)
}
defer f.Close()

// ❌ 错误：忽略 error
f, _ := os.Open(path)   // ❌ 丢弃 error
```

### 2. 使用 `%w` 包装错误上下文

```go
// ✅ 正确：%w 创建错误链
func GetUser(id int) (*User, error) {
    user, err := db.FindByID(id)
    if err != nil {
        return nil, fmt.Errorf("获取用户 %d 失败: %w", id, err)
    }
    return user, nil
}

// ❌ 错误：丢失原始错误
return fmt.Errorf("获取用户失败: %v", err)  // ❌ %v 不包装
```

### 3. 判断错误用 `errors.Is` / `errors.As`

```go
// ✅ 正确：errors.Is 遍历错误链
if errors.Is(err, os.ErrNotExist) {
    return handleNotFound()
}

// ✅ 正确：errors.As 提取自定义错误
var cfgErr *ConfigError
if errors.As(err, &cfgErr) {
    log.Printf("配置错误: 字段 %s 值 %s", cfgErr.Field, cfgErr.Value)
}

// ❌ 错误：直接比较（破坏错误链）
if err == os.ErrNotExist {}  // ❌ 如果被包装过，不相等
```

### 4. 自定义错误类型实现 Error()

```go
// ✅ 正确：自定义错误带额外信息
type ValidationError struct {
    Field string
    Value any
    Msg   string
}

func (e *ValidationError) Error() string {
    return fmt.Sprintf("校验失败: 字段 %s 值 %v — %s", e.Field, e.Value, e.Msg)
}

func (e *ValidationError) Unwrap() error {
    return nil
}
```

### 5. 哨兵错误用于调用方判断

```go
// ✅ 正确：哨兵错误
var ErrNotFound = errors.New("资源不存在")

func GetUser(id int) (*User, error) {
    user, err := db.FindByID(id)
    if errors.Is(err, sql.ErrNoRows) {
        return nil, fmt.Errorf("%w: user_id=%d", ErrNotFound, id)
    }
    return user, nil
}

// 调用方
if errors.Is(err, ErrNotFound) {
    return c.Status(404).JSON(errorResponse(err))
}
```

## 推荐实践 (SHOULD)

### 只处理一次

```go
// ✅ 正确：要么处理（log），要么返回
if err != nil {
    return fmt.Errorf("read: %w", err)  // 只返回，不 log
}

// ❌ 错误：同时 log 和 return（日志重复）
if err != nil {
    log.Printf("error: %v", err)
    return fmt.Errorf("read: %w", err)
}
```

## 禁止行为 (MUST NOT)

- ❌ 用 panic 处理可恢复错误
- ❌ 忽略 error（`_` 丢弃）
- ❌ 同时 log 和 return 同一个 error
- ❌ 使用 `%v` 或 `%s` 包装 error（应使用 `%w`）
- ❌ 直接比较可能被包装过的 error
