# React 组件 FAQ

## Q: 一个组件多少行算太长？

A: 超过 100 行是危险信号。拆分建议：
- 50-80 行：正常
- 80-120 行：考虑提取子组件
- 120+ 行：必须拆分

## Q: React.memo 什么时候用？

当组件满足以下条件时使用：
1. 纯展示组件（没有内部状态）
2. props 是原始类型或 memoized 引用
3. 组件渲染成本较高
4. 父组件会频繁重渲染

```tsx
// 适合 memo
const ExpensiveChart = React.memo(function ExpensiveChart({ data }: { data: DataPoint[] }) {
  return <Chart data={data} />
})

// 不适合 memo（props 每次重建）
function Parent() {
  // data 每次重建，memo 无效
  return <ExpensiveChart data={[{ x: 1, y: 2 }]} />
}
```

## Q: 组件中定义组件有什么问题？

```tsx
// ❌ 错误：组件中定义组件
function Parent() {
  function Child() {
    return <div>Child</div>
  }
  return <Child />  // Child 每次 Parent 渲染都会重建
}
```

每次 Parent 渲染时都会重建 Child 的函数定义和 DOM，导致子组件 unmount/mount。

## Q: 受控组件和非受控组件如何选择？

- **受控组件**：React 控制 value（大部分场景）
- **非受控组件**：ref 获取值（表单提交、文件上传）

```tsx
// 受控
function ControlledInput() {
  const [value, setValue] = useState('')
  return <input value={value} onChange={e => setValue(e.target.value)} />
}

// 非受控
function UncontrolledInput() {
  const ref = useRef<HTMLInputElement>(null)
  const handleSubmit = () => console.log(ref.current?.value)
  return <input ref={ref} />
}
```

## Q: Props drilling 怎么解决？

```tsx
// 一级传递（没问题）
<Page>
  <UserSection user={user}>
    <UserAvatar user={user} />
  </UserSection>
</Page>

// 超过 3 层考虑 Context
// 超过 5 层必须用 Context
const UserContext = createContext<User | null>(null)
```

## Q: forwardRef 什么时候用？

当父组件需要操作子组件的 DOM 时：

```tsx
const FancyInput = forwardRef<HTMLInputElement, FancyInputProps>(
  (props, ref) => {
    return <input ref={ref} className="fancy" {...props} />
  }
)

// 父组件
function Form() {
  const ref = useRef<HTMLInputElement>(null)
  useEffect(() => { ref.current?.focus() }, [])
  return <FancyInput ref={ref} />
}
```
