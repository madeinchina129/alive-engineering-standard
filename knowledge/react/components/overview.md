# React 组件设计规范

## 组件设计原则

### 单一职责

每个组件只做一件事。如果一个组件需要渲染多个不相关的 UI 区域，应该拆分为多个小组件。

```tsx
// ✅ 正确：拆分后的组件职责清晰
function UserProfile({ userId }: { userId: string }) {
  return (
    <div>
      <UserAvatar userId={userId} />
      <UserInfo userId={userId} />
      <UserStats userId={userId} />
    </div>
  )
}

// ❌ 错误：一个组件渲染太多不相关的 UI
function UserProfile({ userId }: { userId: string }) {
  return (
    <div>
      {/* 头像、信息、统计全部混在一起 */}
      <div>...</div> {/* 80 行的 JSX */}
    </div>
  )
}
```

### Props 设计

```tsx
// ✅ 正确：Props 明确、类型安全
interface ButtonProps {
  label: string
  variant: 'primary' | 'secondary' | 'ghost'
  size?: 'sm' | 'md' | 'lg'
  disabled?: boolean
  onClick: () => void
}

function Button({ label, variant, size = 'md', disabled, onClick }: ButtonProps) {
  return (
    <button
      className={`btn btn-${variant} btn-${size}`}
      disabled={disabled}
      onClick={onClick}
    >
      {label}
    </button>
  )
}
```

### 组合优于继承

```tsx
// ✅ 正确：使用 children 和 render props 组合
interface CardProps {
  title: string
  children: React.ReactNode
  footer?: React.ReactNode
}

function Card({ title, children, footer }: CardProps) {
  return (
    <div className="card">
      <div className="card-header">{title}</div>
      <div className="card-body">{children}</div>
      {footer && <div className="card-footer">{footer}</div>}
    </div>
  )
}
```

---

## 组件分类

| 类型 | 描述 | 是否包含状态 | 复用范围 |
|------|------|-------------|---------|
| UI 组件 | 纯展示，Button/Card/Input | ❌ 无状态 | 项目级 |
| 业务组件 | 封装业务逻辑，UserCard/OrderList | ✅ 有状态 | 模块级 |
| 布局组件 | 页面布局，Grid/Container | ❌ 无状态 | 项目级 |
| 页面组件 | 路由页面，HomePage/ProfilePage | ✅ 有状态 | 路由级 |

---

## 适用范围

- **强制使用**：所有 React 组件遵循本文规范
- **组件粒度**：UI 组件 < 业务组件 < 页面组件
- **状态位置**：越靠近使用位置的组件越合适持有状态
