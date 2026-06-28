# Kotlin 项目结构规范

## 标准项目布局

```
myproject/
├── src/
│   ├── main/
│   │   ├── kotlin/
│   │   │   └── com/example/
│   │   │       ├── domain/         # 领域实体、值对象
│   │   │       ├── application/    # 应用服务
│   │   │       ├── infrastructure/ # 基础设施
│   │   │       └── presentation/   # UI 层
│   │   └── resources/
│   ├── test/
│   │   └── kotlin/
│   │       └── com/example/
│   └── build.gradle.kts
├── build.gradle.kts
└── settings.gradle.kts
```

### 分层职责

```
com.example/
├── domain/            # 零框架依赖，纯 Kotlin
│   ├── model/         # 实体、值对象
│   ├── repository/    # 仓储接口
│   └── service/       # 领域服务
├── application/       # 用例编排，事务管理
│   └── usecase/
├── infrastructure/    # 外部依赖适配
│   ├── persistence/   # JPA/Room 实现
│   ├── client/        # HTTP 客户端
│   └── config/        # 配置
└── presentation/      # UI / API
    ├── controller/    # REST 控制器
    └── dto/           # 数据传输对象
```

---

## 目录职责

| 层 | 依赖 | 职责 |
|----|------|------|
| domain | 无 | 核心业务逻辑，纯 Kotlin |
| application | domain | 用例编排 |
| infrastructure | domain, application | 技术实现 |
| presentation | application | 用户接口 |

---

## 适用场景

- **Server**：Spring Boot / Ktor
- **Android**：按 feature 分包
- **Multiplatform**：共享 commonMain
