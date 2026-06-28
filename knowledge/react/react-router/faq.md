# React Router FAQ

## Q: `createBrowserRouter` 和 `<BrowserRouter>` 有什么区别？

`createBrowserRouter` 是 v6.4+ 的 data router API，支持 loader/action/errorElement 等数据路由功能。`<BrowserRouter>` 是传统方式，不支持 data API。

```tsx
// v6.4+：createBrowserRouter（推荐）
const router = createBrowserRouter([
  { path: '/users', element: <UserList />, loader: fetchUsers },
])

// 传统：BrowserRouter
function App() {
  return (
    <BrowserRouter>
      <Routes><Route path="/users" element={<UserList />} /></Routes>
    </BrowserRouter>
  )
}
```

## Q: loader 和 useEffect 获取数据哪个好？

loader 在路由切换时在组件渲染前执行，避免 loading 闪烁。useEffect 在组件挂载后才请求。

```tsx
// loader：数据在渲染前准备好
const router = createBrowserRouter([{
  path: '/users/:id',
  loader: ({ params }) => fetchUser(params.id!),
  element: <UserDetail />,
}])

// useEffect：先渲染空的组件，再请求
function UserDetail() {
  const [user, setUser] = useState()
  useEffect(() => { fetchUser(id).then(setUser) }, [id])
}
```

## Q: 嵌套路由的 `<Outlet />` 怎么用？

父路由渲染 `<Outlet />`，子路由的 element 会渲染在 Outlet 位置：

```tsx
function DashboardLayout() {
  return (
    <div>
      <Sidebar />
      <main><Outlet /></main>  {/* 子路由内容 */}
    </div>
  )
}
```

## Q: `NavLink` 比 `Link` 好在哪？

`NavLink` 提供 active 状态，方便高亮当前导航：

```tsx
<NavLink to="/users" className={({ isActive }) => isActive ? 'active' : ''}>
  用户管理
</NavLink>
```

## Q: 路由参数变化如何重新获取数据？

```tsx
// ✅ 用 key 强制 reset
function UserDetailPage() {
  const { id } = useParams()
  return <UserDetail key={id} userId={id} />
}

// ✅ 或者在 loader 中自动处理
```

## Q: 如何实现路由守卫？

```tsx
function RequireAuth({ children }: { children: React.ReactNode }) {
  const user = useAuth()
  if (!user) return <Navigate to="/login" replace />
  return <>{children}</>
}

// 使用
<Route path="dashboard" element={<RequireAuth><Dashboard /></RequireAuth>} />
```
