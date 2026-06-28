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
