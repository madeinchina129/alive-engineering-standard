# Swift 项目结构规范

## 标准项目布局

```
MyProject/
├── Sources/
│   └── MyProject/
│       ├── App/              # App 入口、AppDelegate
│       ├── Domain/           # 实体、值对象、协议
│       ├── Data/             # 数据访问、Repository 实现
│       ├── Presentation/     # UI 层 (MVVM)
│       │   ├── Views/
│       │   └── ViewModels/
│       └── Infrastructure/   # 网络、数据库、外部服务
├── Resources/                # 资源文件
├── Tests/
│   ├── UnitTests/
│   └── UITests/
└── Package.swift             # SPM 配置
```

### MVVM 架构

```
Presentation/
├── Views/
│   ├── UserListView.swift
│   └── UserDetailView.swift
├── ViewModels/
│   ├── UserListViewModel.swift
│   └── UserDetailViewModel.swift
└── Coordinators/          # 可选：导航协调器
```

---

## 模块划分

| 层 | 职责 | 依赖 |
|----|------|------|
| App | AppDelegate、SceneDelegate | 所有层 |
| Domain | Entity、Protocol、UseCase | 无 |
| Data | RepositoryImpl、DataSource | Domain |
| Presentation | View、ViewModel | Domain |
| Infrastructure | Network、DB | 无 |

---

## 适用场景

- **iOS App**：UIKit / SwiftUI
- **SPM 库**：Sources/LibraryName 结构
- **多模块**：SPM 模块化
