# SwiftUI 细则

## 强制规则 (MUST)

### 1. 使用 @Observable（iOS 17+）管理数据

```swift
// ✅ 正确：@Observable 宏
@Observable
class UserViewModel {
    var name = ""
    var age = 0
    
    func loadUser() { /* 加载逻辑 */ }
}

struct UserView: View {
    @State private var viewModel = UserViewModel()
    var body: some View {
        Text(viewModel.name)
    }
}

// ❌ 错误：手动 ObservableObject
class UserViewModel: ObservableObject {
    @Published var name = ""  // ❌ 手动 @Published
}
```

### 2. 合理使用属性包装器

```swift
// ✅ 正确：根据作用域选择
@State private var isPresented = false      // 局部值类型
@State private var text = ""                 // 表单输入
@Binding var isVisible: Bool                 // 子视图接收父视图状态
@Environment(\.colorScheme) var colorScheme  // 环境值

// ❌ 错误：滥用 @State 传递
struct ChildView: View {
    @State var data: [String]  // ❌ @State 传递应使用 @Binding
}
```

### 3. 布局优先使用容器

```swift
// ✅ 正确：按需选择
VStack(alignment: .leading, spacing: 8) { /* 垂直排列 */ }
HStack { /* 水平排列 */ }
ZStack(alignment: .bottomTrailing) { /* 层叠 */ }
LazyVStack { /* 可滚动列表 */ }
LazyHGrid(rows: gridItems) { /* 网格 */ }

// ❌ 错误：嵌套过多 GeometryReader
GeometryReader { geo in
    VStack {
        Text("宽度: \(geo.size.width)")
    }
}
```

### 4. NavigationStack 导航

```swift
// ✅ 正确：NavigationStack + .navigationDestination
NavigationStack {
    List(users) { user in
        NavigationLink(user.name, value: user)
    }
    .navigationDestination(for: User.self) { user in
        UserDetailView(user: user)
    }
}

// ❌ 错误：NavigationLink 直接导航
NavigationLink(destination: UserDetailView(user: user)) {
    Text(user.name)
}
```

### 5. 提供 Preview

```swift
// ✅ 正确：所有视图提供 Preview
#Preview {
    ContentView()
}

// ✅ 正确：复杂 preview 带 mock 数据
#Preview {
    UserDetailView(user: User.sample)
        .environment(\.colorScheme, .dark)
}
```

## 推荐实践 (SHOULD)

### 组件化

```swift
struct UserRow: View {
    let user: User
    
    var body: some View {
        HStack {
            AvatarView(url: user.avatarUrl)
            VStack(alignment: .leading) {
                Text(user.name).font(.headline)
                Text(user.email).font(.caption).foregroundStyle(.secondary)
            }
        }
    }
}
```

## 禁止行为 (MUST NOT)

- ❌ 在 body 中执行网络请求
- ❌ 使用 UIKit 代码替代 SwiftUI 原生组件（除非必要）
- ❌ View 中使用 class（struct 即可）
- ❌ 忽略 Previews
