# Swift 项目结构细则

## 强制规则 (MUST)

### 1. ViewModel 使用 @Observable / ObservableObject

```swift
// ✅ 正确：SwiftUI + @Observable
@Observable
class UserListViewModel {
    var users: [User] = []
    var isLoading = false
    
    func loadUsers() async {
        isLoading = true
        users = try! await api.getUsers()
        isLoading = false
    }
}

// ❌ 错误：ViewController 包含网络请求逻辑
class UserViewController: UIViewController {
    override func viewDidLoad() {
        super.viewDidLoad()
        URLSession.shared.dataTask(with: url) { data, _, _ in
            // ❌ ViewController 直接处理网络逻辑
        }
    }
}
```

### 2. 使用协议隔离依赖

```swift
// ✅ 正确：Domain 定义协议
protocol UserRepository {
    func fetchUsers() async throws -> [User]
}

// Infrastructure 实现
struct ApiUserRepository: UserRepository {
    func fetchUsers() async throws -> [User] {
        let data = try await URLSession.shared.data(from: url).0
        return try JSONDecoder().decode([User].self, from: data)
    }
}

// ❌ 错误：直接依赖具体实现
class UserListViewModel {
    let repo = ApiUserRepository()  // ❌ 无法替换为 mock
}
```

### 3. 值类型优先于引用类型

```swift
// ✅ 正确：Model 用 struct
struct User: Codable, Identifiable {
    let id: Int
    let name: String
}

// ❌ 错误：Model 用 class（不必要的引用语义）
class User {
    let id: Int
    let name: String
    init(id: Int, name: String) { self.id = id; self.name = name }
}
```

## 推荐实践 (SHOULD)

### 使用 enum 管理常量

```swift
enum API {
    static let baseURL = "https://api.example.com"
    enum Path {
        static let users = "/users"
    }
}
```

## 禁止行为 (MUST NOT)

- ❌ ViewController 包含业务逻辑
- ❌ 使用 `!` implicitly unwrapped optional 作为实例变量
- ❌ 全局可变状态
- ❌ 不使用依赖注入
