# Go 测试 FAQ

## Q: 表驱动测试的命名惯例？

```go
tests := []struct {
    name string  // 测试用例名称
    args Args    // 输入
    want Want    // 期望输出
    err  bool    // 是否期望错误
}
```

`t.Run(tt.name, ...)` 实现子测试，`go test -run TestFunc/case_name` 可单独运行。

## Q: `t.Error` 和 `t.Fatal` 的区别？

```
t.Error → 标记失败但继续执行当前测试
t.Fatal → 标记失败并立即终止当前测试
```

setup 失败用 Fatal，断言失败用 Error。

## Q: 如何测试 HTTP handler？

```go
func TestHandler(t *testing.T) {
    req := httptest.NewRequest("GET", "/api/users", nil)
    w := httptest.NewRecorder()
    
    handler(w, req)
    
    resp := w.Result()
    body, _ := io.ReadAll(resp.Body)
    assert.Equal(t, 200, resp.StatusCode)
    assert.Contains(t, string(body), "users")
}
```

## Q: 覆盖率怎么计算和设置阈值？

```sh
go test -coverprofile=coverage.out ./...
go tool cover -html=coverage.out -o coverage.html
go tool cover -func=coverage.out
```

## Q: `go-cmp` 和 `reflect.DeepEqual` 哪个好？

`go-cmp` 提供更好的错误信息（diff 格式），支持自定义 comparer。`reflect.DeepEqual` 不显示具体差异。
