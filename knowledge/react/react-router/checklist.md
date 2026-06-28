# React Router Checklist

## 路由配置
- [ ] 是否使用 `createBrowserRouter`（v6.4+）？
- [ ] 是否配置了 `errorElement`？
- [ ] 大页面是否使用 `lazy()` 懒加载？
- [ ] 是否配置了 `Suspense fallback`？
- [ ] 404 页面是否配置了 `path="*"`？

## 导航
- [ ] 声明式导航是否使用 `<Link>` 或 `<NavLink>`？
- [ ] 编程式导航是否使用 `useNavigate()`？
- [ ] 是否避免 `window.location` 操作？
- [ ] 登录后跳转是否用 `replace: true`？
- [ ] `NavLink` 是否使用了 `isActive` 样式？

## 参数管理
- [ ] 路径参数是否使用 `useParams`？
- [ ] 查询参数是否使用 `useSearchParams`？
- [ ] 参数变更是否触发了数据重新获取？

## 嵌套路由
- [ ] 父路由是否使用 `<Outlet />`？
- [ ] 布局组件是否由父路由提供？
- [ ] 是否避免不必要路由层级（不超过 3 层）？

## 数据加载
- [ ] 是否使用了 `loader` 替代 `useEffect` + fetch？
- [ ] 加载状态是否有 fallback UI？
- [ ] 错误状态是否配置了 `errorElement`？
