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
