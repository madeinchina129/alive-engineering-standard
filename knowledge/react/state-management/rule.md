# React 状态管理细则

## 强制规则 (MUST)

### 1. 非全局状态不要提升到全局 store

```tsx
// ✅ 正确：局部状态用 useState
function CommentForm() {
  const [text, setText] = useState('')
  return <input value={text} onChange={e => setText(e.target.value)} />
}

// ❌ 错误：局部表单状态放到全局 store
const useStore = create(() => ({ commentText: '' }))
function CommentForm() {
  const text = useStore(s => s.commentText)
  // ❌ 表单输入每次都触发全局更新
}
```

### 2. Zustand 使用 selector 避免不必要渲染

```tsx
// ✅ 正确：细粒度 selector
function UserName() {
  const name = useStore(s => s.user?.name)
  return <span>{name}</span>
}

// ❌ 错误：无 selector 导致全量渲染
function UserName() {
  const state = useStore()  // ❌ 任何状态变化都重渲染
  return <span>{state.user?.name}</span>
}
```

### 3. Context 仅用于低频更新

```tsx
// ✅ 正确：主题、语言等低频更新
const ThemeContext = createContext('light')
function App() {
  return (
    <ThemeContext.Provider value="dark">
      <ThemedButton />
    </ThemeContext.Provider>
  )
}

// ❌ 错误：高频更新用 Context（导致所有消费者重渲染）
const MouseContext = createContext({ x: 0, y: 0 })
```

### 4. 服务端数据用 TanStack Query

```tsx
// ✅ 正确：Query 管理服务端状态
function UserList() {
  const { data, isLoading, error } = useQuery({
    queryKey: ['users'],
    queryFn: () => fetch('/api/users').then(r => r.json()),
  })
}

// ❌ 错误：服务端数据放到 Zustand
const useStore = create(() => ({ users: [], loading: false }))
// ❌ 手动管理 loading/error/cache
```

### 5. useReducer 处理复杂状态

```tsx
// ✅ 正确：复杂状态用 useReducer
type Action = { type: 'increment' } | { type: 'decrement' }
function reducer(state: State, action: Action): State {
  switch (action.type) {
    case 'increment': return { count: state.count + 1 }
    case 'decrement': return { count: state.count - 1 }
  }
}

// ❌ 错误：多个 useState 管理关联状态
const [count, setCount] = useState(0)
const [step, setStep] = useState(1)
// count 和 step 逻辑耦合时容易不一致
```

## 推荐实践 (SHOULD)

### 使用 immer 简化不可变更新

```tsx
import { produce } from 'immer'
setState(produce(draft => { draft.user.name = 'Alice' }))
```

## 禁止行为 (MUST NOT)

- ❌ 表单输入放到全局 store
- ❌ Context 用于高频更新
- ❌ 无 selector 的 Zustand 使用
- ❌ 将服务端数据和 UI 状态混在同一个 store
