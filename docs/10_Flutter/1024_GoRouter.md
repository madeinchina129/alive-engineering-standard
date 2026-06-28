---
id: flutter.go_router
priority: P1
owner: Flutter Team
version: 1.0
generated: 2026-06-28
---

# GoRouter 路由规范

> **领域**: Flutter 开发规范 | **优先级**: P1 | **版本**: 1.0
> 
> Flutter 声明式路由配置，页面跳转和深层链接标准


> **关联规范**: [Riverpod 状态管理规范](../10_Flutter/1023_Riverpod.md)


---




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





---

## 使用规范

# GoRouter 使用规范

## 路由定义规则

### 集中管理所有路由

```dart
// ✅ 推荐：所有路由集中在一个文件
// lib/app/router.dart
final router = GoRouter(
  initialLocation: '/home',
  routes: $appRoutes,
  redirect: _authGuard,
);
```

```dart
// ❌ 禁止：路由分散在多个文件中
class HomePage extends StatelessWidget {
  // ❌ 不要在页面组件内部定义路由
  static const path = '/home';
  static GoRoute get route => GoRoute(path: path, builder: ...);
}
```

### 路由路径命名规范

```
/
├── /login                  # 认证相关
├── /home                   # 首页
├── /users                  # 用户管理
│   ├── /users              # 用户列表
│   └── /users/:id          # 用户详情
├── /settings               # 设置
│   ├── /settings/profile   # 个人资料
│   └── /settings/security  # 安全设置
└── /404                    # 未匹配
```

规则：
- 路径使用 `kebab-case`
- 路径参数使用 `:paramName` 格式
- 查询参数使用 `?paramName=value`
- 常量路径优先于动态路径

## 强制规则 (MUST)

### 1. 使用 ShellRoute 实现持久化布局

```dart
// ✅ 推荐：ShellRoute 保持底部导航
final router = GoRouter(
  routes: [
    ShellRoute(
      builder: (context, state, child) => MainShell(child: child),
      routes: [
        GoRoute(path: '/home', ...),
        GoRoute(path: '/search', ...),
      ],
    ),
  ],
);
```

### 2. redirect 必须轻量且无副作用

```dart
// ✅ 正确：redirect 只做路由判断
redirect: (context, state) {
  final auth = ref.read(authProvider);
  if (auth.isExpired) return '/login';
  return null;
}

// ❌ 错误：redirect 中执行副作用
redirect: (context, state) {
  await analytics.logRoute(state.matchedLocation); // ❌ 不要在 redirect 中 await
  ref.read(someProvider.notifier).doSomething();    // ❌ 不要在 redirect 中修改状态
  return null;
}
```

### 3. 页面组件通过构造函数接收参数

```dart
// ✅ 正确：类型安全的构造函数参数
GoRoute(
  path: '/users/:id',
  builder: (context, state) {
    final id = state.pathParameters['id']!;
    return UserDetailPage(userId: id);
  },
);

class UserDetailPage extends StatelessWidget {
  final String userId;
  const UserDetailPage({super.key, required this.userId});
  // ...
}

// ❌ 错误：在页面内部读取路由参数
class UserDetailPage extends StatelessWidget {
  // ❌ 不要这样
  Widget build(BuildContext context) {
    final routeState = GoRouterState.of(context);
    final id = routeState.pathParameters['id']!;
  }
}
```

### 4. 导航使用 context.go 而非 Navigator.push

```dart
// ✅ 推荐：使用 GoRouter 的导航方法
context.go('/users/123');
context.goNamed('userDetail', pathParameters: {'id': '123'});

// ❌ 避免：混用 Navigator API
Navigator.push(context, MaterialPageRoute(...));

// 例外：Dialog 和 BottomSheet 仍使用 showDialog / showBottomSheet
```

### 5. 使用路由名称而非路径字符串

```dart
// ✅ 推荐：使用命名路由
GoRoute(
  path: '/users/:id',
  name: 'userDetail',
  builder: (context, state) => UserDetailPage(
    userId: state.pathParameters['id']!,
  ),
);

// 导航时使用名称
context.goNamed('userDetail', pathParameters: {'id': '123'});

// ❌ 避免：硬编码路径字符串（难以维护）
context.go('/users/123');
```

## 推荐实践 (SHOULD)

### 1. 提取路由配置为单独文件

```dart
// lib/app/router_config.dart
final routerConfig = GoRouter(
  initialLocation: '/home',
  routes: [
    // ... 所有路由
  ],
  redirect: _handleRedirect,
  errorBuilder: (context, state) => const NotFoundPage(),
);
```

### 2. 使用 StatefulShellRoute 处理复杂的 Tab 导航

```dart
StatefulShellRoute.indexedStack(
  builder: (context, state, navigationShell) {
    return MainShell(navigationShell: navigationShell);
  },
  branches: [
    StatefulShellBranch(
      routes: [GoRoute(path: '/tab1', builder: ...)],
    ),
    StatefulShellBranch(
      routes: [GoRoute(path: '/tab2', builder: ...)],
    ),
  ],
);
```

### 3. 使用 errorBuilder 提供友好的 404 页面

```dart
final router = GoRouter(
  errorBuilder: (context, state) {
    return const NotFoundPage();
  },
);
```

## 禁止行为 (MUST NOT)

- ❌ 在 Widget build 方法中直接使用 `GoRouter.of(context).go()`
- ❌ 在 State.initState 中执行导航操作
- ❌ 使用字符串拼接构建路径（应使用 pathParameters）
- ❌ 在路由 builder 中执行异步操作
- ❌ 创建过深的路由嵌套（超过 5 层）





---

## 代码示例

```dart
// GoRouter 路由规范 — 示例
// Flutter 声明式路由配置，页面跳转和深层链接标准
// TODO: 补充具体实现
```





---

## 常见问题

# GoRouter FAQ

## Q: GoRouter 和 Navigator 2.0 是什么关系？

A: GoRouter 是 Flutter 团队基于 Navigator 2.0 封装的高层路由框架。Navigator 2.0 提供了 Pages API 但使用复杂度高，GoRouter 在其基础上提供了声明式 API 并解决了大部分常见路由需求。

## Q: ShellRoute 和 StatefulShellRoute 有什么区别？

- **ShellRoute**：简单的布局包裹，每次切换子路由时重建 child
- **StatefulShellRoute**：保持子路由状态，适合 Tab 切换场景

选型规则：
- 不需要保持状态（如设置页的侧边栏布局）→ ShellRoute
- 需要保持状态（如底部 Tab 导航）→ StatefulShellRoute.indexedStack

## Q: redirect 中能否访问 Riverpod Provider？

A: 可以，但需要注意：
- 使用 `ref.read` 而非 `ref.watch`（redirect 不是 build 方法）
- 不要在 redirect 中执行异步操作
- 不要在 redirect 中修改 Provider 状态

```dart
redirect: (context, state) {
  // 通过 Provider.container 获取
  final container = ProviderScope.containerOf(context);
  final isLoggedIn = container.read(authProvider);
  if (!isLoggedIn) return '/login';
  return null;
}
```

## Q: 如何处理嵌套导航？

- 浅嵌套（2-3 层）：直接使用 GoRoute 嵌套
- 深嵌套（4 层+）：考虑拆分路由表
- Tab 内导航：使用 StatefulShellRoute

## Q: 页面间如何传递复杂参数？

A: 推荐使用 extra 参数或编码为 JSON：

```dart
// 方式 1：extra 传递对象
context.go('/detail', extra: userObject);

// 方式 2：编码为查询参数
context.go('/detail', queryParams: {
  'data': jsonEncode(user.toJson()),
});

// 方式 3：推荐 - 通过 Provider 共享
// 在源页面写入 Provider
ref.read(selectedUserProvider.notifier).state = user;
// 在目标页面读取
final user = ref.watch(selectedUserProvider);
```

## Q: GoRouter 如何处理 404？

```dart
final router = GoRouter(
  errorBuilder: (context, state) {
    return Scaffold(
      appBar: AppBar(title: const Text('404')),
      body: Center(
        child: Text('Page not found: ${state.uri}'),
      ),
    );
  },
);
```





---

## 检查清单

# GoRouter Code Review Checklist

## 路由定义
- [ ] 所有路由是否集中在单一文件中管理？
- [ ] 路径是否使用 kebab-case？
- [ ] 参数是否使用 `:paramName` 格式？
- [ ] 是否使用 `name` 字段定义路由名称？
- [ ] 常量路径是否优先于动态路径？
- [ ] 嵌套层级是否超过 5 层？

## ShellRoute 使用
- [ ] 持久布局是否使用 ShellRoute 实现？
- [ ] Tab 导航是否使用 StatefulShellRoute？
- [ ] ShellRoute 的 child 参数是否正确使用？

## 导航安全
- [ ] redirect 是否轻量且无副作用？
- [ ] redirect 中是否没有异步操作？
- [ ] redirect 中是否没有修改 Provider 状态？
- [ ] initState 中是否没有执行导航？
- [ ] build 方法中是否没有直接调用 context.go？

## 页面参数
- [ ] 页面组件是否通过构造函数接收参数？（而非从 GoRouterState 读取）
- [ ] 复杂对象是否使用 extra 或 Provider 传递？
- [ ] 路由参数是否有类型安全？

## 错误处理
- [ ] 是否提供了 errorBuilder 处理 404？
- [ ] 是否处理了 pathParameters 为 null 的情况？

## 性能
- [ ] 路由配置是否懒加载？（使用 `builder` 而非 `pageBuilder` 时注意）
- [ ] 是否避免了过深的嵌套路由？





---

## AI Prompt

你是一个 Flutter 路由专家，精通 GoRouter。请根据以下规范回答问题。

## 核心规范

### 路由定义
- 所有路由集中在 lib/app/router.dart
- 路径使用 kebab-case，参数使用 `:paramName`
- 使用 `name` 字段命名路由，通过 `context.goNamed()` 导航

### 强制规则
1. 使用 ShellRoute/StatefulShellRoute 实现持久布局
2. redirect 必须轻量、同步、无副作用
3. 页面组件通过构造函数接收参数
4. 使用 `context.go` / `context.goNamed` 而非 Navigator.push
5. 使用路由名称而非硬编码路径字符串
6. initState / build 中禁止执行导航

### 布局规范
- 不需要保持状态 → ShellRoute
- 需要保持 Tab 状态 → StatefulShellRoute.indexedStack

### 参数传递
- 简单参数 → pathParameters
- 复杂参数 → extra 或 Provider
- 禁止在 Widget 内读取 GoRouterState.of(context)

## 代码审查检查
审查时检查：路由集中管理、路径命名规范、redirect 安全性、参数类型安全、错误处理。




---

*本文档由 AES Knowledge Generator 自动生成。知识源：`knowledge/flutter/go_router/`*