# Swift 项目结构 Checklist

## 分层架构
- [ ] ViewModel 是否使用 @Observable / ObservableObject？
- [ ] 协议是否在 Domain 层定义？
- [ ] 实现是否在 Data/Infrastructure 层？
- [ ] 是否避免 ViewController 包含业务逻辑？

## 类型选择
- [ ] Model 是否用 struct 而非 class？
- [ ] 状态管理是否用 class（@Observable）？
- [ ] 是否避免 force unwrap（!）？
- [ ] 常量是否用 enum 管理？

## 依赖注入
- [ ] 是否使用构造函数注入？
- [ ] 是否避免全局单例？
- [ ] ViewModel 是否可测试（可注入 mock）？
