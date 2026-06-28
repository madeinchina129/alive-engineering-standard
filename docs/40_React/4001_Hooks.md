---
id: react.hooks
priority: P0
owner: Frontend Team
version: 1.0
generated: 2026-06-28
---

# Hooks 使用规范

> **领域**: React 开发规范 | **优先级**: P0 | **版本**: 1.0
> 
> React Hooks 使用标准，useState/useEffect/自定义 Hooks 规范



---

---

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


---

# React Hooks 使用规范

## 基础 Hooks 规范

### useState

```tsx
// ✅ 正确：基础类型自动推断
const [count, setCount] = useState(0)
const [name, setName] = useState('')

// ✅ 正确：复杂类型显式标注
const [user, setUser] = useState<User | null>(null)

// ✅ 正确：惰性初始化（计算昂贵的初始值）
const [data, setData] = useState(() => computeExpensiveInitialValue())

// ❌ 错误：不必要的 state（可从 props 计算）
function Message({ text }: { text: string }) {
  const [message] = useState(text)  // ❌ 应该直接用 props.text
  return <div>{message}</div>
}
```

### useEffect

```tsx
// ✅ 正确：明确的依赖数组
useEffect(() => {
  fetchUser(userId).then(setUser)
}, [userId])  // 依赖明确

// ✅ 正确：清理函数
useEffect(() => {
  const subscription = api.subscribe(id, callback)
  return () => subscription.unsubscribe()  // 组件卸载时清理
}, [id])

// ❌ 错误：缺少依赖
useEffect(() => {
  fetchUser(userId).then(setUser)  // eslint-disable-line
}, [])  // ❌ 应该包含 userId

// ❌ 错误：不必要的依赖
useEffect(() => {
  fetchUser(userId).then(setUser)
}, [userId, setUser])  // setUser 是稳定引用，不需要在依赖中
```

### useRef

```tsx
// ✅ 正确：DOM 引用
function AutoFocus() {
  const inputRef = useRef<HTMLInputElement>(null)
  
  useEffect(() => {
    inputRef.current?.focus()
  }, [])
  
  return <input ref={inputRef} />
}

// ✅ 正确：存储可变值（不触发重渲染）
function Timer() {
  const intervalRef = useRef<number>()
  
  const start = () => {
    intervalRef.current = window.setInterval(tick, 1000)
  }
  
  const stop = () => {
    clearInterval(intervalRef.current)
  }
  
  useEffect(() => () => stop(), [])
  
  return <button onClick={stop}>Stop</button>
}
```

### useMemo & useCallback

```tsx
// ✅ 正确：计算昂贵的派生值
const sortedList = useMemo(
  () => [...items].sort(compareFn),
  [items]
)

// ✅ 正确：传递给子组件的回调（使用 React.memo 时）
const handleClick = useCallback(
  (id: string) => dispatch({ type: 'SELECT', id }),
  [dispatch]
)

// ❌ 错误：过度优化
const doubled = useMemo(() => count * 2, [count])  // count * 2 不昂贵
```

## 强制规则 (MUST)

### 1. Hooks 只能在函数组件或自定义 Hooks 的顶层调用

```tsx
// ✅ 正确：顶层调用
function UserProfile() {
  const [user, setUser] = useState<User | null>(null)
  useEffect(() => { /* ... */ }, [])
  // ...
}

// ❌ 错误：条件或循环中调用
function UserProfile() {
  if (condition) {
    useState()  // ❌ 条件中调用 hooks
  }
  
  for (const item of items) {
    useEffect(() => { /* ... */ })  // ❌ 循环中调用 hooks
  }
}
```

### 2. useEffect 必须有明确的依赖

```tsx
// ✅ 正确：exhaustive-deps 规则
useEffect(() => {
  fetch(`/api/users/${userId}`).then(setUser)
}, [userId])

// 使用 eslint-plugin-react-hooks 确保依赖完整
```

### 3. 自定义 Hooks 以 use 开头

```typescript
// ✅ 正确
function useUser(id: string) { /* ... */ }
function useDebounce<T>(value: T, delay: number) { /* ... */ }

// ❌ 错误
function fetchUser(id: string) { /* 普通函数，不是 hook */ }
```

### 4. 避免在 useEffect 中使用 async 作为直接回调

```tsx
// ✅ 正确：内部定义 async 函数
useEffect(() => {
  async function load() {
    const data = await fetchData(userId)
    setData(data)
  }
  load()
}, [userId])

// ❌ 错误：useEffect 回调直接 async
useEffect(async () => {
  const data = await fetchData(userId)  // ❌ useEffect 不支持 async 回调
  setData(data)
}, [userId])
```

## 推荐实践 (SHOULD)

### 1. 提取复杂逻辑到自定义 Hook

```typescript
// ✅ 推荐：提取分页逻辑
function usePagination<T>(fetcher: (page: number) => Promise<T[]>) {
  const [page, setPage] = useState(0)
  const [data, setData] = useState<T[]>([])
  const [loading, setLoading] = useState(false)
  
  useEffect(() => {
    setLoading(true)
    fetcher(page).then(d => { setData(d); setLoading(false) })
  }, [page, fetcher])
  
  return { page, data, loading, setPage }
}
```

### 2. 状态合并

```tsx
// state 字段超过 3 个且一起变化时，使用 useReducer
const [state, dispatch] = useReducer(userReducer, initialState)
```

## 禁止行为 (MUST NOT)

- ❌ 在条件/循环/嵌套函数中调用 Hooks
- ❌ useEffect 缺少依赖
- ❌ useMemo/useCallback 过度优化简单计算
- ❌ 在 useEffect 中直接使用 async 回调
- ❌ 在 useState 中存储可以从 props 计算的值
- ❌ 在非组件/非 Hook 函数中使用 Hooks


---

# React Hooks FAQ

## Q: useEffect 的依赖数组应该包含什么？

A: 依赖数组中应包含所有在回调中使用的 props、state、以及从 props/state 派生的值。使用 `eslint-plugin-react-hooks/exhaustive-deps` 规则自动检查。

## Q: 如何在 useEffect 中使用 async/await？

```tsx
useEffect(() => {
  const controller = new AbortController()
  
  async function load() {
    try {
      const data = await fetch(`/api/users/${userId}`, {
        signal: controller.signal
      })
      setUser(data)
    } catch (err) {
      if (!controller.signal.aborted) {
        setError(err)
      }
    }
  }
  
  load()
  return () => controller.abort()  // 组件卸载取消请求
}, [userId])
```

## Q: useState 和 useReducer 如何选择？

- **useState**：简单独立的状态（字符串、数字、布尔）
- **useReducer**：复杂状态（多个字段、互相依赖、需要保证事务性）

```tsx
// useState 适合
const [count, setCount] = useState(0)
const [name, setName] = useState('')

// useReducer 适合
const [state, dispatch] = useReducer(formReducer, initialFormState)
```

## Q: useMemo 和 useCallback 什么时候真的需要？

只在两种情况下使用：
1. **passed to child with React.memo**
2. **计算开销很大**（如大数据排序、复杂格式化）

不要到处使用 useMemo/useCallback，它们本身有开销。

## Q: Stale Closure（过期闭包）问题怎么避免？

```tsx
// ❌ 过期闭包
useEffect(() => {
  setInterval(() => setCount(count + 1), 1000)
}, [])  // count 永远是 0

// ✅ 使用函数式更新
useEffect(() => {
  setInterval(() => setCount(c => c + 1), 1000)
}, [])

// ✅ 或使用 ref
const countRef = useRef(count)
countRef.current = count
useEffect(() => {
  setInterval(() => console.log(countRef.current), 1000)
}, [])
```

## Q: 如何在自定义 Hook 中返回稳定的引用？

```typescript
export function useToggle(initial = false) {
  const [value, setValue] = useState(initial)
  
  // ✅ useCallback 保持引用稳定
  const toggle = useCallback(() => setValue(v => !v), [])
  const setTrue = useCallback(() => setValue(true), [])
  const setFalse = useCallback(() => setValue(false), [])
  
  return { value, toggle, setTrue, setFalse }
}
```


---

# React Hooks Code Review Checklist

## 规则遵守
- [ ] Hooks 是否在顶层调用？
- [ ] 是否不在条件/循环/嵌套函数中调用 Hooks？
- [ ] 自定义 Hook 是否以 `use` 开头？
- [ ] 是否不在非组件/非 Hook 中使用 Hooks？

## useState
- [ ] 是否避免了不必要的 state？（可从 props 计算的值）
- [ ] 复杂初始化是否使用了惰性初始化？
- [ ] 状态更新是否使用函数式更新？（当新值依赖旧值时）

## useEffect
- [ ] 依赖数组是否完整？
- [ ] 是否避免了 useEffect 直接 async？
- [ ] 订阅/定时器是否有清理函数？
- [ ] 是否避免了不必要的 useEffect？（派生值用 useMemo）
- [ ] 网络请求是否有取消机制？（AbortController）

## useMemo / useCallback
- [ ] 是否只用于计算昂贵的操作？
- [ ] 是否只用于传递给 React.memo 子组件？
- [ ] 是否避免了过度优化？
- [ ] 依赖数组是否正确？

## 自定义 Hooks
- [ ] 是否提取了可复用的逻辑？
- [ ] 返回值是否稳定？（使用 useCallback/useMemo）
- [ ] 是否处理了组件卸载后的状态更新？
- [ ] 是否有完整的 TypeScript 类型？

## 性能
- [ ] 是否避免了不必要的重渲染？
- [ ] 大型列表是否使用了虚拟化？
- [ ] 是否避免了在渲染中执行昂贵计算？
- [ ] 是否有合理使用 useRef 存储可变值？


---

你是一个 React 前端专家，精通 Hooks。请根据以下规范回答问题。

## 核心规范

### Hooks 规则
- Hooks 只在函数组件/自定义 Hook 顶层调用
- 不在条件/循环/嵌套函数中调用 Hooks
- 自定义 Hooks 以 `use` 开头

### useState
- 基础类型自动推断，复杂类型显式 `useState<T | null>`
- 昂贵初始化使用惰性 `() => compute()`
- 不存储可从 props 计算的值

### useEffect
- 完整依赖数组（exhaustive-deps 规则）
- 不直接 async（内部定义 async 函数）
- 副作用清理函数（订阅/定时器/请求取消）
- 网络请求使用 AbortController 取消

### useMemo / useCallback
- 仅用于真实昂贵计算或 React.memo 子组件
- 避免过度优化

### 自定义 Hooks
- 提取可复用逻辑
- 返回值稳定（useCallback/useMemo）
- 处理组件卸载后的状态更新

## 强制规则
1. Hooks 调用顺序不变
2. useEffect 依赖完整
3. 不以 async 作为 useEffect 直接回调
4. 自定义 Hooks 以 use 开头
5. 避免不必要的 state/memo/callback

## 代码审查检查
审查时检查：Hooks 调用规则、useEffect 依赖、useMemo/callback 必要性、自定义 Hook 规范、类型安全。



---

*本文档由 AES Knowledge Generator 自动生成。知识源：`knowledge/react/hooks/`*
