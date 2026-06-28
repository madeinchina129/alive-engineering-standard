# Go 项目结构 FAQ

## Q: `internal/` 目录的作用？

Go 编译器强制：`internal/` 中的包只能被同一模块树中的包导入。外部项目导入编译失败。用于放置不希望外部依赖的代码。

## Q: 没有 HTTP handler 的项目怎么分类？

服务端项目用 handler，CLI 工具用 command：

```
# CLI 项目结构
cmd/
├── app/main.go
└── admin/main.go
internal/
├── command/       # CLI 命令处理
├── service/       # 业务逻辑
└── repository/    # 数据访问
```

## Q: 什么时候用 `pkg/` 而不是 `internal/`？

- 设计为可复用库 → `pkg/`
- 仅内部使用的实现细节 → `internal/`
- 不确定 → `internal/`（后续改为 `pkg/` 更安全，反之则破坏 API）

## Q: 小型项目也按这个结构吗？

小项目可以简化：

```
myproject/
├── main.go
├── handler.go
├── store.go
├── go.mod
```

当达到 3-5 个文件时再按标准布局拆分。

## Q: monorepo 怎么组织多个服务？

```
cmd/
├── user-service/main.go
├── order-service/main.go
└── notify-service/main.go
internal/
├── user/             # user-service 内部逻辑
│   ├── handler/
│   └── service/
├── order/
│   ├── handler/
│   └── service/
└── notify/
    ├── handler/
    └── service/
pkg/
├── config/           # 公共配置
└── middleware/        # 公共中间件
```

## Q: domain-driven design 如何结合？

```
internal/
├── domain/           # 核心实体、值对象、聚合根
│   ├── user/
│   └── order/
├── application/      # 应用服务（用例编排）
├── infrastructure/   # 基础设施（数据库、消息队列）
└── interfaces/       # 接口适配层（handler、dto）
```
