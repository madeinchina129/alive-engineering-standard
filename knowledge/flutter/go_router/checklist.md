# GoRouter Code Review Checklist

## 路由定义
- [ ] 所有路由是否集中在单一文件中管理？
- [ ] 路径是否使用 kebab-case？
- [ ] 参数是否使用 `:paramName` 格式？
- [ ] 是否使用 `name` 字段定义路由名称？
- [ ] 常量路径是否优先于动态路径？
- [ ] 嵌套层级是否超过 5 层？

## ShellRoute 使用
- [ ] 持久布局是否使用 ShellRoute 实现？
- [ ] Tab 导航是否使用 StatefulShellRoute？
- [ ] ShellRoute 的 child 参数是否正确使用？

## 导航安全
- [ ] redirect 是否轻量且无副作用？
- [ ] redirect 中是否没有异步操作？
- [ ] redirect 中是否没有修改 Provider 状态？
- [ ] initState 中是否没有执行导航？
- [ ] build 方法中是否没有直接调用 context.go？

## 页面参数
- [ ] 页面组件是否通过构造函数接收参数？（而非从 GoRouterState 读取）
- [ ] 复杂对象是否使用 extra 或 Provider 传递？
- [ ] 路由参数是否有类型安全？

## 错误处理
- [ ] 是否提供了 errorBuilder 处理 404？
- [ ] 是否处理了 pathParameters 为 null 的情况？

## 性能
- [ ] 路由配置是否懒加载？（使用 `builder` 而非 `pageBuilder` 时注意）
- [ ] 是否避免了过深的嵌套路由？
