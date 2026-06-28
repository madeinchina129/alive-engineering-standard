# Swift 项目结构 FAQ

## Q: struct 和 class 怎么选？

```
struct：值类型，不可变语义，安全，优先选择
class：引用类型，需要继承或共享状态时使用
```

```swift
struct User { let id: Int; let name: String }  // ✅ Model 用 struct
class UserViewModel { @Published var users: [User] = [] }  // ✅ 状态用 class
```

## Q: SwiftUI 和 UIKit 怎么选？

```
SwiftUI：iOS 16+，声明式 UI，开发效率高
UIKit：iOS 14-，成熟稳定，复杂交互
```

对于新项目，优先 SwiftUI，UIKit 用于兼容旧版本。

## Q: 依赖注入怎么做？

```swift
// 构造函数注入
class UserListViewModel {
    let repo: UserRepository
    init(repo: UserRepository) {
        self.repo = repo
    }
}

// 在 App 入口组装
let viewModel = UserListViewModel(repo: ApiUserRepository())
```

## Q: 多模块 SPM 怎么组织？

```
Sources/
├── MyApp/
├── MyDomain/
├── MyData/
└── MyPresentation/
Tests/
├── MyDomainTests/
└── MyDataTests/
Package.swift  # 多个 target
```
