# Go 项目结构规范

## 标准 Go 项目布局

Go 社区推荐遵循 [Standard Go Project Layout](https://github.com/golang-standards/project-layout)：

```
myproject/
├── cmd/              # 可执行入口
│   └── app/
│       └── main.go
├── internal/         # 私有包（项目内可用，外部不可导入）
│   ├── handler/
│   ├── service/
│   └── repository/
├── pkg/              # 可导出的公共包
│   ├── config/
│   └── middleware/
├── api/              # API 定义（proto、openapi）
├── configs/          # 配置文件
├── scripts/          # 构建脚本
├── test/             # 端到端测试
├── docs/             # 文档
├── go.mod
└── go.sum
```

---

## 目录职责

| 目录 | 职责 | 外部可见性 |
|------|------|-----------|
| `cmd/` | 应用程序入口，每个子目录对应一个 binary | ✅ |
| `internal/` | 业务逻辑，限制外部导入 | ❌ 编译器强制 |
| `pkg/` | 可复用库代码 | ✅ |
| `api/` | 协议定义 | ❌（引用） |

---

## 适用范围

- **推荐使用**：Go 项目布局参考此结构
- **小型项目**：可直接使用 `cmd/` + `internal/` 两层
- **微服务**：每个服务独立 repo 或 monorepo 中独立目录
