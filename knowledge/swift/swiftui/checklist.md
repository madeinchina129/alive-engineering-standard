# SwiftUI Checklist

## View 定义
- [ ] View 是否是 `struct`（非 class）？
- [ ] body 是否保持简洁（< 50 行）？
- [ ] 重复 UI 是否抽取为子组件？
- [ ] 是否提供了 `#Preview`？

## 数据流
- [ ] 是否使用 `@Observable`（iOS 17+）管理状态？
- [ ] 属性包装器使用是否正确（@State / @Binding / @Environment）？
- [ ] 数据是否单向流动？
- [ ] 是否在 body 中执行网络请求？（❌ 禁止）

## 布局
- [ ] 是否使用 VStack/HStack/ZStack 合理布局？
- [ ] 列表是否使用 `LazyVStack` / `List`？
- [ ] 是否提供了 Identifiable 标识？
- [ ] 是否避免过多 GeometryReader？

## 导航
- [ ] 是否使用 NavigationStack？
- [ ] 是否使用 `.navigationDestination` 导航？
- [ ] 深层导航路径是否合理？

## 适配
- [ ] 是否适配深色模式？
- [ ] 是否适配不同动态字体大小？
- [ ] iPad/macOS 布局是否合理？
