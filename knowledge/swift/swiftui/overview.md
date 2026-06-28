# SwiftUI 界面开发规范

## SwiftUI 核心概念

SwiftUI 是 Apple 的声明式 UI 框架，iOS 13+：

```swift
struct ContentView: View {
    @State private var count = 0
    
    var body: some View {
        VStack(spacing: 16) {
            Text("计数: \(count)")
                .font(.title)
            
            Button("增加") {
                count += 1
            }
            .buttonStyle(.borderedProminent)
        }
        .padding()
    }
}
```

### 核心特性

```
SwiftUI
├── 声明式语法      # 描述 UI 状态，非命令式
├── @State          # 局部状态
├── @Binding        # 数据绑定
├── @Observable     # iOS 17+ 可观察对象
├── @Environment    # 环境值
├── Layout          # VStack/HStack/ZStack
├── NavigationStack # 导航
└── Previews        # Xcode 实时预览
```

---

## 数据流

```
数据流向：
数据层 → @Observable / @StateObject → View
用户操作 → Action → 更新数据 → 自动重绘
```

---

## 适用范围

- **iOS/iPadOS 应用**
- **macOS 应用**
- **watchOS 应用**
- **tvOS 应用**
