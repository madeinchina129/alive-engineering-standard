# React 组件设计规范

## 文件组织规范

### 组件文件结构

```
components/
├── ui/                    # 通用 UI 组件
│   ├── Button/
│   │   ├── Button.tsx
│   │   ├── Button.test.tsx
│   │   └── index.ts
│   └── Input/
│       ├── Input.tsx
│       ├── Input.test.tsx
│       └── index.ts
├── business/              # 业务组件
│   └── UserCard/
│       ├── UserCard.tsx
│       ├── UserCard.test.tsx
│       └── index.ts
└── layout/                # 布局组件
    ├── Container.tsx
    ├── Grid.tsx
    └── index.ts
```

### 每个组件一个目录

```tsx
// ✅ 正确：一个组件一个目录，index.ts 导出
// components/ui/Button/index.ts
export { Button } from './Button'
export type { ButtonProps } from './Button'

// ❌ 错误：多个组件在一个文件中
// components/ui/Button.tsx 包含 Button, ButtonGroup, ButtonIcon
```

## 强制规则 (MUST)

### 1. Props 使用 interface 定义并导出

```tsx
// ✅ 正确：Props 类型导出
export interface ButtonProps {
  label: string
  variant: 'primary' | 'secondary'
  onClick: () => void
}

export function Button({ label, variant, onClick }: ButtonProps) {
  return <button className={`btn-${variant}`} onClick={onClick}>{label}</button>
}

// ❌ 错误：Props 类型不导出或不定义
function Button(props: { label: string; variant: string }) {
  // ...
}
```

### 2. 避免 Props 默认值在解构时处理

```tsx
// ✅ 正确：解构时设置默认值
function Button({ label, variant = 'primary', size = 'md' }: ButtonProps) {
  return <button className={`btn-${variant} btn-${size}`}>{label}</button>
}

// ❌ 错误：在组件内部手动处理默认值
function Button(props: ButtonProps) {
  const variant = props.variant ?? 'primary'
  const size = props.size ?? 'md'
  // ...
}
```

### 3. 条件渲染使用三元或 &&，避免 IIFE

```tsx
// ✅ 正确
function UserCard({ user }: { user: User | null }) {
  return (
    <div>
      {user ? (
        <span>{user.name}</span>
      ) : (
        <span>未登录</span>
      )}
      {user?.isAdmin && <AdminBadge />}
    </div>
  )
}

// ❌ 错误：IIFE 条件渲染
function UserCard({ user }: { user: User | null }) {
  return (
    <div>
      {(() => {
        if (user) return <span>{user.name}</span>
        return <span>未登录</span>
      })()}
    </div>
  )
}
```

### 4. 列表渲染必须提供 key

```tsx
// ✅ 正确：使用唯一且稳定的 key
function UserList({ users }: { users: User[] }) {
  return (
    <ul>
      {users.map(user => (
        <li key={user.id}>{user.name}</li>
      ))}
    </ul>
  )
}

// ❌ 错误：使用 index 作为 key
{users.map((user, index) => (
  <li key={index}>{user.name}</li>
))}
```

### 5. 事件处理函数命名规范

```tsx
// ✅ 正确：handle{EventName} 命名
function SearchInput() {
  const [query, setQuery] = useState('')
  
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setQuery(e.target.value)
  }
  
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    onSearch(query)
  }
  
  return <form onSubmit={handleSubmit}>
    <input onChange={handleChange} />
  </form>
}
```

### 6. 使用 React.memo 优化重渲染

```tsx
// ✅ 正确：props 不变的纯展示组件用 memo
const UserAvatar = React.memo(function UserAvatar({ url, name }: AvatarProps) {
  return <img src={url} alt={name} />
})

// ❌ 错误：memo 不能代替 useMemo/useCallback 优化
// 如果 props 包含每次渲染都重建的对象/函数，memo 无效
```

## 推荐实践 (SHOULD)

### 1. 提取 render 逻辑为子组件

```tsx
// 当 JSX 超过 20 行，提取为子组件
function UserList({ users }: { users: User[] }) {
  return (
    <div>
      {users.map(user => (
        <UserListItem key={user.id} user={user} />
      ))}
    </div>
  )
}
```

### 2. 使用 Composition 模式

```tsx
// ✅ Props 组合优于配置
<Dialog>
  <DialogTitle>确认删除</DialogTitle>
  <DialogContent>确定要删除这条记录吗？</DialogContent>
  <DialogActions>
    <Button variant="ghost">取消</Button>
    <Button variant="danger">确认</Button>
  </DialogActions>
</Dialog>
```

## 禁止行为 (MUST NOT)

- ❌ 不要定义 100+ 行的组件（超过应考虑拆分）
- ❌ 不要在组件中定义其他组件（每次渲染重建）
- ❌ 不要在组件中直接修改 props
- ❌ 不要使用 index 作为列表 key
- ❌ 不要遗留 console.log
- ❌ 不要在渲染中执行昂贵计算（用 useMemo）
