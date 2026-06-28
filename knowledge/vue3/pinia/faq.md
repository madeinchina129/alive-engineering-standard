# Pinia FAQ

## Q: Pinia 和 Vuex 的核心区别是什么？

A: 核心区别：
1. **无 mutations**：直接修改 state
2. **完整 TypeScript**：自动推断类型
3. **Setup Store**：支持 Composition API 语法
4. **模块化**：每个 store 独立，无需嵌套 module
5. **代码拆分**：按需加载，Tree-shaking 友好

## Q: Setup Store 和 Options Store 如何选择？

A: 推荐 Setup Store（Composition API 语法）：
- 更好的 TypeScript 支持
- 更灵活（可以使用 watch/computed 等）
- 与 `<script setup>` 风格一致

Options Store 适合 Vuex 迁移场景。

## Q: storeToRefs 的作用是什么？

```typescript
// 直接解构会丢失响应性
const { user, isLoggedIn } = useUserStore()  // ❌ 失去响应性

// storeToRefs 保持响应性
const { user, isLoggedIn } = storeToRefs(useUserStore())  // ✅ 保持响应性
```

原理：`storeToRefs` 将 store 中的 ref/reactive/computed 提取为独立的响应式引用，而非直接解构 proxy。

## Q: Pinia 如何持久化状态？

```typescript
// 方案 1：手动 $subscribe
const store = useUserStore()
store.$subscribe((_, state) => {
  localStorage.setItem('user', JSON.stringify(state))
})

// 方案 2：pinia-plugin-persistedstate
export const useUserStore = defineStore('user', () => {
  // ...
}, {
  persist: true,  // 自动持久化
})
```

## Q: 在组件外如何使用 Pinia Store？

```typescript
// router 守卫中使用
router.beforeEach((to) => {
  const userStore = useUserStore()  // ✅ pinia 已注册后可全局使用
  if (to.meta.requiresAuth && !userStore.isLoggedIn) {
    return '/login'
  }
})
```

## Q: Pinia DevTools 支持如何？

A: Pinia 内置 DevTools 支持：
- 时间旅行调试
- 状态快照
- Action 追踪
- Vuex 迁移时保持 DevTools 兼容
