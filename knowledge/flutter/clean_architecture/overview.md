# Clean Architecture 分层方案

## 为什么选择 Clean Architecture

### 三层架构

```
lib/
├── domain/           # 企业业务规则（纯 Dart，无框架依赖）
│   ├── models/       # 领域实体
│   ├── repositories/ # 仓库接口（抽象）
│   ├── usecases/     # 用例（业务逻辑编排）
│   └── enums/        # 领域枚举
├── data/             # 数据层实现
│   ├── datasources/  # 数据源（API、本地数据库）
│   ├── repositories/ # 仓库实现
│   └── models/       # DTO / 请求/响应模型
└── presentation/     # 表示层
    ├── providers/    # Riverpod Notifier
    ├── pages/        # 页面组件
    └── widgets/      # 可复用 Widget
```

### 依赖规则

```
presentation → domain ← data
                  ↑
              （依赖倒置）
```

- Domain 层不依赖任何外部框架
- Data 层实现 Domain 层定义的接口
- Presentation 层依赖 Domain 层

### 用例 (Use Case) 驱动

```dart
class GetUserProfile implements UseCase<UserProfile, int> {
  final UserRepository repository;
  
  GetUserProfile(this.repository);
  
  @override
  Future<Either<Failure, UserProfile>> call(int userId) {
    return repository.getProfile(userId);
  }
}
```

---

## 对比其他架构

| 维度 | Clean Architecture | MVC | 简单分层 |
|------|-------------------|-----|---------|
| 层数 | 3（domain/data/presentation） | 3（model/view/controller） | 2（ui/data） |
| 依赖方向 | domain 最内层 | 双向 | 单向 |
| 可测试性 | 最高（domain 纯 Dart） | 中 | 低 |
| 学习成本 | 高 | 低 | 最低 |
| 适用项目 | 中大型 | 小中型 | 原型/MVP |

---

## 适用范围

- **强制使用**：所有中大型 Flutter 项目
- **推荐**：MVP 阶段使用简化版，逐步演进
- **flexible**：Domain 层是必须的，Data/Presentation 可简化

## 与项目其他部分的集成

- **Riverpod**：Presentation 层通过 Provider 连接 UseCase 和 UI
- **Freezed**：Data 层的 DTO 和 Domain 层 Entity 使用 Freezed
- **Dio**：Data 层的远程数据源使用 Dio
- **GoRouter**：Presentation 层的路由配置
