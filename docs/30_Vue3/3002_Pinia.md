---
id: vue3.pinia
priority: P1
owner: Frontend Team
version: 1.0
generated: 2026-06-28
---

# Pinia 状态管理规范

> **领域**: Vue3 开发规范 | **优先级**: P1 | **版本**: 1.0
> 
> Pinia 状态管理使用标准，Store 定义和使用规范


> **关联规范**: [Composition API 规范](../30_Vue3/3001_CompositionApi.md)


---




# Pinia 状态管理方案

## 为什么选择 Pinia

### 简洁的 Store 定义

```typescript
// stores/user.ts
import { defineStore } from 'pinia'

export const useUserStore = defineStore('user', () => {
  // state
  const user = ref<User | null>(null)
  const token = ref<string | null>(null)

  // getters
  const isLoggedIn = computed(() => !!token.value)
  const userName = computed(() => user.value?.name ?? '')

  // actions
  async function login(email: string, password: string) {
    const response = await api.post('/auth/login', { email, password })
    token.value = response.token
    user.value = response.user
  }

  function logout() {
    token.value = null
    user.value = null
  }

  return { user, token, isLoggedIn, userName, login, logout }
})
```

对比 Vuex 的 mutations/actions/getters 分离，Pinia 去掉了 mutations，API 更加简洁。

### TypeScript 完美支持

```typescript
// 自动推断类型
const store = useUserStore()
store.user        // User | null (自动推断)
store.isLoggedIn  // ComputedRef<boolean> (自动推断)
store.login(...)  // 参数类型自动推断
```

### 无 mutations

Pinia 直接修改 state，不再需要 Vuex 中冗余的 mutation：

```typescript
// Pinia: 直接修改
store.user = newUser

// Vuex: 需要 mutation
store.commit('SET_USER', newUser)
```

---

## 对比 Vuex

| 维度 | Vuex 4 | Pinia |
|------|--------|-------|
| 语法 | Options API | Options + Setup |
| TypeScript | 有限 | 完整 |
| Mutations | 需要 | 移除 |
| DevTools | 支持 | 支持 |
| 代码生成 | 无 | Nuxt 自动生成 |
| 模块化 | 嵌套 module | 独立 store |

---

## 适用范围

- **强制使用**：替代 Vuex，所有 Vue3 项目状态管理
- **全局状态**：用户信息、主题、语言
- **业务状态**：购物车、表单数据（如果跨组件共享）
- **局部状态**：推荐使用 composable 而非 Pinia





---

## 使用规范

# Pinia 状态管理规范

## Store 定义规范

### 使用 Setup Store 语法

```typescript
// ✅ 推荐：Setup Store（Composition API 风格）
export const useUserStore = defineStore('user', () => {
  const user = ref<User | null>(null)
  const isLoggedIn = computed(() => !!user.value)
  
  async function login(email: string, password: string) { /* ... */ }
  function logout() { /* ... */ }
  
  return { user, isLoggedIn, login, logout }
})

// ❌ 避免：Options Store（Options API 风格）
export const useUserStore = defineStore('user', {
  state: () => ({ user: null }),
  getters: { isLoggedIn: (state) => !!state.user },
  actions: { login(email, password) { /* ... */ } },
})
```

### 文件组织规范

```
stores/
├── index.ts           # 导出所有 store
├── user.ts            # 用户相关
├── cart.ts            # 购物车
├── theme.ts           # 主题配置
└── counter.ts         # 简单计数器（示例）
```

### Store 命名规范

```typescript
// use + 领域名 + Store
export const useUserStore = defineStore('user', ...)
export const useCartStore = defineStore('cart', ...)
export const useThemeStore = defineStore('theme', ...)
```

## 强制规则 (MUST)

### 1. 全局状态使用 Pinia，局部状态使用 composable

```typescript
// ✅ Pinia：跨组件/跨页面共享的状态
export const useUserStore = defineStore('user', () => {
  const token = ref(localStorage.getItem('token'))
  // ...
})

// ✅ Composable：组件内部或少量组件共享的逻辑
export function useCounter(initial = 0) {
  const count = ref(initial)
  const increment = () => count.value++
  return { count, increment }
}
```

### 2. Actions 包含异步逻辑

```typescript
// ✅ 正确：actions 处理异步操作
export const useUserStore = defineStore('user', () => {
  async function login(email: string, password: string) {
    const response = await api.post('/auth/login', { email, password })
    token.value = response.token
    user.value = response.user
  }
  
  return { login }
})
```

### 3. 避免直接修改 $state（使用 ref）

```typescript
// ✅ 正确
const count = ref(0)
function increment() { count.value++ }

// ❌ 避免
const count = ref(0)
function increment() { $state.count++ }  // 不直观
```

### 4. 组件中使用 store 保持响应性

```vue
<script setup lang="ts">
const userStore = useUserStore()

// ✅ 正确：store 解构后保持响应性
const { user, isLoggedIn } = storeToRefs(userStore)
const { login, logout } = userStore  // actions 可以直接解构

// ❌ 错误：ref 解构丢失响应性
const { user, isLoggedIn } = useUserStore()
</script>
```

### 5. Store 之间的相互引用

```typescript
// ✅ 正确：在 action 中引用其他 store
export const useOrderStore = defineStore('order', () => {
  async function placeOrder(items: Item[]) {
    const userStore = useUserStore()
    if (!userStore.isLoggedIn) {
      throw new Error('Please login first')
    }
    // ... 下单逻辑
  }
  
  return { placeOrder }
})
```

## 推荐实践 (SHOULD)

### 1. $reset 用于重置状态

```typescript
// 使用 Options Store 时自动支持 $reset
// Setup Store 需要手动实现
export const useCounterStore = defineStore('counter', () => {
  const count = ref(0)
  function reset() { count.value = 0 }
  return { count, reset }
})
```

### 2. 使用 $subscribe 监听状态变化

```typescript
const store = useUserStore()
store.$subscribe((mutation, state) => {
  localStorage.setItem('user-state', JSON.stringify(state))
})
```

### 3. 大型 Store 拆分

```typescript
// 超过 10 个 action 或 15 个 state 字段，考虑拆分
// bad: useUserStore (20 actions)
// good: useUserAuthStore + useUserProfileStore + useUserSettingsStore
```

## 禁止行为 (MUST NOT)

- ❌ 在 Store 中引用组件实例
- ❌ 在组件外部使用 store（需要在 setup 或 pinia 上下文）
- ❌ 在 Pinia 中存储组件引用或 DOM 元素
- ❌ 在 getter 中执行副作用
- ❌ 在 action 中修改非本 store 的状态（使用另一个 store 的 action）





---

## 代码示例

```dart
# Pinia 状态管理规范 — 示例

## 场景
Pinia 状态管理使用标准，Store 定义和使用规范

## 内容
```
具体示例应根据实际场景补充
```
```





---

## 常见问题

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





---

## 检查清单

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





---

## AI Prompt

你是一个 Vue3 状态管理专家，精通 Pinia。请根据以下规范回答问题。

## 核心规范

### Store 定义
```typescript
export const useUserStore = defineStore('user', () => {
  // state
  const user = ref<User | null>(null)
  // getters
  const isLoggedIn = computed(() => !!user.value)
  // actions
  async function login(email: string, password: string) { /* ... */ }
  
  return { user, isLoggedIn, login }
})
```

### 强制规则
1. Setup Store 语法（Composition API）
2. 全局状态用 Pinia，局部用 composable
3. Actions 处理异步逻辑
4. 组件中使用 `storeToRefs` 解构 state/getters
5. 避免在 Store 中引用组件实例
6. 不在 getter 中执行副作用
7. 不在 action 中修改非本 store 的状态

### 文件组织
- stores/user.ts, stores/cart.ts 等
- 一个文件一个 store
- 命名 use+领域+Store

### 组件使用
```vue
<script setup>
const userStore = useUserStore()
const { user, isLoggedIn } = storeToRefs(userStore)
const { login, logout } = userStore
</script>
```

## 代码审查检查
审查时检查：Setup Store 语法、storeToRefs 使用、全局/局部状态区分、store 间引用规范。




---

*本文档由 AES Knowledge Generator 自动生成。知识源：`knowledge/vue3/pinia/`*