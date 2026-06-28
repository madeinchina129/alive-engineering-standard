# Composition API Code Review Checklist

## 组件结构
- [ ] 是否使用 `<script setup>` 语法？
- [ ] 逻辑是否按功能分组组织？
- [ ] 是否避免在 setup 中使用 `this`？
- [ ] 是否使用了 `defineProps`/`defineEmits` 类型注解？

## 响应式
- [ ] 简单类型是否使用 ref？
- [ ] 对象需要重新赋值时是否使用 ref 而非 reactive？
- [ ] computed 是否用于派生状态？
- [ ] 是否避免了在模板中使用复杂表达式？

## Composable
- [ ] composable 函数是否以 `use` 开头命名？
- [ ] composable 是否返回可使用解构的值？
- [ ] composable 是否处理了组件卸载后的清理？
- [ ] 是否提取了可复用的复杂逻辑？

## 副作用管理
- [ ] watch 是否指定了精确的监听源？
- [ ] 异步操作是否有组件卸载保护？
- [ ] watchEffect 是否追踪了正确的依赖？
- [ ] 定时器/事件监听是否在 onUnmounted 中清理？

## 类型安全
- [ ] 组件 Props 是否有类型定义？
- [ ] ref 是否显式标注了类型？（ref<T>）
- [ ] emit 事件是否有类型定义？
- [ ] 是否避免使用 any 类型？

## 性能
- [ ] 是否避免了不必要 watcher？
- [ ] 是否使用了 shallowRef 处理大型对象？
- [ ] 组件拆分是否合理？（避免过大组件）
