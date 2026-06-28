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
