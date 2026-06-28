# Go 项目结构细则

## 强制规则 (MUST)

### 1. `internal/` 限制外部导入

```go
// 目录结构
// myproject/internal/service/user_service.go
package service

// 外部项目导入会编译错误
// import "otherproject/internal/service"  // ❌ 编译错误
```

`internal/` 由 Go 编译器强制保护，外部包无法导入。

### 2. `cmd/` 每个子目录是一个 main package

```go
// cmd/server/main.go
package main

func main() {
    // 启动 HTTP 服务
}

// cmd/migrate/main.go  
package main

func main() {
    // 执行数据库迁移
}
```

### 3. `pkg/` 包设计为可复用

```go
// pkg/config/config.go - 公共配置库
package config

type Config struct {
    Host string
    Port int
}

func Load(path string) (*Config, error) {
    // 其他人可以复用
}
```

## 推荐实践 (SHOULD)

### 1. 依赖方向：cmd → handler → service → repository

```
cmd/server/main.go         # 入口
    → internal/handler/    # HTTP handler
        → internal/service/  # 业务逻辑
            → internal/repository/  # 数据访问
                → database
```

### 2. 包名反映目录角色

```go
// cmd/migrate/main.go → package main
// internal/handler/user.go → package handler
// internal/service/user.go → package service
// internal/repository/user.go → package repository
```

### 3. main.go 职责最小化

```go
// ✅ 正确：main.go 只做组装
func main() {
    config := config.Load()
    db := database.Connect(config.DSN)
    repo := repository.NewUserRepo(db)
    svc := service.NewUserService(repo)
    h := handler.NewUserHandler(svc)
    server := echo.New()
    h.Register(server)
    server.Start(config.Port)
}
```

## 禁止行为 (MUST NOT)

- ❌ `internal/` 中包被外部导入
- ❌ `cmd/` 中存放非 main package
- ❌ 循环依赖（`service` 依赖 `handler`）
- ❌ 包名和路径不一致
- ❌ `cmd/` 中存放业务逻辑（只放组装代码）
