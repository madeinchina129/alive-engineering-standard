# Go 项目结构 Checklist

## 模块结构
- [ ] 是否遵循 `cmd/internal/pkg` 布局？
- [ ] `cmd/` 下每个目录是否是一个 main package？
- [ ] `internal/` 下是否有业务逻辑分层（handler/service/repository）？
- [ ] `pkg/` 是否只放置可复用代码？

## 强制规则
- [ ] `internal/` 是否没有被外部导入？
- [ ] `cmd/` 是否只做依赖组装，不含业务逻辑？
- [ ] main.go 是否简洁（只做组合）？
- [ ] 包名是否和目录名一致？
- [ ] 是否避免循环依赖？

## 推荐实践
- [ ] 依赖方向是否正确：cmd → handler → service → repository？
- [ ] main.go 是否启动所有依赖？
- [ ] 是否使用 `go mod tidy` 清理依赖？
- [ ] 是否有 Makefile 或 Taskfile 统一命令？

## 工具检查
- [ ] `go vet ./...` 是否通过？
- [ ] `go mod tidy` 是否正常？
- [ ] 是否有 Describe/Context/Success/Hook 风格的测试？
- [ ] 测试是否放在 `_test.go` 文件中？
