# React 状态管理规范

## 状态管理策略

不同粒度的状态使用不同的管理方式：

```tsx
// 组件状态 → useState / useReducer
function Counter() {
  const [count, setCount] = useState(0)
  return <button onClick={() => setCount(c => c + 1)}>{count}</button>
}

// 全局状态 → Zustand / Context
const useStore = create<Store>((set) => ({
  user: null,
  setUser: (user) => set({ user }),
}))

// 服务端状态 → TanStack Query / SWR
function UserProfile({ id }) {
  const { data, isLoading } = useQuery(['user', id], () => fetchUser(id))
}
```

### 状态分层

```
  ┌──────────────┐
  │  服务端状态   │  ← TanStack Query / SWR（缓存 + 重新验证）
  ├──────────────┤
  │  全局客户端   │  ← Zustand / Context（跨组件共享）
  ├──────────────┤
  │  组件局部     │  ← useState / useReducer（UI 交互）
  └──────────────┘
```

---

## 状态管理方案对比

| 方案 | 适用场景 | 模板代码 | 性能 |
|------|---------|---------|------|
| `useState` | 简单组件状态 | 少 | 最优 |
| `useReducer` | 复杂状态逻辑 | 中 | 优 |
| `useContext` | 主题/语言等低频更新 | 中 | 差（高频更新） |
| Zustand | 中大型全局状态 | 少 | 优 |
| TanStack Query | 服务端数据 | 中 | 优 |
| Redux Toolkit | 大型应用 | 多 | 中 |

---

## 适用范围

- **组件状态**：useState / useReducer
- **跨组件共享**：Zustand / Context
- **服务端数据**：TanStack Query
