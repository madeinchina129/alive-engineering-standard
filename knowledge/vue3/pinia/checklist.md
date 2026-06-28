# Pinia Code Review Checklist

## Store 定义
- [ ] 是否使用 Setup Store（Composition API）语法？
- [ ] Store 命名是否遵循 `useXxxStore` 格式？
- [ ] 文件是否按领域分离？（一个 store 一个文件）
- [ ] 是否只有全局状态使用 Pinia？（局部状态使用 composable）

## State
- [ ] state 是否使用 ref/reactive 定义？
- [ ] 是否避免在 state 中存储组件实例或 DOM？
- [ ] 是否使用了 storeToRefs 保持响应性？
- [ ] 是否避免了直接解构 store？

## Getters
- [ ] 派生状态是否使用 computed 定义？
- [ ] getter 中是否没有副作用？
- [ ] 是否避免在组件中重复计算派生状态？

## Actions
- [ ] 异步操作是否在 action 中处理？
- [ ] 是否避免在 action 中修改其他 store 的状态？
- [ ] 是否使用了正确的错误处理？
- [ ] action 命名是否清晰？

## 组件使用
- [ ] 组件中是否使用 storeToRefs 解构 state 和 getters？
- [ ] actions 是否直接解构？（不需要 storeToRefs）
- [ ] 是否避免了在模板中调用 action？

## 性能
- [ ] Store 是否按需加载？（不是所有 store 在 app 启动时都实例化）
- [ ] 大型 store 是否拆分为多个小 store？
- [ ] 是否避免了不必要的大对象监听？
- [ ] $subscribe 回调是否轻量？
