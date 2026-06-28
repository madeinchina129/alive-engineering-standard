# GoRouter 路由方案

## 为什么选择 GoRouter

### 声明式路由配置

GoRouter 使用声明式 API 定义路由，所有路由在单一位置集中管理：

```dart
final router = GoRouter(
  routes: [
    GoRoute(
      path: '/',
      builder: (context, state) => const HomePage(),
    ),
    GoRoute(
      path: '/users/:id',
      builder: (context, state) => UserDetailPage(
        userId: state.pathParameters['id']!,
      ),
    ),
  ],
);
```

对比 Navigator 2.0 的手动 Page 管理，GoRouter 的可读性和可维护性显著提升。

### 类型安全的路由参数

GoRouter 的 `pathParameters` 和 `uriParameters` 提供类型安全的参数访问：

```dart
// 定义带参数路由
GoRoute(
  path: '/users/:userId/posts/:postId',
  builder: (context, state) {
    final userId = state.pathParameters['userId']!;
    final postId = state.pathParameters['postId']!;
    return PostDetailPage(userId: userId, postId: postId);
  },
);
```

### 内置重定向和守卫

GoRouter 原生支持路由守卫，无需额外实现：

```dart
final router = GoRouter(
  redirect: (context, state) {
    final isLoggedIn = authProvider.isLoggedIn;
    final isLoginRoute = state.matchedLocation == '/login';
    
    if (!isLoggedIn && !isLoginRoute) return '/login';
    if (isLoggedIn && isLoginRoute) return '/';
    return null; // 不重定向
  },
);
```

### 深度链接支持

GoRouter 自动处理 Android App Links 和 iOS Universal Links，无需额外配置。

### ShellRoute 实现持久化布局

```dart
final router = GoRouter(
  routes: [
    ShellRoute(
      builder: (context, state, child) => AppShell(child: child),
      routes: [
        GoRoute(path: '/home', builder: (context, state) => const HomePage()),
        GoRoute(path: '/profile', builder: (context, state) => const ProfilePage()),
      ],
    ),
  ],
);
```

ShellRoute 保持底部导航栏等 UI 元素在页面切换时不重建。

---

## 对比其他路由方案

| 维度 | Navigator 1.0 | Navigator 2.0 | GoRouter |
|------|---------------|---------------|----------|
| API 风格 | 命令式 push/pop | 声明式 Pages | 声明式 routes |
| 深度链接 | 手动处理 | 手动处理 | 自动 |
| 路由守卫 | 无 | 自行实现 | redirect 内置 |
| 类型安全 | 无 | 部分 | pathParameters |
| ShellRoute | 无 | 自行实现 | 内置 |
| URL 支持 | 无 | 需要自行解析 | 原生 path/query |

---

## 适用范围

- **强制使用**：所有页面间导航
- **推荐使用**：底部 Tab 导航、深度链接
- **不建议**：Dialog 和 BottomSheet 使用 showDialog 直接弹出

## 与项目其他部分的集成

- **Riverpod**：通过 `ref.watch(goRouterProvider)` 响应路由变化
- **状态管理**：路由守卫中的认证状态通过 Riverpod 获取
- **Dio**：路由变化不影响网络请求层
