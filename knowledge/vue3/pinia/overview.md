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
