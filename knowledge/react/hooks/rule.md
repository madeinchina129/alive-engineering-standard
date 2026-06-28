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
