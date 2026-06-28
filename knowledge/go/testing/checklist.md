# Go 测试 Checklist

## 测试函数
- [ ] 文件名是否以 `_test.go` 结尾？
- [ ] 测试函数签名是否 `func TestXxx(t *testing.T)`？
- [ ] 是否使用表驱动测试覆盖多场景？
- [ ] 子测试是否使用 `t.Run()`？

## 断言
- [ ] 是否使用 `t.Error` / `t.Fatal` 而非 log？
- [ ] 复杂结构是否使用 go-cmp？
- [ ] 辅助函数是否调用了 `t.Helper()`？
- [ ] 错误消息是否包含实际值和期望值？

## Mock
- [ ] mock 是否使用 testify/mock？
- [ ] mock 期望是否在 TestMain 或 setup 中设置？
- [ ] `mock.AssertExpectations` 是否调用？

## 测试覆盖
- [ ] 核心逻辑覆盖率是否 > 80%？
- [ ] 是否运行 `go test -race`？
- [ ] 边界情况（空值、零值、错误）是否测试？

## 隔离
- [ ] 测试是否不依赖外部服务？
- [ ] 测试是否独立可重复执行？
- [ ] 测试数据是否在 setup 中创建，teardown 中清理？
