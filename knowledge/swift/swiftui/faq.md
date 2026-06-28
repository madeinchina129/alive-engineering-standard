# SwiftUI FAQ

## Q: @State vs @StateObject vs @Observable？

iOS 17+ 推荐使用 `@Observable` 宏，替代 `@StateObject`：

```
iOS 17+ 方案：
  @Observable class → @State 创建，自动刷新视图

iOS 16 及以下：
  @State → 视图内部值类型
  @StateObject → 视图持有引用类型（生命周期绑定视图）
  @ObservedObject → 父视图传入的引用类型
```

## Q: SwiftUI 如何实现 MVVM？

SwiftUI 本身是 MVVM 友好架构：

```swift
// Model
struct User { let id: String; let name: String }

// ViewModel (@Observable)
@Observable class UserListViewModel {
    var users: [User] = []
    func load() async { /* 加载数据 */ }
}

// View
struct UserListView: View {
    @State private var viewModel = UserListViewModel()
    var body: some View {
        List(viewModel.users, id: \.id) { user in
            Text(user.name)
        }
        .task { await viewModel.load() }
    }
}
```

## Q: 列表性能优化怎么处理？

- 使用 `LazyVStack` / `List`（自动懒加载）
- `id: \.id` 提供唯一标识
- 避免在 `body` 中执行计算
- 使用 `@Observable` 避免不必要的刷新

## Q: 如何适配深色模式？

```swift
@Environment(\.colorScheme) var colorScheme

var body: some View {
    Text("Hello")
        .foregroundStyle(colorScheme == .dark ? .white : .black)
}
```

或在 Asset Catalog 中使用 Adaptive Color。

## Q: 如何在 SwiftUI 中使用 UIKit 组件？

```swift
struct ActivityIndicator: UIViewRepresentable {
    func makeUIView(context: Context) -> UIActivityIndicatorView {
        UIActivityIndicatorView(style: .medium)
    }
    func updateUIView(_ uiView: UIActivityIndicatorView, context: Context) {
        uiView.startAnimating()
    }
}
```
