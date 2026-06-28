# React Router 路由细则

## 强制规则 (MUST)

### 1. 路由路径参数使用 `useParams`

```tsx
// ✅ 正确：URL 参数通过 useParams 获取
function UserDetail() {
  const { id } = useParams<{ id: string }>()
  const user = useQuery(['user', id], () => fetchUser(id!))
  return <div>{user?.name}</div>
}

// ❌ 错误：手动解析 URL
function UserDetail() {
  const id = window.location.pathname.split('/').pop()
  // ...
}
```

### 2. 查询参数使用 `useSearchParams`

```tsx
// ✅ 正确：useSearchParams 管理查询参数
function UserList() {
  const [searchParams, setSearchParams] = useSearchParams()
  const page = Number(searchParams.get('page')) || 1

  const nextPage = () => setSearchParams({ page: String(page + 1) })
  return <button onClick={nextPage}>下一页</button>
}

// ❌ 错误：手动拼接 URL
function nextPage() {
  const params = new URLSearchParams(window.location.search)
  params.set('page', '2')
  window.location.href = `?${params.toString()}`
}
```

### 3. 导航使用 `useNavigate` 或 `<Link>`

```tsx
// ✅ 正确：声明式导航
function Nav() {
  return <Link to="/users">用户列表</Link>
}

// ✅ 正确：编程式导航
function LoginSuccess() {
  const navigate = useNavigate()
  useEffect(() => { navigate('/dashboard', { replace: true }) }, [])
  return null
}

// ❌ 错误：直接操作 window.location
function LoginSuccess() {
  window.location.href = '/dashboard'
}
```

### 4. 路由懒加载

```tsx
// ✅ 正确：lazy + Suspense
const UserList = lazy(() => import('./pages/UserList'))

function App() {
  return (
    <Suspense fallback={<Loading />}>
      <Routes>
        <Route path="/users" element={<UserList />} />
      </Routes>
    </Suspense>
  )
}

// ❌ 错误：同步加载大页面（增加首屏体积）
import UserList from './pages/UserList'
```

### 5. 错误边界路由

```tsx
// ✅ 正确：errorElement 处理路由级错误
const router = createBrowserRouter([
  {
    path: '/users/:id',
    element: <UserDetail />,
    errorElement: <UserErrorBoundary />,
  },
])

// ❌ 错误：没有 errorElement，用户看到白屏
```

## 推荐实践 (SHOULD)

### Layout Routes 共享 UI

```tsx
// 父路由提供布局，子路由填充 content
<Route element={<DashboardLayout />}>
  <Route path="analytics" element={<Analytics />} />
  <Route path="settings" element={<Settings />} />
</Route>
```

## 禁止行为 (MUST NOT)

- ❌ 直接操作 `window.location`
- ❌ 缺少 `errorElement` 导致白屏
- ❌ 路径硬编码在组件内部
- ❌ 不使用 Link 导致页面刷新
- ❌ 未懒加载的大页面（单文件 > 50KB）
