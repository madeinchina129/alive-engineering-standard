# React Router 路由规范

## 路由设计原则

### 声明式路由

React Router v6 使用声明式路由配置，路由即组件树：

```tsx
// ✅ 正确：声明式路由配置
const router = createBrowserRouter([
  {
    path: '/',
    element: <RootLayout />,
    errorElement: <ErrorPage />,
    children: [
      { index: true, element: <Home /> },
      { path: 'users', element: <UserList /> },
      { path: 'users/:id', element: <UserDetail /> },
    ],
  },
])

// ❌ 错误：手动处理路由匹配
if (window.location.pathname === '/users') {
  render(<UserList />)
}
```

### 嵌套路由对应 UI 嵌套

```tsx
// ✅ 路径和 UI 层次对应
<Route path="dashboard" element={<DashboardLayout />}>
  <Route index element={<DashboardHome />} />
  <Route path="analytics" element={<Analytics />} />
  <Route path="settings" element={<Settings />} />
</Route>
```

---

## 路由方案对比

| 方案 | 适用场景 | 优点 | 缺点 |
|------|---------|------|------|
| `createBrowserRouter` | 大型 SPA | 完整功能，支持 loader/action | 配置较复杂 |
| `<BrowserRouter>` | 中小型项目 | 简单直接 | 缺少 data API |
| `createHashRouter` | 静态部署 | 无需服务端配置 | URL 带 # |
| `createMemoryRouter` | 测试 / RN | 不依赖 URL | 无地址栏 |

---

## 适用范围

- **强制使用**：所有 React 项目的路由层
- **不使用路由的场景**：纯组件库、工具库
