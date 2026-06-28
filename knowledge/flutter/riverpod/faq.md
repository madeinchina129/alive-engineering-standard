# Riverpod FAQ

## Q: Notifier 和 StateNotifier 有什么区别？应该用哪个？

**A:** `Notifier` 是 Riverpod 2.x 引入的替代方案，推荐在新代码中使用。

| 维度 | StateNotifier | Notifier |
|------|---------------|----------|
| 代码量 | 需要定义 State 类 + Notifier 类 | 只需要 Notifier 类 |
| 不可变状态 | 依赖 freezed 或手动 copyWith | 同理 |
| 内置功能 | 基础 | 更多生命周期回调 |
| 社区趋势 | 维护模式 | 推荐方案 |

**结论**：新代码使用 `Notifier` + `NotifierProvider`。仅在维护旧代码时使用 `StateNotifier`。

## Q: ref.read 和 ref.watch 有什么区别？

**A:** 这是 Riverpod 中最常被误解的概念。

- `ref.watch(provider)` — 监听变化，当 provider 的值变化时，当前 widget/provider 会重建
- `ref.read(provider)` — 读取当前值，不监听变化

**规则**：
- `build` 方法中：使用 `ref.watch`
- 事件回调中：使用 `ref.read`
- `ref.read` 在 build 中使用会导致 lint 警告

## Q: autoDispose 和 keepAlive 怎么配合使用？

**A:** `autoDispose` 让 provider 在不再被监听时自动销毁，`keepAlive` 阻止自动销毁。

```dart
// 页面级数据：autoDispose
final pageDataProvider = FutureProvider.autoDispose<List<Data>>((ref) async {
  return fetchData();
});

// 需要缓存的全局数据：autoDispose + keepAlive
final cacheProvider = FutureProvider.autoDispose<List<Data>>((ref) async {
  return fetchExpensiveData();
}).ref.keepAlive(); // 即使没有监听也保留

// 手动控制缓存失效
final cacheProvider2 = FutureProvider.autoDispose<List<Data>>((ref) async {
  final link = ref.keepAlive();
  ref.onDispose(() => link.close());
  return fetchData();
});
```

**最佳实践**：
- 页面/组件级数据：只用 `autoDispose`
- 全局配置/缓存：`autoDispose` + `keepAlive`
- 服务单例：不用 `autoDispose`

## Q: 如何测试 Riverpod 代码？

**A:** 使用 `ProviderContainer`，无需 Flutter Widget 测试框架。

```dart
void main() {
  test('UserListController loads users', () async {
    // 创建测试容器，覆盖真实 API
    final container = ProviderContainer(overrides: [
      userRepositoryProvider.overrideWithValue(
        MockUserRepository(), // 返回测试数据
      ),
    ]);

    // 触发加载
    await container.read(userListControllerProvider.notifier).loadUsers();

    // 验证状态
    final state = container.read(userListControllerProvider);
    expect(state.valueOrNull?.length, greaterThan(0));
  });
}
```

## Q: Riverpod 如何处理依赖循环？

**A:** 循环依赖在编译时就能发现（Riverpod 会检测并抛出 `ProviderException`）。

解决方案：
1. **拆分 Provider**：将循环中的公共逻辑提取为独立 Provider
2. **延迟加载**：使用 `ref.read` 而非 `ref.watch` 打破循环
3. **重新设计**：循环依赖通常意味着设计问题，考虑重新划分职责

```dart
// ❌ 循环依赖：A 依赖 B，B 依赖 A
final aProvider = Provider((ref) => A(ref.read(bProvider)));
final bProvider = Provider((ref) => B(ref.read(aProvider)));

// ✅ 解决方案：提取公共依赖 C
final cProvider = Provider((ref) => C());
final aProvider = Provider((ref) => A(ref.read(cProvider)));
final bProvider = Provider((ref) => B(ref.read(cProvider)));
```

## Q: family 修饰符怎么用？有什么限制？

**A:** `family` 让 Provider 接受参数，每个参数值对应独立的 Provider 实例。

```dart
// 定义
final userProvider = FutureProvider.autoDispose.family<User, String>(
  (ref, userId) => fetchUser(userId),
);

// 使用
final user = ref.watch(userProvider('user-123'));
final user2 = ref.watch(userProvider('user-456')); // 独立实例
```

**限制**：
- 参数必须实现 `hashCode` 和 `==`
- 参数数量过多时考虑封装为对象
- 每次参数变化都会创建新的 Provider 实例

## Q: Provider 中如何访问路由参数？

**A:** 通过 GoRouter + Riverpod 集成。

```dart
// 方案 1：在页面组件中读取路由参数，传给 Provider
final userProvider = FutureProvider.autoDispose.family<User, String>(
  (ref, userId) => ref.read(userRepositoryProvider).fetchById(userId),
);

class UserPage extends ConsumerWidget {
  const UserPage({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final userId = GoRouterState.of(context).pathParameters['id']!;
    final userAsync = ref.watch(userProvider(userId));
    // ...
  }
}

// 方案 2：通过 Provider 封装路由参数读取
final currentUserIdProvider = Provider<String?>((ref) {
  final routeState = ref.watch(goRouterProvider);
  return routeState.pathParameters['id'];
});
```

## Q: Notifier 中如何调用异步操作？

**A:** `Notifier` 的 `state` 是同步的，异步操作需要配合 `AsyncValue`。

```dart
class UserController extends Notifier<AsyncValue<List<User>>> {
  @override
  AsyncValue<List<User>> build() => const AsyncValue.loading();

  Future<void> loadUsers() async {
    state = const AsyncValue.loading();
    try {
      final users = await ref.read(userRepositoryProvider).fetchUsers();
      state = AsyncValue.data(users);
    } catch (e, st) {
      state = AsyncValue.error(e, st);
    }
  }
}
```

或者使用 `AsyncValue.guard` 简化：

```dart
state = await AsyncValue.guard(
  () => ref.read(userRepositoryProvider).fetchUsers(),
);
```

## Q: Provider 的 ref 和 WidgetRef 有什么区别？

**A:** 本质相同，但使用场景不同：

- `Ref` — 在 Provider 的 build 方法中使用
- `WidgetRef` — 在 ConsumerWidget 中使用

在 Provider 中获取另一个 Provider：
```dart
final myProvider = Provider((ref) {
  final other = ref.watch(otherProvider); // ✅ Ref
});
```

在 Widget 中获取 Provider：
```dart
Widget build(BuildContext context, WidgetRef ref) {
  final my = ref.watch(myProvider); // ✅ WidgetRef
}
```

两者都支持 `watch`, `read`, `listen`, `invalidate` 等方法。
