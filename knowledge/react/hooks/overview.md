# React Hooks 方案

## 为什么使用 Hooks

### 函数组件替代 Class 组件

```tsx
// ✅ 推荐：函数组件 + Hooks
function UserProfile({ userId }: { userId: string }) {
  const [user, setUser] = useState<User | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchUser(userId).then(u => {
      setUser(u)
      setLoading(false)
    })
  }, [userId])

  if (loading) return <Spinner />
  return <div>{user?.name}</div>
}
```

对比 Class 组件，代码量减少 40%，逻辑更加集中。

### 自定义 Hooks 实现逻辑复用

```typescript
// hooks/useUser.ts
export function useUser(userId: string) {
  const [user, setUser] = useState<User | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<Error | null>(null)

  useEffect(() => {
    setLoading(true)
    fetchUser(userId)
      .then(setUser)
      .catch(setError)
      .finally(() => setLoading(false))
  }, [userId])

  return { user, loading, error }
}

// 在组件中使用
function UserProfile({ userId }: { userId: string }) {
  const { user, loading, error } = useUser(userId)
  // ...
}
```

对比 mixins 和 HOC，Hooks 没有命名冲突，类型推断完整。

---

## 对比其他方案

| 维度 | Class 组件 | Hooks | HOC | Render Props |
|------|-----------|-------|-----|-------------|
| 代码量 | 多 | 少 | 中 | 中 |
| 逻辑复用 | mixin | custom hooks | HOC 组合 | Render Props |
| 类型安全 | 有限 | 完整 | 中 | 中 |
| 测试 | 中 | 易 | 中 | 中 |
| 学习成本 | 中 | 中高 | 低 | 低 |

---

## 适用范围

- **强制使用**：所有新组件使用 Hooks
- **兼容**：已有 Class 组件逐步迁移
- **不适用**：Error Boundary 必须使用 Class 组件
