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
